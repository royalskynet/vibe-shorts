"""生態推估：臺北各里 2024 總統得票 × 各里 20 歲以上人口組成 → 各族群柯／賴／侯得票率。

Goodman 生態迴歸：里得票率 = Σ 族群占比 × 族群得票率，有界最小平方（0~1），以里有效票加權。
假設：同一族群在各里投票傾向相同、各族群投票率相同（ponytail: 投票率差異未建模，要升級需里別年齡投票率）。
"""
import csv
from collections import defaultdict

import numpy as np

CEC = "/tmp/cec_db/x/voteData__2024總統立委__總統__"
RIS = "/tmp/tpe2026/eco/tpe_raw.csv"
CAND = {"1": "ko", "2": "lai", "3": "hou"}

AGE = {"20~24歲": "20 多歲", "25~29歲": "20 多歲", "30~34歲": "30 多歲", "35~39歲": "30 多歲",
       "40~44歲": "40 多歲", "45~49歲": "40 多歲", "50~54歲": "50 多歲", "55~59歲": "50 多歲",
       "60~64歲": "60 多歲", "65~69歲": "60 多歲"}
EDU = {"博畢": "研究所以上", "碩畢": "研究所以上", "大畢": "大學", "專畢": "專科",
       "高中畢": "高中職", "國中畢": "國中以下", "國小畢以下": "國中以下"}
DIMS = {
    "sex": ["男性", "女性"],
    "age": ["20 多歲", "30 多歲", "40 多歲", "50 多歲", "60 多歲", "70 歲以上"],
    "edu": ["國中以下", "高中職", "專科", "大學", "研究所以上"],
    "ssm": ["同婚", "非同婚"],
}


def rows(path):
    return csv.reader(open(path, encoding="utf-8-sig"))


def load_votes():
    name = {}
    for r in rows(CEC + "elbase.csv"):
        if r[0] == "63":
            name[(r[3], r[4])] = r[5]
    v = defaultdict(lambda: defaultdict(int))
    for r in rows(CEC + "elctks.csv"):
        if r[0] == "63" and r[4] != "0000" and r[5] != "0000":
            v[(name[(r[3], "0000")], name[(r[3], r[4])])][CAND[r[6]]] += int(r[7])
    return v


def load_pop():
    p = defaultdict(lambda: defaultdict(int))
    for r in rows(RIS):
        _, _, site, vil, sex, age, mar, edu, n = r
        if age == "15~19歲" or not n.isdigit():
            continue
        n = int(n)
        g = p[(site.replace("臺北市", ""), vil)]
        g["男性" if sex == "男" else "女性"] += n
        g[AGE.get(age, "70 歲以上")] += n
        g[EDU[edu]] += n
        g["同婚" if mar.endswith("相同性別") else "非同婚"] += n
        g["_adult"] += n
        g["_20_24"] += n * (age == "20~24歲")
        g["_25_29"] += n * (age == "25~29歲")
        g["_30_34"] += n * (age == "30~34歲")
    return p


LAMBDAS = [10 ** e for e in np.arange(-8, 2.01, 0.25)] + [np.inf]


def ridge(X, y, w, lam):
    """族群得票率 = 全市平均 + δ，δ 加 L2 收縮；X、y 先以加權平均置中。"""
    xm, ym = np.average(X, axis=0, weights=w), np.average(y, weights=w)
    Xc, yc, sw = X - xm, y - ym, np.sqrt(w)
    A = Xc * sw[:, None]
    if lam == np.inf:
        return ym + 0 * xm, xm
    d = np.linalg.solve(A.T @ A + lam * np.eye(X.shape[1]), A.T @ (yc * sw))
    d -= xm @ d  # 各族群欄加總為 1 → δ 有一個自由度不可識別，定成人口加權和為 0
    return ym + d, xm


def cv_lambda(X, Y, w, folds=10):
    """10 折交叉驗證，三位候選人誤差合計最小的 λ。"""
    idx = np.random.default_rng(0).permutation(len(w)) % folds
    err = []
    for lam in LAMBDAS:
        e = 0
        for k in range(folds):
            tr, te = idx != k, idx == k
            for y in Y:
                b, _ = ridge(X[tr], y[tr], w[tr], lam)
                e += np.sum(w[te] * (X[te] @ b - y[te]) ** 2)
        err.append(e)
    return LAMBDAS[int(np.argmin(err))], err


def fit(votes, pop, groups):
    keys = sorted(set(votes) & set(pop))
    X = np.array([[pop[k][g] / pop[k]["_adult"] for g in groups] for k in keys])
    w = np.array([sum(votes[k].values()) for k in keys], dtype=float)
    w /= w.mean()
    Y = [np.array([votes[k][c] / sum(votes[k].values()) for k in keys]) for c in ("ko", "lai", "hou")]
    lam, err = cv_lambda(X, Y, w)
    gain = 1 - min(err) / err[-1]  # 對照 λ=∞（每個族群都等於全市平均）的誤差降幅
    out = {c: np.clip(ridge(X, y, w, lam)[0], 0, 1) for c, y in zip(("ko", "lai", "hou"), Y)}
    res = {}
    for i, g in enumerate(groups):
        s = sum(out[c][i] for c in out)
        res[g] = {c: out[c][i] / s for c in out}
    return res, keys, lam, gain


def main():
    votes, pop = load_votes(), load_pop()
    miss_v = sorted(set(votes) - set(pop))
    miss_p = sorted(set(pop) - set(votes))
    print("里數 票", len(votes), "人口", len(pop), "對不上", miss_v[:5], miss_p[:5])
    assert len(miss_v) <= 3, miss_v
    city = {c: sum(v[c] for v in votes.values()) for c in ("ko", "lai", "hou")}
    print("全市 2024", city)
    adult = sum(p["_adult"] for p in pop.values())
    with open("/tmp/tpe2026/eco/groups2024.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(["dim", "group", "pop_share", "ko", "lai", "hou"])
        for dim, groups in DIMS.items():
            res, keys, lam, gain = fit(votes, pop, groups)
            print(f"{dim} λ={lam:.1e} 交叉驗證誤差比全市平均少 {gain:.0%}")
            for g in groups:
                ps = sum(pop[k][g] for k in keys) / sum(pop[k]["_adult"] for k in keys)
                wr.writerow([dim, g, f"{ps:.5f}"] + [f"{res[g][c]:.4f}" for c in ("ko", "lai", "hou")])
                print(f"{dim:4s} {g:8s} 占{ps:6.1%} 柯{res[g]['ko']:5.1%} 賴{res[g]['lai']:5.1%} 侯{res[g]['hou']:5.1%}")
            # 回推全市：族群得票率按人口加權，應接近實際
            back = {c: sum(res[g][c] * sum(pop[k][g] for k in keys) for g in groups) / adult for c in city}
            print("     回推全市", {c: f"{x:.1%}" for c, x in back.items()})
    with open("/tmp/tpe2026/eco/age_fine.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(["band", "pop"])
        for b in ("_20_24", "_25_29", "_30_34", "_adult"):
            wr.writerow([b, sum(p[b] for p in pop.values())])


if __name__ == "__main__":
    main()

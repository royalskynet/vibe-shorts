#!/usr/bin/env bash
# WO-19 驗收：第一集改稿（主 session 寫，Devin 不改）
set -u
F=/Users/51mini/dev/vibe-shorts-pipeline/films/wv-primer-1; N=$F/narration.md
fail=0; chk(){ echo "FAIL $1"; fail=1; }
for w in 不在乎他人痛苦 藏著人工智慧 汪達的故事，也是我們的故事 一顆砲彈 父母當場身亡 罩住全地球 一個人怎麼面對失去 祕密組織 恨一個人 武器炸到誰 沒爆 腦袋裡很混亂 本尊降臨 主動提出一個解法 這次彈指 悲傷不正是 愛的延續 孤獨 孤單 為什麼他們自願 躺上實驗台的動力 守著 打敗奧創，拯救 這個故事留下一句話 尋找連結 瞬滅 控制 接管 艾格妮絲 緋紅 哈克尼斯 飛彈 燉雞 蘇格蘭偷襲 捏 取名 命名; do
  grep -q "$w" "$N" && chk "稿裡還有「${w}」"
done
for w in 一個人怎麼在陪伴裡 成為被稱作鋼鐵人 不知民間疾苦 奪走了兄妹的父母 眼睜睜 史塔克工業 鋼鐵裝甲 罩住全世界 意識結構 汪達的故事還沒有結束 小鎮突然出現 籠罩 究竟發生了什麼 下一集 不能錯過 野心組織 兄妹的家 印著史塔克工業 危險的權杖 外星人入侵 融合 大軍 最後手段 倒下 催動 愛與失去 陪伴 找回 困 長大成人 對抗奧創 愛丁堡 酒館 彈指事件 "The Blip" 史塔克工業 軍火商 逆轉時間 泰坦星 心靈寶石 九頭蛇 奴役 賈維斯 兩者都不是; do
  grep -q "$w" "$N" || chk "稿裡缺「${w}」"
done
python3 - "$N" <<'PY' || fail=1
import sys, re
L = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
ok = True
n = sum(len(re.sub(r"[，。？！、「」《》：；…,.?!\s（）()]", "", l)) for l in L)
print(f"INFO 字數 {n}")
if not 1250 <= n <= 1700: print(f"FAIL 字數 {n} 不在 1250–1700"); ok = False
for l in L:
    if len(l) > 35: print(f"FAIL 超過 35 字：{l}"); ok = False
    if l.count("。") > 1: print(f"FAIL 一行兩個句號：{l}"); ok = False
sys.exit(0 if ok else 1)
PY
python3 - "$N" <<'PY2' || fail=1
import sys
L=[l.strip() for l in open(sys.argv[1],encoding="utf-8") if l.strip()]
idx=[i for i,l in enumerate(L) if "薩諾斯" in l]
secs=[i for i,l in enumerate(L) if l.startswith("## ")]
ok=True
if idx and any(idx[0]<s<idx[-1] for s in secs): print("FAIL 薩諾斯句跨了段落"); ok=False
if idx and idx[-1]-idx[0]>22: print(f"FAIL 薩諾斯句分散，第一句到最後一句跨 {idx[-1]-idx[0]} 行"); ok=False
i=[k for k,l in enumerate(L) if "打敗奧創" in l]; j=[k for k,l in enumerate(L) if "只剩她一個人" in l]
if i and j and i[0]<j[0]: print("FAIL 打敗奧創還在哥哥死之前"); ok=False
sys.exit(0 if ok else 1)
PY2
H=$(head -1 "$F/audit/humanize.md" | sed 's/^narration_sha: *//')
case "$(shasum -a 256 "$N" | cut -d' ' -f1)" in "${H:-NONE}"*) ;; *) chk "humanize 戳記不是現在的稿";; esac
grep -q "zh.wikipedia.org/zh-tw/彈指事件\|%E5%BD%88%E6%8C%87%E4%BA%8B%E4%BB%B6" "$F/SOURCES.md" || chk "SOURCES 缺彈指事件來源"
grep -qi "hair\|長髮" "$F/index.html" || chk "index.html 沒有長髮"
[ $fail -eq 0 ] && echo "ACCEPT-19 OK"
exit $fail

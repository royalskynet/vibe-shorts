## 任務

工作目錄：`/Users/you/dev/vibe-shorts-pipeline`。只建片目錄，不寫稿、不查資料、不 render、不 git commit。

照 `films/taipei-silence/` 複製出 `films/pikmin-bloom/`，依序做：

```bash
cd /Users/you/dev/vibe-shorts-pipeline
rsync -a films/taipei-silence/ films/pikmin-bloom/
cd films/pikmin-bloom && rm -rf out dist qa audit/*.log *.mp4 narration.md narration-v9-draft.md
cd ../..
bash scripts/mascot_install.sh films/pikmin-bloom
bash scripts/illust_install.sh films/pikmin-bloom
```
再把 `films/pikmin-bloom/build.sh` 裡 `OUT=` 的值由 `taipei-silence` 改成 `pikmin-bloom`（只改這一處，其他行不動）。`rhythm-profile`、`index.html`、`mix.py`、`TREATMENT.md`、`SOURCES.md`、`meta/facts.md` 保持範本原樣，下一張單才改。

## 驗收

```bash
cd /Users/you/dev/vibe-shorts-pipeline
test -f films/pikmin-bloom/index.html
test -f films/pikmin-bloom/mix.py
test -f films/pikmin-bloom/build.sh
test -f films/pikmin-bloom/cast.json
grep -q 'OUT=.*pikmin-bloom' films/pikmin-bloom/build.sh
if grep -q 'taipei-silence' films/pikmin-bloom/build.sh; then exit 1; fi
if [ -e films/pikmin-bloom/narration.md ]; then exit 1; fi
if [ -e films/pikmin-bloom/out ]; then exit 1; fi
test "$(diff -rq films/taipei-silence films/pikmin-bloom | grep -c 'build.sh')" -ge 1
```
預期整段 exit 0；開工前 `films/pikmin-bloom` 不存在，第一行就會失敗。

## 不動
`films/` 其他資料夾、`scripts/`、`tests/`、`refs/`、`PLAN.md`、任何閘門基準。

## 禁止
1. 不 render、不執行 `build.sh`、不 git commit。
2. 無頭機：禁止回報「請使用者手動貼 token／授權／執行指令」；憑證讀不到＝停手回報阻斷點。
3. 不碰 `refs/viral-text/pikmin-seed.md`。

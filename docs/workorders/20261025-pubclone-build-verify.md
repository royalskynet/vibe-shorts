# 工單：從公開版 clone 跑完整建置，證明範本片能出片

公開版技能包 royalskynet/vibe-shorts-skill 要讓外人自足做片。旁白步已驗過（23 句全過），
剩下混音→尋幀一致→藏字→逐幀渲染→合軌沒從公開 clone 跑過。這張單只要你跑完並留下成片。

工作目錄已備好：`.venv` 連結與 `assets/voice/` 參考音都在。已存在合格的
`films/nerf/nerf.mp4` 就什麼都不用做（冪等）。

做這一件事：

```bash
cd /tmp/pubcheck/vibe-shorts-skill/films/nerf
LIB=$HOME/dev/lemo-opuscar bash build.sh
```

build.sh 自己會 exec 到 `$HOME/.local/bin/heavy` 拿重活閘，你不用另外包。約 15～30
分鐘，渲染階段長時間沒輸出是正常的。跑完把最後 30 行原始輸出與成片秒數寫進回報。

## 驗收

```bash
cd /tmp/pubcheck/vibe-shorts-skill/films/nerf
test -s nerf.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 nerf.mp4)
/usr/bin/python3 -c "import sys;d=float(sys.argv[1]);sys.exit(0 if 40<d<50 else 1)" "$D"
A=$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 nerf.mp4)
[ "$A" = "audio" ]
cd /tmp/pubcheck/vibe-shorts-skill
/usr/bin/python3 scripts/precheck.py films/nerf
```

預期：`nerf.mp4` 存在、片長 40～50 秒、含音軌，且 `precheck.py` exit 0。

## 禁止

- 不要重建環境（`.venv`、參考音都已就位）。
- 不要改 `narration.md`、`cast.json`、`index.html`、`build.sh`。
- 不要改任何閘門門檻（`SIM_MIN`、`rhythm_check.py` 基準、`precheck.py` 的常數）。
- 不要 `git commit`、不要 push、不要跑 `publish-sync`。
- 不要同時跑兩支 `build.sh`，不要繞過 `heavy`。
- 失敗照原樣回報原始錯誤文字，不得宣告成功。

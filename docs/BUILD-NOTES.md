# 建置閘門經驗（bixiang-foreseeable 2026-11-25 沉澱）

新片複製舊目錄起手式、卡面修法、閘門數學，一次建好少跑幾輪 build。

## 複製目錄先改的殘留

- `build.sh` 的 `OUT=<舊片名>.mp4`：不改的話合軌產出舊檔名，旁白核對報「找不到成片」。連同 `<title>`、CARDS、EV、FACTS、meta/ 整組檢查。
- `meta/` 是最大雷：title/caption/published.json 會帶舊片內容上傳。新片全部重寫、published.json 歸零 `{}`。

## 藏字檢查（textless ink <0.03 擋）

量法：每張卡把字拿掉後，畫面自己還要有 ≥0.03 的墨。白紙文件、淡色泡泡、細線人在米底幾乎不算墨。

修法順序（全域先做，再補個案）：

1. 地面色帶加厚：`rr(40, 1170→1146, 1000, 30→54)`，一支改 24 處比逐卡快。
2. `stampC` 章填充 `globalAlpha × 0.3` 實色。
3. 文件類：`doc()` 加彩色書脊＋深色內文線＋底條（白紙在米底沒墨）。
4. 標籤全改實色 chip：`rr + CREAM 字`（證人的說法／容任／有罪／一審／十二道金牌…），比 plain 描邊字墨多又可讀。
5. **關鍵時序**：實色塊要畫在 `pop()` 外面。藏字取樣在卡片早段（lt≈0.3-0.4s），pop 晚於取樣點才出現的墨不算。

## 節奏閘門（相鄰幀亮度差異 calm ≥0.15）

量法：縮到 64×36 灰階算相鄰幀平均差。一格格 53px 高——**±4px 的 pop 和小物移動在縮圖後幾乎不計**。這門的真目的是抓「整片凍住的壞渲染」。

修法：加「全域連續微動」，一次性抬全片：

- `let CUR_LT`，drawCard 裡 `CUR_LT = lt`；
- `man()` 包一層 `y += sin(CUR_LT*1.7 + x*0.01) * 8`（小人呼吸，ep1 同型 ±4–8px）；
- `doc()`±8、`shop()`±5、`coin()`±6 同型漂移；
- 整卡 `g.translate(0, sin(t*0.7)*3)`——全部墨邊每幀都在動，這是最大的單一槓桿；
- 虛線行進 `lineDashOffset = -lt*60`（佔畫面小，單獨不夠，配著加）。

實測：只加 ±4px 小人呼吸 → 0.14；補到上面全套 → 0.15–0.16。

## 卡面可讀性（冷讀常抓）

- 字不壓深色色帶（紅字壓 DIM 帶對比不足），標籤一律實色 chip。
- 字不壓人：speech 泡泡的文字放泡泡上方或留白，不放人身。
- 內頁大標門 ≥72px 就擋：內頁強調字用 68px 以下（片尾系列名同級）。

## QA／稽核檔案格式

- `qa/review_log.md` 首行 `video_sha: <成片 sha256>`，內容要含七維評分：開場／手機可讀／動作／變化／構圖／貼合原稿／聲畫同步。
- `audit/verdicts.md` 首行 `engine=<codex|opencode|subagent>`＋narration_sha／sources_sha；裁決值只能是 `CON_WINS / PRO_WINS / SPLIT / UNRESOLVED`，寫完每個爭點要有 VERDICT＋REASON。
- narration.md 或 SOURCES.md 一改，稽核 sha 就過期：重跑 `devils.sh`、`coldread.sh script`；影片一改，`coldread.sh film` 的 video_sha 過期（WARN 不擋，但發布前刷新）。
- `index.html` 的 `FACTS` 物件要長成多行（regex 要 `\n};` 結尾），空物件也要留著。
- `deliver.sh` 參數是 mp4 路徑不是目錄：`scripts/deliver.sh films/<片>/<片>.mp4`。
- 稿冷讀的常態不通過＝它要求每句自帶完整法理，跟 75–95s 短片壓縮格式本質衝突；裁決慣例：逐條 wont-fix＋理由，實質 flag（事實過寬、動機斷言）單獨呈報使用者。

## heavy 鎖

全機重活序列（`~/.local/bin/heavy`）：nightly batch（laya、chiikawa-daily）會插隊，build 排著等放行就對了，不要殺別人的行程。

## JS 小坑

- `array.forEach(([t], k)` 會把字串解構成**只取第一個字**（「詐團說」→「詐」）。map 解構參數用在字串陣列前先看元素型別。

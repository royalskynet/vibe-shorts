# 配音線：決定與實測

## 結論

**採用 Qwen3-TTS Base，以 D 當範本複製音色。音色鎖定已驗證（2026-10-11）。**

D 是 Qwen3-TTS VoiceDesign 用一句話描述生出來的聲音（「台灣口音年輕女性、清亮溫柔、紀錄片旁白」）。VoiceDesign 每次生成都會重抽一個音色，所以把 D 這一段存起來當固定範本，之後每支片都用它複製，聲音才不會換人。

- 授權乾淨：Qwen3-TTS Apache-2.0、mlx-audio MIT，可離線、可商用。
- 速度：本機 M4，一段 16 秒旁白約 1.5–3 分鐘（大部分時間在載模型，批次生成會更快）。
- 範本檔已存進 `assets/voice/`，不要刪。

## 為什麼不是其他方案

| 方案 | 否決或降級的理由 |
|---|---|
| A 曉臻（edge-tts `zh-TW-HsiaoChenNeural`） | 台灣口音最省事、幾秒出一段，但走微軟 Edge 的線上朗讀服務，非官方開放介面，隨時可能失效；而且那是微軟的商用聲音，**複製它的音色拿去經營帳號有授權風險**，只能試聽 |
| F BreezyVoice（聯發科研究院，Apache-2.0） | 台灣口音最道地，但 Mac 只能用 CPU，20 秒音檔要 **17 分鐘**（約 50 倍即時）。降為備案 |
| HF Space 跑 BreezyVoice | 找得到的 20 個 Space 全不能用（官方連結是免費 CPU、輸出固定 0.6 秒空音；其餘建置失敗／執行錯誤／休眠／沒在跑）。自己複製一個掛 ZeroGPU 要 HF PRO 每月 $9，違反免費優先 |
| GPT-SoVITS（MIT ★63k） | 跟 Qwen3 的「拿現成模型直接複製」是同一類做法，沒有理由多裝 4GB。官方 README 寫明 Mac 用 MPS 訓練品質明顯變差。**定位**：等錄好 1 分鐘自己的乾淨人聲要微調時再用，那時它比 Qwen3 有優勢 |
| CosyVoice 3（★24k Apache-2.0） | BreezyVoice 就是從它改出來的，台灣口音不如 Breezy，沒有優勢 |
| fish-speech、IndexTTS2 | 研究授權／bilibili 自訂授權，商用要另外看條款，先排除 |
| ChatTTS | AGPL，太嚴格 |
| Kokoro（Apache-2.0） | 離線穩定但中文偏弱，lemo 自己的中文配音也是用 edge-tts |

## 候選一覽（試聽頁對照）

| 代號 | 做法 | 長度 |
|---|---|---|
| A | edge-tts 曉臻 HsiaoChen，標準語速 | 19.3 秒 |
| B | edge-tts 曉雨 HsiaoYu，標準語速 | 22.3 秒 |
| C | 曉臻，語速 −15%、音高 −3Hz | 22.7 秒 |
| D | Qwen3 VoiceDesign，一句話描述 | 18.9 秒 |
| D2 | 同一句描述再生成一次（**音色跟 D 不同**，證明 VoiceDesign 不穩） | 21.0 秒 |
| E | Qwen3 官方內建中文女聲 Vivian ＋「平靜、稍慢」 | 19.2 秒 |
| F | BreezyVoice 用 D 當範本重念 | 20.5 秒 |
| G | BreezyVoice HF Space 版 | 壞的（固定 0.6 秒空音） |
| H | Qwen3 Base 複製 A 的音色（範本＝A 前 7.8 秒） | 15.9 秒 |
| **I1** | **Qwen3 Base 複製 D（第一次）** | **15.68 秒** |
| **I2** | **Qwen3 Base 複製 D（第二次）** | **16.84 秒** |

試聽頁（私有 artifact）：

- 含 A–H：<https://claude.ai/artifact/1fDtLAhgc58ccoV7WsKsyM>
- 含 A–I2：<https://claude.ai/artifact/1MsXsR4nQHNupWvfA8FLhD>

I1／I2 是音色鎖定的驗證：同一個範本跑兩次，聽起來是同一個人，所以鎖得住。

兩段都比 D 原聲（18.88 秒）短 2–3 秒，彼此也差 1.2 秒。長度不穩可能是語速飄，也可能有吃字——**還沒用 Whisper 核過逐字稿**，正式量產前要補這道檢查。

## 復現方式

範本檔（都在 `assets/voice/`）：

| 檔案 | 用途 |
|---|---|
| `d24k.wav` | **正式範本**：D 整段轉 24kHz 單聲道，給 `--ref_audio` 用 |
| `d-reference-source.wav` | D 的原始輸出，保底 |
| `script.txt` | 範本的逐字稿，給 `--ref_text` 用（必須跟範本音檔完全對上） |
| `i1.mp3`／`i2.mp3`／`d-qwen-design.mp3` | 試聽用 |

環境（原本在 session scratchpad 裡，會被清掉，重建很快，模型已在 `~/.cache/huggingface` 不用重抓）：

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python 'mlx-audio==0.5.8'   # 連帶 mlx 0.32.3
```

生成：成片一律用 `.venv/bin/python scripts/voice.py films/<片>`（逐句念、Whisper 核稿）。單段試聽才直接叫 CLI：

```bash
.venv/bin/mlx_audio.tts.generate \
  --model mlx-community/Qwen3-TTS-12Hz-1.7B-Base-bf16 \
  --text "<要念的稿>" --lang_code Chinese \
  --ref_audio assets/voice/d24k.wav \
  --ref_text "$(tr -d '\n' < assets/voice/script.txt)" \
  --output_path ./out --file_prefix take1 --join_audio
```

## 已知的坑

- **Metal kernel 載入失敗**：記憶體吃緊時會在 7 秒內掛掉，訊息是 `[metal::Device] Unable to load kernel implicit_gemm_conv_2d_...`。重跑即可，但批次生成要留記憶體餘裕。2026-10-11 遇過一次。
- **BreezyVoice 的 Mac 安裝**：官方只給 Linux＋NVIDIA，改了 6 處依賴才裝起來，坑記在 fixindex 10386。其中 WeTextProcessing（數字轉國字讀法）沒有 Mac 版，換成「原樣通過」的替身，所以**稿子裡的「2026 年」「3.5 倍」要先手動改成國字**，不然會念錯。這條只在走 F 備案時才有影響。
- **HF Space 的 FINISHED 不等於成功**：呼叫前先查 `runtime.stage` 與 `hardware.current`，並驗輸出長度合不合理。記在 fixindex 10391。

## 配音在流水線裡的位置

**2026-10-13 改：從第一支就配旁白**（使用者決定）。原本照 Tom CC 前 5–10 支走純音樂＋字幕、之後再 A/B，這個做法作廢。

- 先用免費開源：Qwen3-TTS Base 複製 D（Apache-2.0，可商用，零成本）。
- 商業版之後再考慮，例如 ElevenLabs Starter（官方定價頁 10-13：首月 $6，含商用與聲音複製）。觸發條件：成片的配音被留言點名不自然，或要多語版本。
- 換到商業版時，要用 D 範本複製同一個音色，不要換聲音（理由見下一段）。

字幕照樣要上。

一旦開始用旁白，**聲音不要再換**：用 AI 女聲養出來的觀眾，之後換成本人的聲音會覺得換人了。

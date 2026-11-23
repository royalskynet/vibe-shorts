// 畫面字 OCR：macOS Vision（系統內建，零依賴）。
// 用法：swift scripts/vocr.swift <圖檔>…   印一個 JSON 字串陣列，一張一格（由上而下以空格串接）；任一張讀不了就 exit 1。
// 用 JSON 不用逐行：辨識結果可能含換行，逐行對應會讓後面每幀錯位（codex 11-10 審查）。
// 為什麼不用 tesseract：影片幀彩色底（紅底白字、深底黃字、照片底描邊字）各要不同前處理，
// 11-10 實測 tesseract 三種前處理都有一張認錯（紅底「冷」→「伶」），Vision 四張全對。
import Foundation
import Vision

var out: [String] = []
for path in CommandLine.arguments.dropFirst() {
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["zh-Hant", "en-US"]
    req.usesLanguageCorrection = true
    do {
        try VNImageRequestHandler(url: URL(fileURLWithPath: path)).perform([req])
    } catch {
        FileHandle.standardError.write("\(path): \(error)\n".data(using: .utf8)!)
        exit(1)
    }
    let obs = (req.results ?? []).sorted { $0.boundingBox.minY > $1.boundingBox.minY }
    out.append(obs.compactMap { $0.topCandidates(1).first?.string }.joined(separator: " "))
}
print(String(data: try! JSONSerialization.data(withJSONObject: out), encoding: .utf8)!)

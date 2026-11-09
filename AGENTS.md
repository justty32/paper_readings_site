# paper_readings_site

繁中論文入門教學站。`content/*.json` 是課程內容，`tools/build.py` 產生靜態 HTML；不要手改產生的頁面。概念課來源固定於 `content/site.json` 的 `source_commit`；單篇導讀 `content/paper_*.json` 各自以 `source_commit` 與 `source_path` 固定來源庫 `primers/` 母稿，驗證器須核對該 commit 與檔案存在，更新內容時同步母稿與來源版本。每篇論文須有原文與已讀筆記連結；未入庫成摘要／翻譯者明說，不能造筆記路徑。修改後執行 `python3 tools/build.py`、`python3 tools/check.py`。保持手機、鍵盤與無 JavaScript 可閱讀。教學玩具明確標為示意，不當成論文結果。正式站只用此 repo 的 GitHub Pages（public）；不可改回 Sites/chatgpt.site，也不要改變來源論文庫的 private 存取權。主分支 main；保留既有更動。

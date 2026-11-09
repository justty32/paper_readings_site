# 研究遊樂場

繁中 AI 論文入門站。用一個問題、一個具體例子和可操作圖解，走進研究；技術方法與限制收在原生摺疊區塊。

目前有 **10 個主題、28 課、12 篇單篇導讀、54 個頁面、46 篇代表性論文來源**。分類沿用 [paper_readings](https://github.com/justty32/paper_readings) A–J；智能體與系統類拆成11課。本站不是全庫逐篇摘要，圖與互動均為合成資料／手寫規則的教學示意。

## 開始閱讀

- [首頁](index.html)
- [重要論文導讀](papers.html)：從可手算的小例，走進 12 篇研究的方法與限制。
- [完整閱讀地圖](map.html)
- [關於本站與來源政策](about.html)

正式網站：**https://justty32.github.io/paper_readings_site/**

直接開啟 HTML 即可閱讀。要在本機使用一致的瀏覽器儲存與網址：

```sh
python3 -m http.server 8778 --bind 127.0.0.1
```

開啟 `http://127.0.0.1:8778/`。無安裝依賴、無登入、無追蹤；閱讀勾選只記在此瀏覽器。停用 JavaScript 時仍有完整文章、靜態例子、摺疊細節與來源。

## 維護

```sh
python3 tools/build.py
python3 tools/check.py
node --check assets/app.js
python3 tools/package_static.py
```

- `content/site.json`：分類、閱讀順序、固定來源 commit。
- `content/{foundations,core,agents}.json`：概念課正文及逐篇來源卡。
- `content/paths.json`：三條問題導向閱讀路徑，首頁與閱讀地圖共用；不影響原有閱讀進度。
- `content/paper_*.json`：單篇論文導讀，逐篇記錄 `source_path`／`source_commit`；母稿位於來源論文庫 `primers/`，網站改編保存在本 repo 的 JSON。圖解按相關段落排列，技術與實驗細節收在原生摺疊區塊。
- `tools/build.py`、`tools/illustrations.py`：靜態頁面與語意 SVG。
- `assets/`：本地 CSS、JavaScript，無外部字型或程式依賴。
- `dist/`：可發布檔案，從原始頁面複製產生，不進版本控制。
- `.github/workflows/pages.yml`：main 推送後以 GitHub Actions 重建、檢查與發布純靜態 dist。
- `docs/qa/`：桌面／手機截圖與瀏覽器驗證紀錄。

`check.py` 檢查全部本地連結、錨點、引用、課程 schema 和來源快照路徑；相鄰論文庫不存在時會明示略過來源物件檢查。瀏覽器驗證另確認 1440／390px 版面、28 課互動（既有瀏覽器驗證；本輪新增頁使用靜態 DOM／SVG 檢查，未另跑瀏覽器視覺驗證）、搜尋、閱讀勾選、清除、問答與無 JavaScript 回退。

## 來源範圍

固定來源快照 `1f91be9b96e04d7f0b6b074a90173a4375eb2214`（2026-11-05）。既有概念課依已提交的摘要與精要逐節譯文自讀編寫，未重新取得所有原始 PDF。新增的單篇導讀另外自讀公開原文核對，使用各篇自己的母稿快照；不會冒稱所有舊課都已更新來源。每課逐項連回原論文與實際使用的筆記；講義中的教學類比不宣稱是作者實驗。來源庫持續增加的論文不會自動改變本站。

需要更完整的符號迴歸計算實驗，可前往另一個已發布的[互動實驗室](https://justty32.github.io/engineer_study/symbolic-regression/)。

## 發布與存取

依使用者指定，正式網站只走此 repo 的 GitHub Pages。帳戶方案不支援私有 repo 的 Pages，因此新建的本站 repo 改為 public；原 paper_readings 論文庫仍保持 private，筆記連結需要存取權，arXiv 原文可公開閱讀。

涉及網站或建置流程的 push main 觸發 Actions（純文件／QA紀錄更新略過）：重建、檢查、封裝 `dist/`，再透過 Pages 部署。發布檔案只有 HTML、CSS、JavaScript 與 SVG，不包含 docs、QA、來源 JSON 或任何託管設定。精確版本與結果見 [發布紀錄](docs/DEPLOYMENT.md)。舊私有預覽已停止更新，見[遷移註記](docs/LEGACY-PREVIEW.md)。

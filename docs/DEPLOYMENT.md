# GitHub Pages 發布

正式網址：**https://justty32.github.io/paper_readings_site/**。

唯一正式流程為 `.github/workflows/pages.yml`：push main → 產生HTML → 靜態與JavaScript檢查 → 封裝純靜態dist → upload-pages-artifact → deploy-pages。只發布站點所需HTML、CSS、JavaScript與SVG，不把docs/qa、內容JSON或託管設定當網站資產。

## 2026-11-09：單篇圖解導讀與閱讀路徑

最後 DGM 窄篇版本 `2f2d216310efb2bec3b8d9d930579db1c3fd3804` 已由 [Actions 42585830895](https://github.com/justty32/paper_readings_site/actions/runs/42585830895) 成功部署，累計 13 篇導讀、55 頁、39 張論文 SVG；新母稿固定 `1759b9add4eb078c4983b959b201df6142a2e5c9`。103 個公開靜態檔 HTTP200 且 SHA256 全等於提交隔離快照，見[最後發布核對](qa/2026-11-09-dgm-publication.json)。DGM 同篇摘要、精要譯文及演化主題綜述三個目的地亦已核對，見[閱讀目標](qa/2026-11-09-dgm-reading-targets-http.json)。未開第二篇趕稿；本輪全程僅靜態／HTTP 驗證，未做瀏覽器版面或操作驗收。

閱讀層級導航與六題自測版本 `780719ef258787c7d588b439ce232fe93563f447` 已由 [Actions 42582262160](https://github.com/justty32/paper_readings_site/actions/runs/42582262160) 成功部署，99 個公開檔案 HTTP200 且 SHA256 等於隔離提交快照，見[公開核對](qa/2026-11-09-reading-and-self-checks-publication.json)。29 個公開筆記目的地及兩個子章另經 HTTP、題名、論文 ID 與版本核實，見[閱讀目標核對](qa/2026-11-09-reading-targets-http.json)。12 篇頁首與文末都提供同篇摘要、精要譯文、主題延伸及原文；KAN 缺少原始同篇筆記的狀態明示，MetaKAN 單獨標為後續研究。

連字號[公開筆記閱讀站](https://justty32.github.io/paper_readings-site/)亦已完成反向入口：鏡像版本 `b6636084b8e7f8567f72166a21c67ca598999817` 的 [Actions 42583007309](https://github.com/justty32/paper_readings-site/actions/runs/42583007309) 成功，Pages 為 built。內容快照保持 `c9d29302217534828571f025b99a3e9c289079c8`，只用來源模板 `2d581928a1aa07ea33cb9d54f879a617babd4f47` 加上全域回入門站鏈；2632 筆 manifest 來源雜湊一致，2628 頁排除導航／頁尾後正文文字逐字相同。13 回歸測試、完整本地連結驗證及六個公開代表檔的 HTTP／SHA 均通過，見[鏡像回鏈核對](qa/2026-11-09-mirror-backlink-publication.json)。私人來源、公開入門站與公開筆記鏡像的存取分工未變。

第三批內容版本 `35738f9d8a9abea48877e070f9c96e9c28e95fa4` 已由 [Actions 42578304966](https://github.com/justty32/paper_readings_site/actions/runs/42578304966) 成功部署，累計 12 篇導讀、54 頁、三條問題導向閱讀路徑。新四篇母稿固定 `766036350934d720a66979d398de3daa9680919b`。提交隔離快照重新建置通過，95 個公開靜態檔 HTTP200 且 SHA256 與該快照產物完全一致，見[第三批公開核對](qa/2026-11-09-third-publication.json)。本輪仍僅做靜態／HTTP 驗證，未做瀏覽器版面或操作驗收。

第二批內容版本 `d73c24ef5b2b0d86294e310b6d9740b5391426a7` 已由 [Actions 42577062345](https://github.com/justty32/paper_readings_site/actions/runs/42577062345) 成功部署，累計 8 篇單篇導讀、50 頁。新增四篇母稿固定 `6c07331018539a4bf4a6170de8efaa2b40e9a0f3`；首批仍使用原本固定版本。從此提交的獨立 `git archive` 快照重建並通過全部站點檢查，79 個公開檔案 HTTP 與 SHA256 全等於該快照產物，沒有混入下一批並行草稿。見[第二批公開核對](qa/2026-11-09-second-publication.json)。

內容版本 `0666fb8646e64b67f2181704ebc0c686daba5e0d` 已由 [Actions 42575104965](https://github.com/justty32/paper_readings_site/actions/runs/42575104965) 成功部署。新增入口 [重要論文導讀](https://justty32.github.io/paper_readings_site/papers.html)，共 46 頁；四篇母稿固定來源 `80b087d692d96581316ca7ee372a2530438d575a`，概念課保持原本的來源快照。

HTTP 核對 63 個公開靜態檔案全部成功，內容 SHA256 與本地 `dist/` 完全相同，證據見 [逐檔紀錄](qa/2026-11-09-first-publication.json)。本輪完成原文與獨立內容覆核、DOM／SVG、來源版本、連結／錨點、JavaScript 語法及純函式 mock 檢查；未做瀏覽器版面或操作驗收。

## 2026-11-05：初版

2026-11-05已實際對private repo建立Pages，API回覆HTTP422「Your current plan does not support GitHub Pages for this repository」。依使用者隨後明確指定GitHub Pages的授權，在稽核無憑證及私人資料後，將新建本站repo改public；來源paper_readings仍為private。本站來源筆記需原庫GitHub權限，arXiv原文入口公開。

最終網站內容部署 `c46c0c3b8fdd632bbf3f0b4470bf30b846dafc9c` 已成功：[Actions 41985769569](https://github.com/justty32/paper_readings_site/actions/runs/41985769569) build與deploy皆success。正式URL的44個靜態檔HTTP200且SHA256與本地dist完全相同；content/site.json、docs/qa/browser-report.json與舊hosting設定路徑皆HTTP404。正式站另通過41頁桌面／手機、28課互動、已知約束與查詢分工、JSON語法與語意、保留輸入及並列流程等檢查，見 [QA](qa/README.md)。

純docs、README、AGENTS與瀏覽器QA腳本更動不觸發重新發布；網站內容與建置流程更動仍觸發完整部署。第一次private預覽已停止更新；其限制另記[遷移註記](LEGACY-PREVIEW.md)。

GitHub標準流程參考：[Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

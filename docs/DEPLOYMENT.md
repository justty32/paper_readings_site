# GitHub Pages 發布

正式網址：**https://justty32.github.io/paper_readings_site/**。

唯一正式流程為 `.github/workflows/pages.yml`：push main → 產生HTML → 靜態與JavaScript檢查 → 封裝純靜態dist → upload-pages-artifact → deploy-pages。只發布站點所需HTML、CSS、JavaScript與SVG，不把docs/qa、內容JSON或託管設定當網站資產。

2026-11-05已實際對private repo建立Pages，API回覆HTTP422「Your current plan does not support GitHub Pages for this repository」。依使用者隨後明確指定GitHub Pages的授權，在稽核無憑證及私人資料後，將新建本站repo改public；來源paper_readings仍為private。本站來源筆記需原庫GitHub權限，arXiv原文入口公開。

目前正在等待此輪Actions發布與正式URL內容驗收。第一次private預覽已停止更新；其限制另記[遷移註記](LEGACY-PREVIEW.md)。

GitHub標準流程參考：[Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

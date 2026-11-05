# 2026-11-05 驗證

- 靜態：41頁、28課、10分類，全部本地連結與錨點、正文引用、45個固定已讀筆記路徑通過。
- 瀏覽器：Windows Chrome headless，獨立使用者資料目錄及CDP連接埠，沒有開啟可見視窗或佔用鍵盤焦點。
- 1440px／390px：41頁逐頁無橫向溢位、互動空白或JavaScript例外，共82個版面檢查。
- 28課：實際點擊每個互動按鈕、調整各旋鈕／選項，確認有效解釋與無執行錯誤。
- 功能：主題搜尋及無結果狀態、閱讀勾選跨頁保存、清除勾選、選答回饋、停用JavaScript的靜態例子。
- 額外：320px KAN抽查、Space鍵開啟原生details。
- 修正回歸：已知約束與查詢分工、可解析但數量錯誤的JSON、保留輸入不含訓練點、並列工作與串行交接的視覺差異。

正式GitHub Pages另以相同測試巡檢，44個發布檔HTTP200且精確SHA256一致，未發布路徑HTTP404，見 [正式站檢查](github-pages-http.json)。Linux urllib的外網路由無法連線，位元組核驗改由實際Windows headless Chrome同源fetch完成，沒有繞過認證或變更網路。

詳細執行紀錄在 [browser-report.json](browser-report.json)。代表截圖：首頁桌面／手機、I類總覽、ARC手機、符號迴歸首屏及互動區、工具呼叫手機、智能體記憶展開細節。

可重現：先啟動本地靜態伺服器及一個獨立headless瀏覽器，再執行：

```sh
SITE_URL=http://127.0.0.1:8778/ BROWSER_CDP_URL=http://127.0.0.1:9335 node tools/browser_qa.mjs
```

本機沒有Linux Chrome執行所需的libnspr4，因此使用已安裝Windows Chrome的headless模式。未安裝新瀏覽器，未操作使用者原有分頁。

內容驗證依固定快照的已讀筆記，不宣稱重讀45篇全部原PDF。主線已實際覆核子線正文與來源卡，另回讀世界模型定理假設、Ratchet退役與非發散條件、TTT資料邊界等易過度推論處。所有圖與玩具均標示合成／教學，沒有拿玩具結果當論文效能。arXiv原文入口未做45篇批次HTTP壓力檢查；GitHub筆記連結的commit與路徑已用Git物件逐一核實。

## 獨立內容覆核

兩位內容作者交叉重讀對方主題，另由非作者審A/C/H/J。28課合計101組證據記錄、127段行號範圍、62份來源章節；主線已核行號存在並抽查高風險定理、資料邊界與修正。

- [I類11課](review-agents.json)
- [B/D/E/F/G十課](review-core.json)
- [A/C/H/J七課](review-foundations.json)
- [新手可讀性](review-readability.json)
- [接受的修正與驗證](review-resolutions.json)

唯一內容概念修正是將A1的已知和與待答查詢分開；其他改善針對玩具語義與標示，沒有增加頁數。原評審報告保留當時finding，解決情形另記resolutions，避免把歷史審核直接改成全部通過。

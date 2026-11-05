#!/usr/bin/env python3
"""Build the whole site using only Python's standard library."""
import json,re,sys
from html import escape as e
from pathlib import Path
from urllib.parse import quote
sys.path.insert(0,str(Path(__file__).parent))
from illustrations import svg,home_svg
ROOT=Path(__file__).resolve().parent.parent
SITE=json.loads((ROOT/'content/site.json').read_text())
LESSONS=[]
for p in sorted((ROOT/'content').glob('*.json')):
 if p.name!='site.json': LESSONS+=json.loads(p.read_text())['lessons']
BY={x['id']:x for x in LESSONS}; CATS={x['id']:x for x in SITE['categories']}
BASE=SITE['source_repo']+'/blob/'+SITE['source_commit']+'/'

def rich(text):
 return re.sub(r'\[arxiv:([\d.]+)\]',lambda m:f'<a class="citation" href="#source-{m[1]}">〔{m[1]}〕</a>',e(text))
def link(path):return BASE+quote(path,safe='/')
def nav(depth=0,current=''):
 pre='../'*depth
 return f'''<a class="skip" href="#main">跳到主要內容</a><header class="site-header"><nav class="nav" aria-label="主要導覽"><a class="brand" href="{pre}index.html"><span class="brand-mark" aria-hidden="true">∿</span>研究遊樂場</a><div class="nav-links"><a href="{pre}index.html#topics" {'aria-current="page"' if current=='topics' else ''}>主題探索</a><a href="{pre}map.html" {'aria-current="page"' if current=='map' else ''}>閱讀地圖</a><a href="{pre}about.html" {'aria-current="page"' if current=='about' else ''}>關於與來源</a></div></nav></header>'''
def footer(depth=0):
 pre='../'*depth
 return f'''<footer class="site-footer"><div class="shell footer-inner"><p>研究遊樂場 · 把問題拆小，把理解走深。<br>繁中圖解入門 · 所有互動皆為教學示意。</p><p><a href="{pre}about.html">來源與閱讀方式</a> · <a href="{pre}map.html">完整閱讀地圖</a><br>論文庫快照 {SITE['snapshot_date']} · <a href="{SITE['source_repo']}/tree/{SITE['source_commit']}">{SITE['source_commit'][:7]}</a></p></div></footer>'''
def page(title,body,depth=0,current='',description=''):
 pre='../'*depth
 return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#172d38"><title>{e(title)}｜研究遊樂場</title><meta name="description" content="{e(description or SITE['description'])}"><link rel="icon" href="{pre}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{pre}assets/style.css"><script src="{pre}assets/app.js" defer></script></head><body>{nav(depth,current)}{body}{footer(depth)}</body></html>'''
def write(path,text):
 dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True)
 if str(path).endswith('.html'):
  canonical=SITE['site_url']+('' if str(path)=='index.html' else str(path))
  text=text.replace('<head>','<head><link rel="canonical" href="'+canonical+'">',1)
 dest.write_text(text+'\n')
def crumb(cat=None,lesson=False):
 s='<div class="breadcrumb"><a href="../index.html">首頁</a><span aria-hidden="true">/</span>'
 if cat:s+=f'<a href="../topics/{cat["id"]}.html">{e(cat["name"])}</a>' if lesson else e(cat['name'])
 return s+('<span aria-hidden="true">/</span><span>入門課</span>' if lesson else '')+'</div>'
def topic_card(c):
 n=len(c['route']); terms=' '.join([c['name'],c['tag'],c['question'],c['intro']]+[BY[x]['title']+' '+BY[x]['subtitle'] for x in c['route'] if x in BY])
 return f'''<a class="topic-card" href="topics/{c['id']}.html" style="--topic:{c['color']}" data-search="{e(terms)}"><div class="card-art">{svg(c['icon'],c['question'])}</div><div class="card-copy"><div class="card-top"><span>領域 {c['id'].upper()} · {e(c['tag'])}</span><span>{n} 課</span></div><h3>{e(c['name'])}</h3><p>{e(c['question'])}</p><div class="card-bottom"><span>從小問題開始</span><span class="arrow" aria-hidden="true">↗</span></div></div></a>'''

home=f'''<main id="main" class="shell"><section class="hero"><div><span class="eyebrow">A FIELD GUIDE TO AI RESEARCH · 繁中入門</span><h1>論文很深。<br>入口可以<em>很淺。</em></h1><p class="lede">從一個小問題出發，用圖解、玩具例子和可展開的細節，走過 AI 研究的核心想法。</p><div class="hero-actions"><a class="button" href="#topics">挑一個主題 <span aria-hidden="true">↓</span></a><a class="button secondary" href="map.html">跟著路徑讀</a></div></div><figure class="hero-art"><div class="art-label">一張方法地圖 / 先理解問題，再認識論文</div>{home_svg()}<figcaption>觀察、規則、搜尋、驗證：不同研究，把力氣放在不同地方。</figcaption></figure></section><div class="note-strip"><div><strong>10 個主題</strong>從神經符號到智能體</div><div><strong>{len(LESSONS)} 堂小課</strong>每次只弄懂一個核心</div><div><strong>你決定深度</strong>細節與限制，隨時展開</div></div><section class="section"><div class="section-head"><div><span class="eyebrow">START WITH A QUESTION</span><h2>先挑你想問的問題</h2></div><p class="muted">不必照字母順序。先讀直覺，再動手改一個條件，最後回到論文看方法與邊界。</p></div><div class="path-grid"><article class="path-card"><div class="number">01</div><h3>想看懂 AI 怎麼推理</h3><p>從感覺與規則的合作，到彩色方格裡的抽象。</p><a href="lessons/neurosymbolic.html">神經符號 → 邏輯推理 → ARC ↗</a></article><article class="path-card"><div class="number">02</div><h3>想讓資料說出規律</h3><p>從找公式、減少重複搜尋，到可檢視的曲線。</p><a href="lessons/symbolic-regression.html">符號迴歸 → 等價性 → KAN ↗</a></article><article class="path-card"><div class="number">03</div><h3>想知道智能體怎麼做事</h3><p>從工具與記憶，走到驗證、成本和不確定性。</p><a href="lessons/tool-use.html">工具 → 記憶 → 自我修正 ↗</a></article></div></section><section class="section" id="topics"><div class="section-head"><div><span class="eyebrow">EXPLORE THE LANDSCAPE</span><h2>十個入口，各走一小段</h2></div><p class="muted">分類沿用論文閱讀庫。每個入口有自己的課程；智能體與系統再拆成 11 站。</p></div><div class="filters"><label class="sr-only" for="topic-search">搜尋主題或課名</label><input class="search" id="topic-search" type="search" placeholder="搜尋主題、問題或課名，例如：公式、記憶…"><span class="filter-count" id="search-count" aria-live="polite">10 個主題</span></div><div class="grid" id="topic-grid">{''.join(topic_card(c) for c in SITE['categories'])}</div><p class="empty no-results" id="no-results">沒有符合的主題。試試「推理」「公式」「工具」，或清空搜尋。</p></section><section class="dark-section"><div><span class="eyebrow">LESS JARGON, MORE UNDERSTANDING</span><h2>不用一次讀完，<br>也不用先懂所有術語。</h2></div><div><p>每課的主線先用日常例子解釋。想知道公式、實作和限制，再打開細節。玩具只示範概念；論文實際做了什麼，會另外標出來源。</p><a href="about.html">了解這個站怎麼選內容 ↗</a></div></section></main>'''
write('index.html',page('從一個小問題走進 AI 論文',home))

for c in SITE['categories']:
 rows=''
 for i,id in enumerate(c['route']):
  if id not in BY:continue
  l=BY[id]
  rows+=f'''<li class="lesson-row" data-lesson="{id}"><div class="step-num">{i+1:02}</div><div><h3><a href="../lessons/{id}.html">{e(l['title'])}</a></h3><p>{e(l['subtitle'])}</p><span class="read-badge">已走過這一課</span></div><a class="button secondary" href="../lessons/{id}.html">開始讀 <span aria-hidden="true">↗</span></a></li>'''
 body=f'''<main id="main" class="shell" style="--topic:{c['color']}">{crumb(c)}<section class="topic-hero"><div><span class="eyebrow">領域 {c['id'].upper()} / {e(c['tag'])}</span><h1>{e(c['name'])}</h1><p class="lede">{e(c['question'])}</p><p class="muted">{e(c['intro'])}</p><span class="pill">{len(c['route'])} 課 · 從直覺到論文</span></div><figure>{svg(c['icon'],c['question'])}<figcaption>教學示意 · {e(c['tag'])}</figcaption></figure></section><section class="section"><div class="section-head"><div><span class="eyebrow">A SMALL LEARNING PATH</span><h2>從這裡，一課一課走</h2></div><p class="muted">每課先讀約 5–8 分鐘。開啟細節與來源後，可以停留得更久。</p></div><div class="category-note">{('系統問題彼此相連，但工具、記憶、成本和可信度各有自己的評估方式。這 11 課可依需要選讀；先走前三課，會得到一個最小的智能體輪廓。' if c['id']=='i' else '建議先走直覺課，再看方法與邊界。下方只選代表性論文解釋核心想法，完整分類另有連結，並非全庫逐篇摘要。')}</div><ol class="lesson-list">{rows}</ol></section><section class="dark-section"><div><span class="eyebrow">BACK TO THE PAPERS</span><h2>懂了輪廓，<br>再回去挑一篇。</h2></div><div><p>課程中的每個來源卡都說明「這篇解什麼問題、怎麼做、哪裡要保留條件」。要看更多同類論文，可回到原始閱讀庫。</p><a href="{link(c['index'])}">查看 {e(c['name'])} 完整索引 ↗</a></div></section></main>'''
 write(f'topics/{c["id"]}.html',page(c['name'],body,1,'topics',c['intro']))

QUIZ={
'neurosymbolic':('若感知把真實候選漏掉，規則一定能補回來嗎？',['不一定，還要看候選與規則是否足夠','一定，邏輯會自動知道現實'],0,'規則只能處理它拿到的表示；缺失的候選或錯誤前提仍會造成失敗。'),
'logic-belief':('取所有合規世界的權重總和，等同挑出單一最大權重世界嗎？',['相同，只是說法不同','不同，前者聚合、後者最大化'],1,'加總與取最大值是不同推理目標。'),
'symbolic-regression':('兩條公式穿過同樣三點，就證明它們相同嗎？',['是，三點足夠','否，未觀測位置仍可能分歧'],1,'有限樣本的吻合不等於對所有輸入的恆等。'),
'equivalence':('少數輸入輸出接近，能直接證明兩式精確等價嗎？',['可以','不行，要有合法的語意與改寫依據'],1,'取樣相似是證據；精確等價需要相應證明或規則。'),
'kan':('每條邊能畫成曲線，就保證模型是因果正確的嗎？',['不能，仍需驗證','能，因為曲線可見'],0,'可視化呈現運算，不單獨建立因果關係。'),
'gan':('InfoGAN 的高互資訊，保證每個碼都剛好對應想要的人類概念嗎？',['保證','不保證，仍需檢查學到的變化'],1,'資訊能回推，不等於語意必然如人所願。'),
'symmetry':('模型的輸入旋轉時，輸出跟著旋轉，通常稱為什麼？',['等變','輸出一定完全不變'],0,'等變是輸出按對應方式變換；不變才是輸出保持不變。'),
'reasoning':('形式求解器跑得正確，就保證自然語言前提翻譯正確嗎？',['不保證，翻譯仍需檢查','保證'],0,'求解只相對於交入的形式表示。'),
'grounding':('任務答案正確，就一定代表中間概念辨識正確嗎？',['一定','不一定，可能走了推理捷徑'],1,'下游任務有時無法唯一辨認中間表示。'),
'meta-learning':('測新任務的適應能力時，能先看它的隱藏答案來挑方法嗎？',['可以，只要學得快','不行，這會破壞評估'],1,'保留任務必須維持評估邊界。'),
'evolution':('保留多個分支，是保證每個落後版本都會成功嗎？',['不是，它提供探索機會','是'],0,'踏腳石有機會有價值，並非每條分支都會通往好答案。'),
'arc':('只符合一張示範的規則，可以直接當成題目的唯一解釋嗎？',['不行，還要檢查其他示範與歧義','可以'],0,'少量示範可能容許多個假設，需要逐一檢查。'),
'adaptation':('測試時適應可以使用新題隱藏的正確答案嗎？',['不能，只能用允許的已知訊號','可以，這就是適應'],0,'使用隱藏答案會造成資料洩漏。'),
'automata':('兩狀態奇偶機能分辨拍了 4 次還是 400 次嗎？',['能','不能，它只保留奇偶資訊'],1,'同樣偶數次都回到偶狀態，計數資訊已被捨棄。'),
'computation':('一個局部更新規則，還需要指定邊界嗎？',['需要，邊界會改變後續行為','不需要'],0,'補零、環形或固定邊界會定義不同系統。'),
'program-search':('通過有限例子，等同對所有輸入的形式證明嗎？',['不等同','等同'],0,'測試能提供反例和證據，沒有涵蓋到的輸入仍可能失敗。'),
'library-learning':('抽出一個新函式，程式庫一定變得更省嗎？',['不一定，定義本身也有成本','一定，函式越多越好'],0,'必須計入抽象的定義、參數和使用成本。'),
}

def demo(l):
 id=l['id'];c=CATS[l['category']]
 fall=f'<p class="fallback no-js">互動需啟用 JavaScript。靜態示意：{e(l["example"]["before"])} → {e(l["example"]["after"])}</p>'
 return f'''<div class="demo" data-demo="{id}"><h3>換個條件，看看會發生什麼</h3><small>這是一個小型概念玩具，不需要下載模型。</small>{fall}<div class="js-only demo-mount"></div><p class="demo-note">教學示意 · 合成資料／手寫規則 · 非論文實驗、非模型效能比較。</p></div>'''
def quiz(l):
 q=QUIZ.get(l['id'])
 if not q:return ''
 s,opts,ans,why=q
 return f'''<div class="quiz" data-answer="{ans}" data-why="{e(why)}"><h3>帶走前，想一下</h3><p>{e(s)}</p><div>{''.join(f'<button class="secondary" data-choice="{i}">{e(o)}</button>' for i,o in enumerate(opts))}</div><p class="quiz-result" aria-live="polite">選一個答案，看看判斷理由。</p><noscript><p>參考答案：{e(opts[ans])}。{e(why)}</p></noscript></div>'''
for l in LESSONS:
 c=CATS[l['category']];id=l['id']
 steps=''.join(f'<li><span class="step-badge">{i+1}</span><strong>{e(s["title"])}</strong><p>{rich(s["text"])}</p></li>' for i,s in enumerate(l['steps']))
 details=''.join(f'<details><summary>{e(d["title"])}</summary><p>{rich(d["text"])}</p></details>' for d in l['details'])
 sources=''.join(f'''<li class="source" id="source-{s['id']}"><strong>{e(s['title'])}</strong><p>{rich(s['note'])}</p>{('<dl class="paper-takeaway"><dt>問題</dt><dd>'+rich(s['problem'])+'</dd><dt>方法</dt><dd>'+rich(s['method'])+'</dd><dt>邊界</dt><dd>'+rich(s['boundary'])+'</dd></dl>') if 'problem' in s else ''}<div class="source-links"><a href="https://arxiv.org/abs/{s['id']}">原始論文 {s['id']} ↗</a><a href="{link(s['path'])}">已讀筆記／譯文章 ↗</a></div></li>''' for s in l['sources'])
 nexts=''.join(f'''<a class="next-card" href="{x}.html"><span>接著探索 · {e(CATS[BY[x]['category']]['name'])}</span><strong>{e(BY[x]['title'])} ↗</strong></a>''' for x in l['next'] if x in BY)
 body=f'''<main id="main" class="shell" data-page-lesson="{id}" style="--topic:{c['color']}">{crumb(c,True)}<header class="lesson-header"><span class="eyebrow">{e(c['name'])} / 一次一個核心想法</span><h1>{e(l['title'])}</h1><p class="lede">{e(l['subtitle'])}</p><div class="lesson-meta"><span class="pill">主線 5–8 分鐘</span><span>{len(l['sources'])} 篇代表來源</span><span>技術細節可展開</span></div></header><div class="lesson-layout"><article class="lesson-content"><section id="intuition"><div class="question"><span class="eyebrow">THIS LESSON ASKS</span><p>{e(l['question'])}</p></div><h2>先抓住這個直覺</h2><p class="intuition">{e(l['intuition'])}</p></section><section id="picture"><span class="eyebrow">DRAW THE IDEA</span><h2>把方法畫成幾步</h2><div class="compare"><div><span class="eyebrow">看見問題</span><p>{e(l['example']['before'])}</p></div><div><span class="eyebrow">換個方式理解</span><p>{e(l['example']['after'])}</p></div></div><p class="example-note"><strong>{e(l['example']['title'])}</strong><br>{e(l['example']['explanation'])}</p><figure class="steps-diagram"><ol style="--steps:{len(l['steps'])}">{steps}</ol><figcaption>本站教學概念圖。流程將角色拆開說明；不是原論文的完整演算法或結果圖。</figcaption></figure></section><section id="try"><span class="eyebrow">MAKE ONE CHANGE</span><h2>自己動手，改一個條件</h2>{demo(l)}{quiz(l)}</section><section id="deeper"><span class="eyebrow">OPEN ONLY WHEN YOU WANT TO</span><h2>想再走深一點？</h2><p class="muted">先有輪廓就夠了。方法的細節與適用條件，可以現在讀，也可以回頭再看。</p><details><summary>研究怎麼做？把例子接回論文</summary>{''.join('<p>'+rich(p)+'</p>' for p in l['story'])}</details>{details}<details><summary>兩個容易混淆的地方</summary><div class="pitfalls"><ul>{''.join('<li>'+rich(p)+'</li>' for p in l['pitfalls'])}</ul></div></details></section><section id="sources"><span class="eyebrow">BACK TO THE EVIDENCE</span><h2>這些想法，從哪幾篇開始？</h2><p class="muted small">下方連到原始論文，以及固定快照中的已讀筆記。課程是入門導讀；教學類比與互動不代表論文曾做過的實驗。原筆記需 GitHub 權限；原論文可公開閱讀。</p><ol class="sources">{sources}</ol><p class="small"><a href="{link(c['index'])}">查看這一類的完整論文索引 ↗</a></p>{('<p class="category-note">想做更完整的公式、誤差和參數實驗？<a href="https://justty32.github.io/engineer_study/symbolic-regression/">前往符號迴歸互動實驗室 ↗</a>（另一個學習站）。</p>') if id in ['symbolic-regression','equivalence'] else ''}</section><section id="next"><h2>下一站，沿著問題走</h2><div class="next-grid">{nexts}</div><p class="small" style="margin-top:22px"><a href="../topics/{c['id']}.html">← 回到 {e(c['name'])} 課程路徑</a></p></section></article><aside class="margin-nav" aria-label="本課目錄"><strong>這一課怎麼走</strong><a href="#intuition">01 直覺與問題</a><a href="#picture">02 圖解與例子</a><a href="#try">03 動手改條件</a><a href="#deeper">04 方法與限制</a><a href="#sources">05 代表性論文</a><div class="complete"><label><input type="checkbox" data-complete="{id}">我走過這一課了</label><p class="small muted" style="margin:7px 0 0">只記在此瀏覽器，可隨時取消。</p></div></aside></div></main>'''
 write(f'lessons/{id}.html',page(l['title'],body,1,'topics',l['subtitle']))

maprows=''.join(f'''<section class="map-row"><div><span class="eyebrow">領域 {c['id'].upper()}</span><h2><a href="topics/{c['id']}.html">{e(c['name'])}</a></h2><p class="small muted">{e(c['tag'])}</p></div><div class="map-links">{''.join(f'<a href="lessons/{id}.html" data-lesson="{id}">{e(BY[id]["title"])} <span class="read-badge">✓</span></a>' for id in c['route'] if id in BY)}</div></section>''' for c in SITE['categories'])
mapbody=f'''<main id="main" class="shell"><section class="lesson-header"><span class="eyebrow">YOUR READING MAP</span><h1>一次走一小段。</h1><p class="lede">不用從頭讀到底。依你想解的問題，選一條路，或回來找下一個接點。</p><p class="small muted" id="progress-text">在課程頁勾選「走過了」，這裡會顯示你的進度。</p><div class="progress-bar" aria-hidden="true"><span id="progress-fill"></span></div></section><section class="section" style="padding-top:10px">{maprows}</section><section class="category-note"><strong>還想接著聽研究者怎麼想？</strong><p>原庫另有 Ndea 訪談的繁中摘要。這是訪談材料，與 A–J 論文分類分開；本站本輪先以研究方法的入門路徑為主。</p><a href="{link('index/video.md')}">前往訪談索引 ↗</a></section></main>'''
write('map.html',page('完整閱讀地圖',mapbody,current='map'))
about=f'''<main id="main" class="shell source-policy"><section class="lesson-header"><span class="eyebrow">ABOUT THIS FIELD GUIDE</span><h1>先懂問題，<br>再把論文讀深。</h1><p class="lede">這是一份論文閱讀庫的入門導覽，給想先看懂研究在忙什麼的人。</p></section><section class="section" style="padding-top:0"><h2>每課只帶走一個核心</h2><p>直覺與日常類比放在主線，流程圖拆解角色，互動讓你改一個條件。公式、方法差異與限制放在原生可摺疊區塊，鍵盤也能開啟。課程不是全庫逐篇摘要，也不取代閱讀論文。</p><h2>來源怎麼看？</h2><p>分類沿用 <a href="{link('index/README.md')}">paper_readings 的 A–J 索引</a>。此站依已提交的摘要與精要逐節譯文編寫，未宣稱本輪重新完整閱讀所有原始 PDF。每課列出實際依據的筆記路徑與 arXiv 原文入口；正文的論文編號可跳到來源卡。</p><p>內容快照固定於 <a href="{SITE['source_repo']}/tree/{SITE['source_commit']}">{SITE['source_commit'][:7]}</a>，日期 {SITE['snapshot_date']}。來源庫日後新增論文，不會自動改變這版課程。來源中的逐節譯文仍是閱讀筆記，關鍵定義、數字與引用請回查原文。原筆記連結需要該私有論文庫的 GitHub 存取權；arXiv 原論文入口可公開閱讀。</p><h2>圖和數字代表什麼？</h2><p>所有 SVG、流程圖與互動是本站手製教學示意，使用合成資料或手寫規則；不是論文實驗圖，也沒有在瀏覽器訓練大型模型。旋鈕改變圖形，不代表模型已學會那些因子。未列出實驗數字時，刻意不以玩具結果推斷真實效能。</p><h2>怎麼讀比較輕鬆？</h2><ol><li>讀標題底下的問題，再讀「先抓住這個直覺」。</li><li>對照圖中每一步的角色，改一次互動條件。</li><li>能說出方法做了什麼，再展開限制，挑一篇來源讀。</li></ol><h2>使用與隱私</h2><p>網站無追蹤、無登入、無後端。閱讀勾選只存在瀏覽器的 localStorage；若停用儲存，文章與互動仍可閱讀。可以在閱讀地圖使用下方按鈕清除本站的勾選，其他網站資料不受影響。</p><button class="secondary" id="clear-progress">清除本站閱讀勾選</button><p id="clear-result" class="small" aria-live="polite"></p><h2>維護方式</h2><p>這是免依賴的靜態網站。內容保存在 JSON，Python 產生 HTML；手機、鍵盤、無 JavaScript 時仍能閱讀主線與來源。<a href="map.html">回閱讀地圖，挑一個現在最有趣的問題。</a></p></section></main>'''
write('about.html',page('關於本站與來源',about,current='about'))
write('assets/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="15" fill="#172d38"/><path d="M10 35C17 8 24 9 32 35S47 60 55 28" fill="none" stroke="#d5f27c" stroke-width="6"/></svg>')
# No application fetches: this index is used solely by tooling and traceability.
write('content/catalog.json.tmp',json.dumps({'lesson_ids':list(BY)},ensure_ascii=False))
(ROOT/'content/catalog.json.tmp').unlink()
print(f'Built {len(LESSONS)} lessons + 10 topic pages + home/map/about = {len(LESSONS)+13} pages.')

"""Small, semantic SVG diagrams. All are teaching schematics, never paper figures."""
from html import escape

def svg(kind,label='',dark=False):
 c='#d5f27c' if dark else '#1b5961'; ink='#eaf1e5' if dark else '#172d38'; pale='#344d55' if dark else '#e6eadd'; hot='#e9a65a'
 def text(x,y,s,size=15,fill=ink): return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{fill}">{escape(s)}</text>'
 def rect(x,y,w,h,fill=pale,r=12): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
 def line(x,y,a,b): return f'<path d="M{x} {y} L{a} {b}" stroke="{c}" stroke-width="3" fill="none"/>'
 content=''; desc=''
 if kind in ('logic','proof'):
  desc='左側感知給出兩種候選，中間規則檢查，右側留下相容的解。'
  content=rect(15,53,92,90)+text(61,88,'看見')+text(61,118,'3？8？',19)+line(107,98,150,98)+rect(150,53,115,90)+text(207,88,'規則')+text(207,117,'x < 5',20)+line(265,98,305,98)+rect(305,53,75,90,c)+text(342,110,'3',29,'#fff' if not dark else '#172d38')
  content+=text(200,185,'辨認 → 約束 → 相容的候選',14)
 elif kind=='formula':
  desc='散點資料經過候選公式與調整常數後形成簡潔的函數。'
  content=line(30,155,170,155)+line(30,155,30,30)
  for x,y in [(48,136),(72,118),(96,94),(120,76),(145,52)]:content+=f'<circle cx="{x}" cy="{y}" r="6" fill="{hot}"/>'
  content+=f'<path d="M35 150 L156 43" stroke="{c}" stroke-width="3" fill="none"/>'+text(105,191,'觀測資料',14)+line(185,100,224,100)+rect(240,47,145,105)+text(312,93,'y = ax + b',20)+text(312,124,'結構 + 常數',13)
 elif kind=='grid':
  desc='一個L形方塊向右移一格，顏色與形狀保持不變。'
  for k,base in enumerate([25,235]):
   for r in range(4):
    for col in range(4):
     on=(r,col-k) in [(1,1),(2,1),(2,2)]
     content+=rect(base+col*31,35+r*31,27,27,hot if on else pale,3)
  content+=text(90,188,'輸入',14)+text(300,188,'向右一格',14)+line(165,95,211,95)
 elif kind=='cells':
  desc='每個格子只讀附近，反覆更新可使訊息移動。'
  for r in range(4):
   for col in range(7): content+=rect(75+col*34,25+r*36,29,29,c if col==r else pale,4)
  content+=text(200,190,'時間往下；訊息向右',14)
 elif kind=='tree':
  desc='程式語法樹：加法連接乘法子式和常數，組成2x+1。'
  for a,b,d,e in [(200,43,120,96),(200,43,280,96),(120,96,75,153),(120,96,165,153)]:content+=line(a,b,d,e)
  for x,y,s in [(200,37,'+'),(120,96,'×'),(280,96,'1'),(75,156,'2'),(165,156,'x')]: content+=f'<circle cx="{x}" cy="{y}" r="23" fill="{c if s in ["+","×"] else pale}"/>'+text(x,y+6,s,21,'#fff' if s in ['+','×'] and not dark else ink)
  content+=text(300,175,'2x + 1',20)
 elif kind=='curve':
  desc='兩個輸入分別通過邊上的一維曲線，再在輸出節點求和。'
  for yy,s in [(58,'x₁'),(155,'x₂')]:
   content+=f'<circle cx="45" cy="{yy}" r="23" fill="{pale}"/>'+text(45,yy+5,s,17)+line(70,yy,120,yy)+line(230,yy,315,105)
  content+=rect(120,21,110,70)+rect(120,119,110,70)
  content+=f'<path d="M133 75 Q160 18 215 57 M133 171 Q163 118 216 140" stroke="{c}" stroke-width="3" fill="none"/>'
  content+=f'<circle cx="340" cy="105" r="28" fill="{c}"/>'+text(340,113,'Σ',26,'#fff' if not dark else '#172d38')
 elif kind=='evolution':
  desc='多個候選接受評估後，有些被保留並繼續產生不同後代。'
  for x,y in [(50,55),(50,105),(50,155)]:content+=rect(x,y-17,70,34)+text(x+35,y+5,'候選',13)+line(x+70,y,180,105)
  content+=f'<circle cx="204" cy="105" r="31" fill="{c}"/>'+text(204,110,'評估',15,'white' if not dark else '#172d38')
  for yy,s in [(48,'改寫 A'),(107,'改寫 B'),(166,'保留 C')]:content+=line(235,105,285,yy)+rect(285,yy-20,90,40,hot if yy==107 else pale)+text(330,yy+5,s,14)
 elif kind=='gan':
  desc='生成器產出樣本，判別器比較真資料與生成樣本，再給回饋。'
  content=rect(15,70,105,65)+text(67,108,'生成器',18)+line(120,102,165,102)+rect(165,70,70,65,hot)+text(200,108,'樣本',16)+line(235,102,280,102)+rect(280,70,105,65)+text(332,108,'判別器',18)
  content+=f'<path d="M330 140 V174 H68 V140" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="6 4"/>'+text(200,194,'依回饋調整生成',13)+text(330,43,'↑ 真資料',13)
 elif kind=='agent':
  desc='智能體將目標轉為計畫，呼叫工具，取得觀測，再決定下一步。'
  for x,y,w,s in [(20,20,110,'目標'),(270,20,110,'工具'),(270,140,110,'觀測'),(20,140,110,'下一步')]:content+=rect(x,y,w,48)+text(x+w/2,y+30,s,17)
  content+=line(130,44,265,44)+line(325,70,325,135)+line(265,165,137,165)+line(75,135,75,74)
  content+=f'<circle cx="200" cy="106" r="32" fill="{c}"/>'+text(200,112,'檢查',17,'white' if not dark else '#172d38')
 else:return svg('agent',label,dark)
 return f'<svg viewBox="0 0 400 215" role="img" aria-label="{escape(label or desc)}" xmlns="http://www.w3.org/2000/svg"><title>{escape(label or desc)}</title><desc>{escape(desc)}</desc>{content}</svg>'

def home_svg():
 return '''<svg viewBox="0 0 470 330" role="img" aria-label="研究地圖：一個問題經過觀察、規則、搜尋、驗證，產生可回到論文檢查的理解" xmlns="http://www.w3.org/2000/svg"><title>從問題出發，沿研究方法走一圈</title><g stroke="#6d8587" stroke-width="2" fill="none"><path d="M100 80 Q235 10 365 80 M365 80 Q455 165 365 248 M365 248 Q230 320 100 248 M100 248 Q10 165 100 80" stroke-dasharray="7 7"/><path d="M100 80 L235 165 L365 80 M100 248 L235 165 L365 248"/></g><g fill="#344d55" stroke="#78958d"><rect x="33" y="44" width="134" height="72" rx="17"/><rect x="298" y="44" width="134" height="72" rx="17"/><rect x="33" y="212" width="134" height="72" rx="17"/><rect x="298" y="212" width="134" height="72" rx="17"/></g><g fill="#eaf1e5" text-anchor="middle" font-size="17"><text x="100" y="75">觀察資料</text><text x="100" y="99" font-size="12" fill="#bccbca">看見了什麼？</text><text x="365" y="75">提出規則</text><text x="365" y="99" font-size="12" fill="#bccbca">什麼關係成立？</text><text x="100" y="242">搜尋解法</text><text x="100" y="266" font-size="12" fill="#bccbca">還有別種可能？</text><text x="365" y="242">檢查證據</text><text x="365" y="266" font-size="12" fill="#bccbca">在哪裡會失效？</text></g><circle cx="235" cy="165" r="58" fill="#d5f27c"/><text x="235" y="161" text-anchor="middle" fill="#172d38" font-size="22" font-weight="700">一個問題</text><text x="235" y="185" text-anchor="middle" fill="#172d38" font-size="13">走進十種研究</text></svg>'''

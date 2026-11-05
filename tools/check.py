#!/usr/bin/env python3
"""Validate generated navigation, lesson contracts, citations and frozen source paths."""
import json,re,subprocess,sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlparse
ROOT=Path(__file__).resolve().parent.parent
class Doc(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.lang=None;self.titles=0;self.main=0;self.details=0;self.summary=0;self.has_alt=True
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id'in a:self.ids.append(a['id'])
  if tag=='html':self.lang=a.get('lang')
  if tag=='title':self.titles+=1
  if tag=='main':self.main+=1
  if tag=='details':self.details+=1
  if tag=='summary':self.summary+=1
  if tag in ('a','link','script','img'):
   v=a.get('href') or a.get('src')
   if v:self.links.append(v)
  if tag=='img' and 'alt'not in a:self.has_alt=False
  if tag=='svg' and a.get('role')=='img' and not a.get('aria-label'):self.has_alt=False
site=json.loads((ROOT/'content/site.json').read_text());lessons=[];errors=[]
for p in sorted((ROOT/'content').glob('*.json')):
 if p.name!='site.json':lessons+=json.loads(p.read_text())['lessons']
by={l['id']:l for l in lessons};ids=list(by)
if len(by)!=len(lessons):errors.append('duplicate lesson id')
required='id category title subtitle question intuition story steps example pitfalls details sources next'.split()
source_paths=set();papers=set()
for l in lessons:
 for field in required:
  if field not in l:errors.append(f'{l.get("id")}: missing {field}')
 if not 2<=len(l['sources'])<=4:errors.append(l['id']+': expected representative sources')
 if len(l['steps'])<3 or len(l['details'])<2:errors.append(l['id']+': incomplete teaching structure')
 sources={s['id'] for s in l['sources']};papers|=sources
 for s in l['sources']:
  source_paths.add(s['path'])
  if s['id'] not in s['path']:errors.append(l['id']+': source id/path mismatch')
 citations=re.findall(r'\[arxiv:([\d.]+)\]',json.dumps({k:v for k,v in l.items() if k!='sources'},ensure_ascii=False))
 for cid in citations:
  if cid not in sources:errors.append(l['id']+': citation missing source '+cid)
 for nxt in l['next']:
  if nxt not in by:errors.append(l['id']+': unknown next '+nxt)
 if not re.search(r'示意',l['example']['title']+l['example']['explanation']):errors.append(l['id']+': example not labelled')
 if len(''.join(l['story']))<180:errors.append(l['id']+': main text too thin')
for c in site['categories']:
 if not c['route']:errors.append(c['id']+': no learning route')
 for id in c['route']:
  if id not in by:errors.append(c['id']+': unknown lesson '+id)
  elif by[id]['category']!=c['id']:errors.append(id+': category mismatch')
htmls=list(ROOT.glob('*.html'))+list((ROOT/'topics').glob('*.html'))+list((ROOT/'lessons').glob('*.html'))
docs={}
for p in htmls:
 d=Doc();d.feed(p.read_text());docs[p.resolve()]=d
 if d.lang!='zh-Hant' or d.main!=1 or d.titles<1:errors.append(str(p)+': missing document landmarks')
 if len(d.ids)!=len(set(d.ids)):errors.append(str(p)+': duplicate ids')
 if d.details!=d.summary:errors.append(str(p)+': details/summary mismatch')
 if not d.has_alt:errors.append(str(p)+': missing image alternative')
for p,d in docs.items():
 for href in d.links:
  u=urlparse(href)
  if u.scheme or u.netloc:continue
  dest=(p.parent/unquote(u.path)).resolve() if u.path else p
  if not dest.exists():errors.append(f'{p.relative_to(ROOT)}: missing {href}')
  elif u.fragment and dest in docs and unquote(u.fragment)not in docs[dest].ids:errors.append(f'{p.relative_to(ROOT)}: missing fragment {href}')
source=ROOT.parent/'paper_readings'
if source.exists():
 for path in sorted(source_paths|{c['index'] for c in site['categories']}):
  r=subprocess.run(['git','-C',str(source),'cat-file','-e',site['source_commit']+':'+path],capture_output=True)
  if r.returncode:errors.append('frozen source missing: '+path)
else:print('NOTE: sibling source repo absent; frozen source path check skipped.')
app=(ROOT/'assets/app.js').read_text()
for id in ids:
 # Every lesson has an explicit entry in the demo registry (including identifier shorthand).
 registry=app.split('const demos={',1)[1].split('};',1)[0]
 if not re.search(r"(?:^|[,])(?:'"+re.escape(id)+r"'|"+re.escape(id)+r")(?:[:,]|$)",registry):errors.append('missing demo registry: '+id)
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(htmls)} HTML pages, {len(lessons)} lessons, 10 categories, {len(papers)} unique papers, {len(source_paths)} frozen note paths; all local links/anchors/citations valid.')

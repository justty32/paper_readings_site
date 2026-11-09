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
site=json.loads((ROOT/'content/site.json').read_text());lessons=[];guides=[];paths=[];errors=[]
for p in sorted((ROOT/'content').glob('*.json')):
 if p.name!='site.json':
  data=json.loads(p.read_text());lessons+=data.get('lessons',[]);guides+=data.get('papers',[]);paths+=data.get('paths',[])
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
for lesson in lessons:
 if 'diagrams' not in lesson:continue
 prefix=lesson['id']+': '
 if not isinstance(lesson['diagrams'],list):errors.append(prefix+'diagrams must be a list');continue
 for d in lesson['diagrams']:
  if not isinstance(d,dict):errors.append(prefix+'invalid diagram');continue
  if d.get('kind') not in ('flow','compare'):errors.append(prefix+'diagram kind must be flow or compare')
  if not isinstance(d.get('title'),str) or not d['title'].strip():errors.append(prefix+'diagram missing title')
  if not isinstance(d.get('caption'),str) or '示意' not in d['caption']:errors.append(prefix+'diagram caption must identify teaching illustration')
  if not isinstance(d.get('items'),list) or len(d['items'])<2:errors.append(prefix+'diagram needs at least two items')
  elif any(not isinstance(item,dict) or any(not isinstance(item.get(k),str) or not item[k].strip() for k in ('label','text')) for item in d['items']):errors.append(prefix+'diagram items need label and text')
  if 'image' in d:
   image=d['image']
   if not isinstance(image,str) or not re.fullmatch(r'assets/lessons/[A-Za-z0-9_-]+\.svg',image):errors.append(prefix+'diagram image must be a safe assets/lessons/*.svg path')
   elif not (ROOT/image).is_file():errors.append(prefix+'missing diagram image '+image)
for c in site['categories']:
 if not c['route']:errors.append(c['id']+': no learning route')
 for id in c['route']:
  if id not in by:errors.append(c['id']+': unknown lesson '+id)
  elif by[id]['category']!=c['id']:errors.append(id+': category mismatch')
guide_ids=set(); guide_sources=[]
categories={c['id'] for c in site['categories']}
for g in guides:
 gid=g.get('id','<missing>'); prefix='paper '+str(gid)+': '
 required='id title subtitle category arxiv_id source_path source_commit intro sections diagrams related_lessons sources'.split()
 if any(field not in g for field in required):
  errors.append(prefix+'missing required fields');continue
 if not isinstance(gid,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',gid):errors.append(prefix+'invalid id')
 if gid in guide_ids:errors.append(prefix+'duplicate id')
 guide_ids.add(gid)
 for field in ['title','subtitle','intro']:
  if not isinstance(g[field],str) or not g[field].strip():errors.append(prefix+'invalid '+field)
 if g['category'] not in categories:errors.append(prefix+'unknown category')
 if not isinstance(g['arxiv_id'],str) or not re.fullmatch(r'\d{4}\.\d{4,5}(?:v\d+)?',g['arxiv_id']):errors.append(prefix+'invalid arxiv_id')
 valid_commit=isinstance(g['source_commit'],str) and re.fullmatch(r'[0-9a-f]{40}',g['source_commit'])
 valid_path=isinstance(g['source_path'],str) and re.fullmatch(r'primers/[A-Za-z0-9_./-]+\.md',g['source_path']) and '..' not in Path(g['source_path']).parts
 if not valid_commit:errors.append(prefix+'source_commit must be a full 40-character SHA')
 if not valid_path:errors.append(prefix+'source_path must be a safe primers Markdown path')
 if valid_commit and valid_path:guide_sources.append((g['source_commit'],g['source_path']))
 if not isinstance(g['sections'],list) or len(g['sections'])<4:errors.append(prefix+'expected at least four sections')
 else:
  visible=0
  for section in g['sections']:
   if not isinstance(section,dict):errors.append(prefix+'invalid section');continue
   if not isinstance(section.get('title'),str) or not section['title'].strip():errors.append(prefix+'section missing title')
   paragraphs=section.get('paragraphs')
   if not isinstance(paragraphs,list) or not paragraphs or any(not isinstance(t,str) or not t.strip() for t in paragraphs):errors.append(prefix+'section needs nonempty text paragraphs')
   if 'code' in section and not isinstance(section['code'],str):errors.append(prefix+'code must be plain text')
   if 'collapsible' in section and not isinstance(section['collapsible'],bool):errors.append(prefix+'collapsible must be boolean')
   if not section.get('collapsible',False):visible+=1
  if visible<2:errors.append(prefix+'keep at least two sections in the visible main narrative')
 if not isinstance(g['diagrams'],list) or len(g['diagrams'])<2:errors.append(prefix+'expected at least two diagrams')
 else:
  for d in g['diagrams']:
   if not isinstance(d,dict):errors.append(prefix+'invalid diagram');continue
   if d.get('kind') not in ('flow','compare'):errors.append(prefix+'diagram kind must be flow or compare')
   if 'after_section' in d and (type(d['after_section']) is not int or not 1<=d['after_section']<=len(g['sections'])):errors.append(prefix+'diagram after_section must be a 1-based section number')
   if 'image' in d:
    image=d['image']
    if not isinstance(image,str) or not re.fullmatch(r'assets/papers/[A-Za-z0-9_-]+\.svg',image):errors.append(prefix+'diagram image must be a safe assets/papers/*.svg path')
    elif not (ROOT/image).is_file():errors.append(prefix+'missing diagram image '+image)

   if not isinstance(d.get('title'),str) or not d['title'].strip():errors.append(prefix+'diagram missing title')
   if not isinstance(d.get('caption'),str) or '示意' not in d['caption']:errors.append(prefix+'diagram caption must identify teaching illustration')
   if not isinstance(d.get('items'),list) or len(d['items'])<2:errors.append(prefix+'diagram needs at least two items')
   elif any(not isinstance(item,dict) or any(not isinstance(item.get(k),str) or not item[k].strip() for k in ('label','text')) for item in d['items']):errors.append(prefix+'diagram items need label and text')
 if not isinstance(g['related_lessons'],list) or not g['related_lessons'] or any(id not in by for id in g['related_lessons']):errors.append(prefix+'unknown or missing related lessons')
 if not isinstance(g['sources'],list) or not g['sources']:errors.append(prefix+'expected public source links')
 else:
  for source in g['sources']:
   if not isinstance(source,dict) or not isinstance(source.get('label'),str) or not source['label'].strip() or not isinstance(source.get('url'),str):errors.append(prefix+'invalid public source');continue
   url=urlparse(source['url'])
   if url.scheme!='https' or not url.netloc:errors.append(prefix+'source URL must be absolute HTTPS')
path_ids=set()
if len(paths)>3:errors.append('expected at most three reading paths')
for path in paths:
 pid=path.get('id');prefix='reading path '+str(pid)+': '
 if not isinstance(pid,str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',pid):errors.append(prefix+'invalid id');continue
 if pid in path_ids:errors.append(prefix+'duplicate id')
 path_ids.add(pid)
 for field in ('question','intro'):
  if not isinstance(path.get(field),str) or not path[field].strip():errors.append(prefix+'missing '+field)
 steps=path.get('steps')
 if not isinstance(steps,list) or not 3<=len(steps)<=5:errors.append(prefix+'expected three to five steps');continue
 seen=set()
 for step in steps:
  if not isinstance(step,dict):errors.append(prefix+'invalid step');continue
  key=(step.get('kind'),step.get('id'))
  if key in seen:errors.append(prefix+'duplicate step')
  seen.add(key)
  for target in [step]+([step['branch']] if 'branch' in step else []):
   if not isinstance(target,dict):errors.append(prefix+'invalid branch');continue
   kind=target.get('kind');tid=target.get('id')
   if kind not in ('lesson','paper') or tid not in (by if kind=='lesson' else guide_ids):errors.append(prefix+'unknown step or branch target '+str(tid))
   if not isinstance(target.get('goal'),str) or not target['goal'].strip():errors.append(prefix+'missing goal')
  if not isinstance(step.get('verb'),str) or not step['verb'].strip():errors.append(prefix+'missing step verb')
  if 'branch' in step and (not isinstance(step['branch'],dict) or not isinstance(step['branch'].get('question'),str) or not step['branch']['question'].strip()):errors.append(prefix+'missing branch question')
  for field in ('stop','transition'):
   if field in step and (not isinstance(step[field],str) or not step[field].strip()):errors.append(prefix+'invalid '+field)
htmls=list(ROOT.glob('*.html'))+list((ROOT/'topics').glob('*.html'))+list((ROOT/'lessons').glob('*.html'))+list((ROOT/'papers').glob('*.html'))
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
 for commit,path in guide_sources:
  commit_check=subprocess.run(['git','-C',str(source),'cat-file','-e',commit+'^{commit}'],capture_output=True)
  if commit_check.returncode:errors.append('paper source is not a commit: '+commit)
  r=subprocess.run(['git','-C',str(source),'cat-file','-e',commit+':'+path],capture_output=True)
  if r.returncode:errors.append('frozen paper source missing: '+commit+':'+path)
else:print('NOTE: sibling source repo absent; frozen source path check skipped.')
for gid in guide_ids:
 if not (ROOT/'papers'/f'{gid}.html').is_file():errors.append('missing dedicated paper page: '+gid)
if not (ROOT/'papers.html').is_file():errors.append('missing paper index')
app=(ROOT/'assets/app.js').read_text()
for id in ids:
 # Every lesson has an explicit entry in the demo registry (including identifier shorthand).
 registry=app.split('const demos={',1)[1].split('};',1)[0]
 if not re.search(r"(?:^|[,])(?:'"+re.escape(id)+r"'|"+re.escape(id)+r")(?:[:,]|$)",registry):errors.append('missing demo registry: '+id)
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(htmls)} HTML pages, {len(lessons)} lessons, 10 categories, {len(papers)} unique lesson papers, {len(guides)} dedicated paper guides, {len(source_paths)} frozen note paths; all local links/anchors/citations valid.')

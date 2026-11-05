import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const origin=process.env.SITE_URL||'http://127.0.0.1:8778/';
const cdp=process.env.BROWSER_CDP_URL||'http://127.0.0.1:9335';
const target=await(await fetch(cdp+'/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let seq=0;const pending=new Map(),events=[];ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}else events.push(m);};
const c=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});
const ev=async expression=>{const r=await c('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
const assert=(v,m)=>{if(!v)throw Error(m);};
await c('Page.enable');await c('Runtime.enable');await c('Log.enable');await c('Network.enable');await c('Network.setCacheDisabled',{cacheDisabled:true});
await c('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');const data=['agents','core','foundations'].flatMap(name=>JSON.parse(fs.readFileSync(root+'/content/'+name+'.json')).lessons);
const pages=['index.html','map.html','about.html',...'abcdefghij'.split('').map(x=>'topics/'+x+'.html'),...data.map(x=>'lessons/'+x.id+'.html')];
const report=[];const output=root+'/docs/qa';fs.mkdirSync(output,{recursive:true});
async function go(path,width){events.length=0;await c('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:width<700});await c('Page.navigate',{url:origin+path});for(let i=0;i<60;i++){if(await ev('document.readyState==="complete" && !!document.querySelector("main")'))break;await new Promise(r=>setTimeout(r,80));}await new Promise(r=>setTimeout(r,70));}
for(const width of [1440,390]){
 for(const p of pages){await go(p,width);const s=await ev(`({title:document.title,overflow:document.documentElement.scrollWidth>innerWidth+1,w:document.documentElement.scrollWidth,inner:innerWidth,demos:[...document.querySelectorAll('.demo-mount')].map(x=>x.children.length),errors:[...document.querySelectorAll('.demo-mount')].filter(x=>x.textContent.includes('暫時無法載入')).length})`);assert(!s.overflow,p+' overflows '+width+':'+s.w);assert(!s.errors,p+' demo error');assert(s.demos.every(n=>n>=2),p+' empty demo');const errs=events.filter(x=>x.method==='Runtime.exceptionThrown');assert(!errs.length,p+' runtime '+JSON.stringify(errs));report.push({page:p,width,status:'PASS'});
 if((width===1440&&['index.html','topics/i.html','lessons/symbolic-regression.html'].includes(p))||(width===390&&['index.html','lessons/arc.html'].includes(p))){let shot=await c('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(output+'/'+p.replaceAll('/','-').replace('.html','')+'-'+width+'.png',Buffer.from(shot.data,'base64'));}
 }
}
for(const l of data){await go('lessons/'+l.id+'.html',1000);let before=await ev(`document.querySelector('.demo-output').textContent`);assert(before.length>10,l.id+' no initial explanation');await ev(`for(const b of document.querySelectorAll('.demo button'))b.click();for(const x of document.querySelectorAll('.demo input')){if(x.type==='range')x.value=x.max;else if(x.type==='checkbox')x.checked=!x.checked;x.dispatchEvent(new Event(x.type==='checkbox'?'change':'input',{bubbles:true}));}for(const s of document.querySelectorAll('.demo select')){s.selectedIndex=s.options.length-1;s.dispatchEvent(new Event('change',{bubbles:true}));}`);let out=await ev(`document.querySelector('.demo-output').textContent`);assert(out.length>10,l.id+' interaction empty');assert(!events.filter(x=>x.method==='Runtime.exceptionThrown').length,l.id+' event error');report.push({demo:l.id,status:'PASS',output:out});}
await go('index.html',390);assert(await ev(`(()=>{let i=document.querySelector('#topic-search');i.value='長期記憶';i.dispatchEvent(new Event('input'));return [...document.querySelectorAll('.topic-card')].filter(x=>!x.hidden).length===1;})()`),'search memory');await ev(`document.querySelector('#topic-search').value='不存在xyz';document.querySelector('#topic-search').dispatchEvent(new Event('input'));`);assert(await ev(`document.querySelector('#no-results').classList.contains('visible')`),'empty state');
await go('lessons/arc.html',390);await ev(`document.querySelector('[data-complete]').click()`);await go('map.html',390);assert(await ev(`document.querySelector('[data-lesson="arc"]').classList.contains('is-read')`),'reading state');await go('about.html',390);await ev(`document.querySelector('#clear-progress').click()`);assert(await ev(`!localStorage.getItem('paper-playground-read-v1')`),'clear progress');
await go('lessons/reasoning.html',390);await ev(`document.querySelector('.quiz button').click()`);assert(await ev(`document.querySelector('.quiz-result').textContent.includes('答對了')`),'quiz');

await go('lessons/neurosymbolic.html',390);
await ev(`document.querySelector('#omit-three').click()`);assert(await ev(`document.querySelector('.demo-output').textContent.includes('無法憑空')`),'missing true candidate must not force an answer');
await ev(`document.querySelector('[data-action="ten"]').click()`);assert(await ev(`document.querySelector('.demo svg').textContent.includes('第二張是 8')`),'known sum ten must retain eight');
await go('lessons/constrained-decoding.html',390);
await ev(`document.querySelector('[data-action="valid"]').click()`);assert(await ev(`JSON.parse(document.querySelector('.demo-code').textContent).quantity===20`),'syntactically valid but semantically wrong JSON');
await ev(`document.querySelector('[data-action="correct"]').click()`);assert(await ev(`JSON.parse(document.querySelector('.demo-code').textContent).quantity===2`),'correct JSON quantity');
await go('lessons/program-search.html',390);assert(await ev(`Number(document.querySelector('#test-x').min)>3`),'heldout range excludes training inputs');
await go('lessons/workflow-optimization.html',390);assert(!(await ev(`document.querySelector('.trace').textContent.includes('→')`)),'parallel repetitions must not imply sequential dependencies');
await ev(`document.querySelector('[data-action="pipeline"]').click()`);assert(await ev(`document.querySelector('.trace').textContent.includes('→')`),'pipeline shows actual handoffs');

await go('lessons/agent-memory.html',1440);await ev(`document.querySelector('#deeper details').open=true;document.querySelector('#deeper').scrollIntoView();`);
let shot=await c('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(output+'/agent-memory-details-1440.png',Buffer.from(shot.data,'base64'));
await go('lessons/symbolic-regression.html',1440);await ev(`document.querySelector('#try').scrollIntoView();document.querySelector('[data-action="cubic"]').click();`);
shot=await c('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(output+'/symbolic-regression-interactive-1440.png',Buffer.from(shot.data,'base64'));
await go('lessons/tool-use.html',390);await ev(`document.querySelector('#try').scrollIntoView();document.querySelector('[data-action="query"]').click();`);
shot=await c('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(output+'/tool-use-interactive-390.png',Buffer.from(shot.data,'base64'));
await go('lessons/kan.html',320);assert(!(await ev(`document.documentElement.scrollWidth>innerWidth+1`)),'320px KAN overflow');
await ev(`document.querySelector('#deeper summary').focus()`);await c('Input.dispatchKeyEvent',{type:'keyDown',key:' ',code:'Space',windowsVirtualKeyCode:32});await c('Input.dispatchKeyEvent',{type:'keyUp',key:' ',code:'Space',windowsVirtualKeyCode:32});assert(await ev(`document.querySelector('#deeper details').open`),'keyboard details');
await c('Emulation.setScriptExecutionDisabled',{value:true});await go('lessons/symbolic-regression.html',390);assert(await ev(`getComputedStyle(document.querySelector('.no-js')).display!=='none' && document.querySelectorAll('details').length===4`),'no-JS fallback');await c('Emulation.setScriptExecutionDisabled',{value:false});
fs.writeFileSync(output+'/browser-report.json',JSON.stringify({date:new Date().toISOString(),base_url:origin,checks:report.length,pages:pages.length,widths:[1440,390],extra:['all demo controls','search','empty state','reading state','clear state','quiz','no-JS fallback','320px spot check','keyboard details','known constraint vs query','JSON syntax vs semantics','heldout inputs exclude training','parallel vs sequential workflow'],results:report},null,2));
console.log('PASS',pages.length,'pages x 2 widths;',data.length,'interactive lessons; search/progress/quiz/no-JS.');await c('Page.close');ws.close();

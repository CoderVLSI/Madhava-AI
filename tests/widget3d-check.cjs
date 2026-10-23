// Real-browser check: a generated 3D card runs in the sandboxed frame, loads the shipped toolkit and draws pixels.
// Needs Playwright and Chromium (PLAYWRIGHT_BROWSERS_PATH or CHROME env). Run: node tests/widget3d-check.cjs
const http=require('http'),fs=require('fs'),path=require('path'),assert=require('assert');
let chromium;try{({chromium}=require('playwright'))}catch{({chromium}=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'))}
const assets=path.resolve('app/src/main/assets');
(async()=>{
 const {widgetDocument,WIDGET_CSP}=await import('../web/widgets.js');
 const html=fs.readFileSync('tools/samples/earth-widget.html','utf8');
 const server=http.createServer((req,res)=>{
  if(req.url==='/w/doc'){res.writeHead(200,{'Content-Type':'text/html','Content-Security-Policy':'sandbox allow-scripts; default-src \'none\'; '+WIDGET_CSP.replace(/^default-src 'none'; /,'')});return res.end(widgetDocument(html))}
  if(req.url==='/widget3d.js'){res.writeHead(200,{'Content-Type':'application/javascript','Access-Control-Allow-Origin':'*'});return res.end(fs.readFileSync(path.join(assets,'widget3d.js')))}
  if(req.url==='/'){res.writeHead(200,{'Content-Type':'text/html'});return res.end('<iframe id="f" sandbox="allow-scripts" src="/w/doc" style="width:360px;height:520px;border:0"></iframe>')}
  res.writeHead(req.url==='/favicon.ico'?204:404).end()});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const exe=process.env.CHROME||(fs.existsSync('/opt/pw-browsers/chromium')?'/opt/pw-browsers/chromium':undefined);
 const browser=await chromium.launch({executablePath:exe,headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 try{
  const page=await browser.newPage({viewport:{width:380,height:560}});const errors=[];page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});
  await page.goto('http://127.0.0.1:'+server.address().port+'/');
  const frame=page.frameLocator('#f');await frame.locator('canvas').waitFor({timeout:15000});await page.waitForTimeout(1200);
  fs.mkdirSync('build',{recursive:true});await page.screenshot({path:'build/widget3d-earth.png'});
  const shot=(await page.locator('#f').screenshot()).toString('base64');
  const lit=await page.evaluate(async b=>{const im=new Image();im.src='data:image/png;base64,'+b;await im.decode();const g=document.createElement('canvas');g.width=im.width;g.height=im.height;const x=g.getContext('2d');x.drawImage(im,0,0);const d=x.getImageData(0,0,g.width,g.height).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i+1]>110&&d[i+1]>d[i]+20)n++;return n},shot);
  assert.ok(lit>3000,'the globe should paint visibly (green land pixels: '+lit+')');
  await frame.getByRole('button',{name:'Hide clouds'}).click();await frame.getByRole('button',{name:'Show clouds'}).waitFor();
  assert.deepEqual(errors,[],errors.join('\n'));
  console.log('PASS 3D card loads the toolkit in the sandbox and draws (lit pixels '+lit+')');
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exitCode=1});

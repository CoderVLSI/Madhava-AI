import http from 'node:http';
import {mkdir,appendFile} from 'node:fs/promises';
import {randomUUID,timingSafeEqual} from 'node:crypto';
import {pathToFileURL} from 'node:url';
const categories=new Set(['incorrect_scripture','offensive','unsafe','other']);
export function validateReport(x){if(!x||typeof x!=='object'||Array.isArray(x)||!categories.has(x.category)||typeof x.content!=='string'||!x.content.trim()||x.content.length>6000||typeof x.id!=='string'||! /^[a-zA-Z0-9_-]{1,80}$/.test(x.id)||(x.comment!==undefined&&(typeof x.comment!=='string'||x.comment.length>1000)))throw Error('Invalid report');return {id:x.id,category:x.category,content:x.content,comment:x.comment||'',receivedAt:new Date().toISOString(),status:'pending_review'};}
export function createServer({env=process.env,fetcher=fetch}={}){
 const buckets=new Map();const auth=env.MADHAVA_ACCESS_TOKEN||'';const secret=env.GEMINI_API_KEY||'';
 return http.createServer(async(req,res)=>{
 const finish=(status,data)=>{res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(data));};
 if(req.method==='GET'&&req.url==='/health')return finish(200,{ok:true});
 if(req.method!=='POST'||!['/v1/reports','/v1/chat','/v1/live-token'].includes(req.url))return finish(404,{error:'Not found'});
 const supplied=Buffer.from((req.headers.authorization||'').replace(/^Bearer /,'')),expected=Buffer.from(auth);
 if(!auth||supplied.length!==expected.length||!timingSafeEqual(supplied,expected))return finish(401,{error:'Authentication required'});
 const ip=req.socket.remoteAddress||'unknown',now=Date.now();let bucket=buckets.get(ip);if(!bucket||now-bucket.start>60000){bucket={start:now,count:0};if(buckets.size>10000)buckets.clear();buckets.set(ip,bucket);}if(++bucket.count>20)return finish(429,{error:'Rate limit exceeded'});
 if(!String(req.headers['content-type']||'').startsWith('application/json'))return finish(415,{error:'Use application/json'});
 let body='';try{for await(const chunk of req){body+=chunk.toString();if(Buffer.byteLength(body)>40000){finish(413,{error:'Request too large'});req.destroy();return;}}}catch{return;}
 let x;try{x=JSON.parse(body);}catch{return finish(400,{error:'Invalid JSON'});}
 if(req.url==='/v1/reports'){let report;try{report=validateReport(x);}catch{return finish(400,{error:'Invalid report'});}try{const dir=env.REPORT_DIR||'./private-reports';await mkdir(dir,{recursive:true,mode:0o700});await appendFile(dir+'/reports.jsonl',JSON.stringify(report)+'\n',{mode:0o600});return finish(202,{id:report.id,status:'pending_review'});}catch{return finish(503,{error:'Report storage unavailable'});}}
 if(!secret)return finish(503,{error:'AI service not configured'});
 let url,payload;
 if(req.url==='/v1/chat'){
 if(!Array.isArray(x.messages)||x.messages.length<1||x.messages.length>30||x.messages.some(m=>!m||!['user','assistant'].includes(m.role)||typeof m.text!=='string'||m.text.length>6000))return finish(400,{error:'Invalid messages'});
 const model=env.GEMINI_TEXT_MODEL||'gemini-3.8-flash';url=`https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent`;
 payload={contents:x.messages.map(m=>({role:m.role==='assistant'?'model':'user',parts:[{text:m.text}]})),systemInstruction:{parts:[{text:'You are a disclosed AI devotional portrayal of Krishna. Be compassionate and honest about AI identity. Never invent scripture or divine commands. Without supplied reviewed source passages, explain as a paraphrase and do not claim exact verse quotations.'}]},generationConfig:{maxOutputTokens:1024}};
 }else{
 if(x.language!==undefined&&!['Auto','English','Hindi','Telugu'].includes(x.language))return finish(400,{error:'Invalid language'});
 url='https://generativelanguage.googleapis.com/v1alpha/auth_tokens';payload={uses:1,newSessionExpireTime:new Date(now+60000).toISOString(),expireTime:new Date(now+5*60000).toISOString(),liveConnectConstraints:{model:env.GEMINI_LIVE_MODEL||'gemini-3.8-live',config:{responseModalities:['AUDIO'],systemInstruction:{parts:[{text:'You are a disclosed AI devotional portrayal of Krishna. Be compassionate, do not invent scripture, and be honest about AI identity.'+(x.language&&x.language!=='Auto'?` Prefer ${x.language}.`:'')}]}}}};
 }
 try{const upstream=await fetcher(url,{method:'POST',headers:{'Content-Type':'application/json','x-goog-api-key':secret},body:JSON.stringify(payload),signal:AbortSignal.timeout(30000)});if(!upstream.ok)return finish(upstream.status===429?429:502,{error:'AI service unavailable'});const data=await upstream.json();if(req.url==='/v1/live-token'){if(typeof data.name!=='string')return finish(502,{error:'Invalid token response'});return finish(200,{token:data.name,model:env.GEMINI_LIVE_MODEL||'gemini-3.8-live',expiresAt:payload.expireTime});}const text=(data.candidates?.[0]?.content?.parts||[]).filter(p=>!p.thought).map(p=>p.text||'').join('');return finish(200,{id:randomUUID(),text,model:env.GEMINI_TEXT_MODEL||'gemini-3.8-flash'});}catch{return finish(502,{error:'AI service unavailable'});}
 });
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){if(!process.env.MADHAVA_ACCESS_TOKEN)throw Error('Set MADHAVA_ACCESS_TOKEN; never embed it in the public app');createServer().listen(Number(process.env.PORT)||8080,'127.0.0.1',()=>console.log('Madhava development server listening on loopback'));}

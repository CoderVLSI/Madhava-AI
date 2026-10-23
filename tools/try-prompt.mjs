// Dev tool: send a prompt through the app's real Krishna persona and see whether Gemini adds an interactive widget.
// The key is read from your own environment, never written anywhere.
//   PowerShell:  $env:GEMINI_API_KEY="your-key"; node tools/try-prompt.mjs "Explain the Kathopanishad"
//   bash:        GEMINI_API_KEY=your-key node tools/try-prompt.mjs "Explain the Kathopanishad"
import {mkdirSync,writeFileSync} from 'node:fs';
import {generate,TEXT_MODELS} from '../web/core.js';
import {extractWidget,widgetDocument} from '../web/widgets.js';
const key=process.env.GEMINI_API_KEY;
const prompt=process.argv.slice(2).join(' ').trim();
if(!key||!prompt){console.error('Usage: GEMINI_API_KEY=... node tools/try-prompt.mjs "your question"');process.exit(1)}
const out=new URL('./last-run/',import.meta.url);mkdirSync(out,{recursive:true});
const started=Date.now();
const result=await generate({key,models:TEXT_MODELS,history:[{role:'user',text:prompt}],onFallback:m=>console.error('falling back to',m)});
const {text,widget}=extractWidget(result.text);
writeFileSync(new URL('reply.txt',out),result.text);
console.log(`model: ${result.model}   time: ${((Date.now()-started)/1000).toFixed(1)}s   raw length: ${result.text.length}`);
console.log('\n--- Krishna says ---\n'+text);
if(widget){writeFileSync(new URL('widget.html',out),widgetDocument(widget.html));console.log(`\n--- WIDGET: "${widget.title}" (${widget.html.length} chars) ---\nSaved to tools/last-run/widget.html`)}
else console.log(result.text.toLowerCase().includes('<madhava-widget')?'\n--- A widget block was present but rejected or cut off (see tools/last-run/reply.txt) ---':'\n--- No widget in this reply ---');

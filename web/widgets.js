// Interactive explanations: Gemini writes HTML/CSS/JS, the app runs it in a locked-down, network-less, sandboxed frame.
export const WIDGET_MAX=100000;
const OPEN='<madhava-widget',CLOSE='</madhava-widget>';
export const WIDGET_CSP="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; media-src data:; font-src data:; connect-src 'none'; frame-src 'none'; form-action 'none'; base-uri 'none'";
// Anything that could reach the native bridge or embed other content is refused outright.
export function isSafeWidgetHtml(html){return typeof html==='string'&&html.trim().length>20&&html.length<=WIDGET_MAX&&!/android\s*[.\[]|window\s*\[|<\s*(iframe|object|embed|frame)\b/i.test(html)}
export function extractWidget(raw){
 let text=String(raw||'');
 text=text.replace(/```(?:html)?\s*(<madhava-widget[\s\S]*?<\/madhava-widget>)\s*```/gi,'$1');
 const start=text.toLowerCase().indexOf(OPEN);
 if(start<0)return {text:text.trim(),widget:null};
 const end=text.toLowerCase().indexOf(CLOSE,start);
 if(end<0)return {text:text.slice(0,start).trim(),widget:null}; // truncated output: drop the unfinished block
 const block=text.slice(start,end+CLOSE.length);
 const m=block.match(/^<madhava-widget(?:\s+title\s*=\s*"([^"]{0,80})")?\s*>([\s\S]*)<\/madhava-widget>$/i);
 const rest=(text.slice(0,start)+text.slice(end+CLOSE.length)).replace(/\n{3,}/g,'\n\n').trim();
 if(!m||!isSafeWidgetHtml(m[2]))return {text:rest,widget:null};
 return {text:rest,widget:{title:(m[1]||'Interactive explanation').trim()||'Interactive explanation',html:m[2].trim()}};
}
const BASE=`:root{--bg:#141d38;--surface:#1c2749;--surface2:#27335a;--text:#efe4cb;--muted:#9aa7c7;--gold:#f0a63a;--teal:#1b8a89;--lotus:#d4607f;--line:#27335a;--serif:'Iowan Old Style','Noto Serif','Palatino Linotype',Georgia,serif;--sans:system-ui,-apple-system,'Segoe UI','Noto Sans',Roboto,sans-serif;color-scheme:dark}*{box-sizing:border-box}html,body{margin:0}body{background:var(--bg);color:var(--text);font:16px/1.55 var(--sans);padding:16px;overflow-x:hidden}h1,h2,h3{font-family:var(--serif);font-weight:600;margin:0 0 .5em;line-height:1.25}h1{font-size:22px}h2{font-size:19px}h3{font-size:17px}p{margin:0 0 .8em}button{font:inherit;min-height:44px;padding:10px 16px;border-radius:12px;border:1px solid var(--gold);background:var(--gold);color:#141d38;font-weight:700;cursor:pointer}button.ghost{background:transparent;color:var(--text);border-color:var(--line)}input[type=range]{width:100%;accent-color:var(--gold)}svg{max-width:100%;height:auto}.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px}@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}`;
const BOOT=`(function(){function post(){try{parent.postMessage({madhavaWidgetHeight:Math.ceil(document.documentElement.scrollHeight)},'*')}catch(e){}}try{new ResizeObserver(post).observe(document.body)}catch(e){}addEventListener('load',post);post()})()`;
export function widgetDocument(html){return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="${WIDGET_CSP}"><style>${BASE}</style></head><body>${html}<script>${BOOT}</script></body></html>`}

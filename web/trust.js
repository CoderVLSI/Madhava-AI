import {safeJSON} from './core.js';
const $=id=>document.getElementById(id);
export function makeReport(content,category,comment=''){
 if(!['Incorrect scripture','Harmful or offensive','Privacy concern','Other'].includes(category))throw Error('Choose a report category.');
 return {id:globalThis.crypto?.randomUUID?.()||`report-${Date.now()}-${Math.random().toString(36).slice(2)}`,category,content:String(content).slice(0,16000),comment:String(comment).slice(0,2000),createdAt:new Date().toISOString(),status:'local draft — not submitted'};
}
export function initTrust({toast,onDelete}){
 let content='';
 function close(id){$(id).close()}
 $('onboardingContinue').onclick=()=>{if(!$('onboardingConsent').checked)return toast('Please read and acknowledge how AI conversations work.');localStorage.setItem('onboardingVersion','1');close('onboardingDialog')};
 $('onboardingDialog').oncancel=e=>e.preventDefault();
 if(localStorage.getItem('onboardingVersion')!=='1')$('onboardingDialog').showModal();
 $('openPrivacy').onclick=()=>$('privacyDialog').showModal();$('closePrivacy').onclick=()=>close('privacyDialog');
 $('deleteAll').onclick=onDelete;
 $('closeSources').onclick=()=>close('sourcesDialog');
 $('closeReport').onclick=()=>close('reportDialog');
 $('saveReport').onclick=()=>{try{const r=makeReport(content,$('reportCategory').value,$('reportComment').value),reports=safeJSON(localStorage.getItem('reports'),[]);localStorage.setItem('reports',JSON.stringify([...reports,r].slice(-50)));close('reportDialog');toast('Report draft saved on this device. It has not been submitted.')}catch(e){toast(e.message)}};
 $('viewReports').onclick=()=>{$('reportExport').value=JSON.stringify(safeJSON(localStorage.getItem('reports'),[]),null,2);$('reportsDialog').showModal()};$('closeReports').onclick=()=>close('reportsDialog');
 $('copyReports').onclick=async()=>{try{await navigator.clipboard.writeText($('reportExport').value);toast('Report drafts copied.')}catch{$('reportExport').focus();$('reportExport').select();toast('Press and hold the selected text to copy.')}};
 return {
 report(text){content=text;$('reportComment').value='';$('reportDialog').showModal()},
 sources(records){const list=$('sourceRecords');list.replaceChildren();for(const r of records){const card=document.createElement('article');card.className='sourceRecord';for(const [tag,value]of [['h3',r.reference],['small',`${r.type} · Speaker: ${r.speaker||'See source'}`],['p',r.sanskrit||r.text],['p',r.transliteration],['p',r.readingAid?'Reading aid — original paraphrase, not a literal translation: '+r.readingAid.text:''],['small',typeof r.source==='string'?r.source:JSON.stringify(r.source)]]){if(!value)continue;const el=document.createElement(tag);el.textContent=value;card.append(el)}list.append(card)}$('sourcesDialog').showModal()}
 };
}

import corpus from './gita-data.json' with {type:'json'};
import {lookupGita} from './gita.js';
const BOOKMARK_KEY='madhava-study-bookmarks-v1';
const JOURNAL_KEY='madhava-reflection-v1';
const dailyIds=['2.47','2.48','6.26','12.13','17.15','6.17','18.63','6.32','3.19','4.34','9.26','6.5'];
const prompts=['What action can I give my full attention to today, without trying to control its outcome?','How can I meet one success or setback with steadiness?','When my attention wanders today, what will help me gently return?','What is one practical act of kindness I can offer today?','Can I make one difficult conversation truthful, helpful and gentle?','What small adjustment would bring more balance to my daily routine?','What choice deserves a little more reflection before I act?','Whose experience can I try to understand more carefully today?','What useful work can I do with less attachment to praise?','What sincere question would I like to ask a trusted teacher?','What simple offering can I make with care today?','What small step would help me support myself today?'];
export function chapterVerses(chapter){return corpus.verses.filter(v=>v.chapter===Number(chapter));}
export function getStudyVerse(id){if(!/^\d{1,2}\.\d{1,2}$/.test(String(id)))return null;return lookupGita(id,1).results[0]||null;}
export function dailyReflection(date=new Date()){
 const day=Math.floor(Date.UTC(date.getFullYear(),date.getMonth(),date.getDate())/86400000);
 const index=((day%dailyIds.length)+dailyIds.length)%dailyIds.length;
 return {id:dailyIds[index],prompt:prompts[index],date:[date.getFullYear(),String(date.getMonth()+1).padStart(2,'0'),String(date.getDate()).padStart(2,'0')].join('-')};
}
export function readBookmarks(storage){try{const data=JSON.parse(storage.getItem(BOOKMARK_KEY)||'[]');return Array.isArray(data)?[...new Set(data.filter(id=>typeof id==='string'&&getStudyVerse(id)))].slice(0,701):[];}catch{return [];}}
export function toggleBookmark(storage,id){if(!getStudyVerse(id))throw Error('Unknown verse');const ids=readBookmarks(storage);const next=ids.includes(id)?ids.filter(x=>x!==id):[...ids,id];storage.setItem(BOOKMARK_KEY,JSON.stringify(next));return next;}
export function initStudy({toast=()=>{},storage=globalThis.localStorage}={}){
 const el=id=>document.getElementById(id);
 const chapter=el('studyChapter'),verse=el('studyVerse');
 if(!chapter||!verse)return;
 let current='2.47';
 const daily=dailyReflection();
 const option=(value,label)=>{const o=document.createElement('option');o.value=String(value);o.textContent=label;return o;};
 chapter.replaceChildren(...Array.from({length:18},(_,i)=>option(i+1,'Chapter '+(i+1))));
 const text=(id,value)=>{if(el(id))el(id).textContent=value;};
 const bookmarks=()=>{const list=el('studyBookmarks');if(!list)return;list.replaceChildren();const ids=readBookmarks(storage);if(!ids.length){list.textContent='No bookmarks yet. Save a verse to return to it.';return;}for(const id of ids){const button=document.createElement('button');button.type='button';button.textContent='Gita '+id;button.addEventListener('click',()=>show(id));list.append(button);}};
 const render=()=>{const record=getStudyVerse(current);if(!record)return;text('studyReference',record.reference);text('studySpeaker','Speaker: '+record.speaker);text('studySanskrit',record.sanskrit);text('studyTransliteration',record.transliteration);text('studyAid',record.readingAid?.text||'No authored reading aid is available for this verse. The Sanskrit and transliteration above are the source text.');text('studyAidLabel',record.readingAid?'Authored paraphrase · not a literal translation':'Reading aid');text('studySourceNote',corpus.sources.note);const source=el('studySource');if(source){source.href=record.source;source.textContent='Sanskrit source and edition';}const button=el('studyBookmark');if(button){const saved=readBookmarks(storage).includes(current);button.textContent=saved?'Remove bookmark':'Bookmark verse';button.setAttribute('aria-pressed',String(saved));}bookmarks();};
 const show=id=>{const record=getStudyVerse(id);if(!record)return;current=id;chapter.value=String(record.chapter);verse.replaceChildren(...chapterVerses(record.chapter).map(v=>option(v.verse,'Verse '+v.verse)));verse.value=String(record.verse);render();};
 chapter.addEventListener('change',()=>show(chapter.value+'.'+chapterVerses(chapter.value)[0].verse));
 verse.addEventListener('change',()=>show(chapter.value+'.'+verse.value));
 el('studyBookmark')?.addEventListener('click',()=>{try{toggleBookmark(storage,current);render();}catch{toast('Could not save this bookmark on your device.');}});
 text('reflectionReference','Bhagavad Gita '+daily.id);text('reflectionPrompt',daily.prompt);
 text('reflectionAid',getStudyVerse(daily.id)?.readingAid?.text||'');
 el('reflectionRead')?.addEventListener('click',()=>show(daily.id));
 const journal=el('reflectionJournal');
 if(journal){try{const saved=JSON.parse(storage.getItem(JOURNAL_KEY)||'{}');journal.value=saved.date===daily.date&&typeof saved.text==='string'?saved.text:'';}catch{journal.value='';}}
 el('reflectionSave')?.addEventListener('click',()=>{try{storage.setItem(JOURNAL_KEY,JSON.stringify({date:daily.date,text:(journal?.value||'').slice(0,5000)}));toast('Reflection saved on this device.');}catch{toast('Could not save your reflection on this device.');}});
 el('reflectionDelete')?.addEventListener('click',()=>{try{storage.removeItem(JOURNAL_KEY);if(journal)journal.value='';toast('Reflection deleted.');}catch{toast('Could not delete the saved reflection.');}});
 show(current);
 return {show,refresh:render};
}

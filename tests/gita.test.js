import assert from 'node:assert/strict';
import {lookupGita,GITA_META} from '../web/gita.js';
import {generate,LiveClient,PERSONA} from '../web/core.js';
assert.equal(GITA_META.chapters,18);assert.equal(GITA_META.verses,701);
const exact=lookupGita('Bhagavad Gita 2.47');assert.equal(exact.results[0].verse,47);assert.ok(exact.results[0].sanskrit.includes('कर्मण्येवाधिकारस्ते'));
assert.equal(lookupGita('99.99').results.length,0);
assert.ok(lookupGita('work duty results anxiety').results.some(x=>x.verse===47&&x.chapter===2));
assert.ok(lookupGita('నాకు కోపం వస్తుంది').results.some(x=>['2.63','16.21'].some(id=>x.reference.endsWith(id))));
assert.ok(lookupGita('restless mind practice detachment').results.some(x=>x.reference.endsWith('6.35')));
assert.ok(lookupGita('surrender refuge').results.some(x=>x.reference.endsWith('18.66')));
for(const p of lookupGita('battle army war').results.filter(x=>x.type.startsWith('English'))){assert.equal(p.verse,undefined);assert.ok(p.reference.includes('chapter'))}
assert.ok(PERSONA.includes('FIRST PERSON'));assert.ok(PERSONA.includes('briefly and honestly'));
let body;const r=await generate({key:'fake',models:['test'],history:[{role:'user',text:'Explain Gita 2.47'}],fetcher:async(u,o)=>{body=JSON.parse(o.body);return {ok:true,json:async()=>({candidates:[{content:{parts:[{text:'Test grounded response'}]}}]})}}});assert.ok(body.systemInstruction.parts[0].text.includes('कर्मण्येवाधिकारस्ते'));assert.equal(r.gita[0].verse,47);
class WS{constructor(){this.readyState=1;this.bufferedAmount=0;this.sent=[]}send(s){this.sent.push(JSON.parse(s))}close(){this.readyState=3}}
let grounded;const c=new LiveClient({key:'fake',models:['test'],WebSocketClass:WS,callbacks:{onGrounding:r=>grounded=r}});c.start();c.ws.onopen();assert.equal(c.ws.sent[0].setup.tools[0].functionDeclarations[0].name,'lookup_gita');c.receive({setupComplete:{}});c.receive({toolCall:{functionCalls:[{id:'g1',name:'lookup_gita',args:{query:'6.35'}}]}});const reply=c.ws.sent.at(-1).toolResponse.functionResponses[0];assert.equal(reply.id,'g1');assert.equal(reply.response.results[0].verse,35);assert.equal(grounded.results[0].chapter,6);let form;c.callbacks.onAvatarForm=f=>form=f;c.receive({toolCall:{functionCalls:[{id:'v1',name:'set_avatar_form',args:{form:'vishwaroopa'}}]}});assert.equal(form,'vishwaroopa');assert.equal(c.ws.sent.at(-1).toolResponse.functionResponses[0].id,'v1');c.receive({toolCall:{functionCalls:[{id:'v2',name:'set_avatar_form',args:{form:'invalid'}}]}});assert.equal(form,'vishwaroopa');assert.ok(c.ws.sent.at(-1).toolResponse.functionResponses[0].response.error);c.stop();
console.log('PASS 701-verse corpus, exact/invalid references, English & Telugu topic retrieval, source distinctions, REST grounding and Live tool roundtrip.');

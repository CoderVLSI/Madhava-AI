import assert from 'node:assert/strict';
import fs from 'node:fs';
import {Box3,Vector3} from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {FORM_IDS,FORMS,requestedForm} from '../web/forms.js';
import {Avatar} from '../web/avatar.js';
import {LiveClient} from '../web/core.js';
assert.equal(FORM_IDS.length,11);assert.equal(new Set(FORM_IDS).size,11);
for(const f of FORMS)assert.equal(requestedForm('Show me '+f.name),f.id);
assert.equal(requestedForm('నరసింహ రూపం చూపించు'),'narasimha');assert.equal(requestedForm('राम रूप दिखाओ'),'rama');assert.equal(requestedForm('Show Parashurama'),'parashurama');assert.equal(requestedForm('Tell me about Rama'),null);assert.equal(requestedForm("Don't show Kalki"),null);
globalThis.self??=globalThis;
const quiet=(f)=>{const w=console.warn,e=console.error;console.warn=console.error=()=>{};return f().finally(()=>{console.warn=w;console.error=e})};
for(const id of FORM_IDS.filter(x=>x!=='krishna')){const b=fs.readFileSync(new URL('../app/src/main/assets/forms/'+id+'.glb',import.meta.url));const g=await quiet(()=>new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),''));let meshes=0,talk=false;g.scene.traverse(o=>{if(o.isMesh){meshes++;assert.ok(o.geometry.attributes.position.count>0,id)}if(o.morphTargetDictionary?.Talk!==undefined)talk=true});assert.ok(meshes>=1,id);assert.ok(talk,id+' has a Talk morph');assert.ok(new Box3().setFromObject(g.scene).getSize(new Vector3()).y>1,id)}
class WS{constructor(){this.readyState=1;this.sent=[]}send(s){this.sent.push(JSON.parse(s))}close(){}}
let done;const c=new LiveClient({key:'fake',models:['test'],WebSocketClass:WS,callbacks:{onAvatarForm:()=>new Promise(r=>done=r)}});c.start();c.receive({setupComplete:{}});const p=c.receive({toolCall:{functionCalls:[{id:'n',name:'set_avatar_form',args:{form:'narasimha'}}]}});assert.equal(c.ws.sent.length,0);done();await p;assert.equal(c.ws.sent.at(-1).toolResponse.functionResponses[0].response.status,'displayed');c.callbacks.onAvatarForm=()=>Promise.reject(Error('Asset missing'));await c.receive({toolCall:{functionCalls:[{id:'k',name:'set_avatar_form',args:{form:'kalki'}}]}});assert.ok(c.ws.sent.at(-1).toolResponse.functionResponses[0].response.error);c.stop();console.log('PASS 11 form requests, Telugu/Hindi aliases, all 9 new GLBs and awaited Live display success/failure');

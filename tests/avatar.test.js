import assert from 'node:assert/strict';
import fs from 'node:fs';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {Avatar} from '../web/avatar.js';
globalThis.self??=globalThis;
const warn=console.warn,err=console.error;console.warn=console.error=()=>{}; // node cannot decode embedded textures
const bytes=fs.readFileSync(new URL('../app/src/main/assets/Imported-Krishna.glb',import.meta.url));
const g=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'');
console.warn=warn;console.error=err;
const a=new Avatar({});a.root=g.scene;a.bindRig();
assert.ok(a.morphs.length>0,'Krishna has a morph-target face mesh');assert.ok(a.morphs.some(m=>m.morphTargetDictionary.Talk!==undefined),'Talk morph');
assert.ok(Object.keys(a.joints).length>0,'Krishna keeps head/arm rig joints');
a.level=0;a.animate(.016);const talk=m=>m.morphTargetInfluences[m.morphTargetDictionary.Talk];const m0=a.morphs.find(m=>m.morphTargetDictionary.Talk!==undefined);const closed=talk(m0);
a.level=.13;for(let i=0;i<60;i++)a.animate(1/60);assert.ok(talk(m0)>closed+.3,'audio level opens the mouth');
a.level=0;for(let i=0;i<90;i++)a.animate(1/60);assert.ok(a.energy<.001);assert.ok(talk(m0)<.05,'mouth closes in silence');
a.hide();assert.equal(a.active,false);for(const m of a.morphs)assert.ok(m.morphTargetInfluences.every(v=>v===0));
console.log('PASS Imported-Krishna morph/rig articulation, audio-driven talk, silence decay and hide reset');

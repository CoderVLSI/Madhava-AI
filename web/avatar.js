import {FORM_IDS} from './forms.js';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
export class Avatar{
 constructor(el){this.el=el;this.active=false;this.level=0;this.drag=0;this.eyes=[];this.joints={};this.state='listening';this.form='krishna';this.energy=0;this.last=0;this.blinkAt=3;this.blinkStart=-10;this.time=0;this.models=new Map();this.formEpoch=0;this.q=new THREE.Quaternion();this.euler=new THREE.Euler()}
 async init(){if(this.loading)return this.loading;this.loading=this.load();try{await this.loading}catch(e){this.loading=null;this.renderer?.dispose();this.renderer?.domElement.remove();this.renderer=null;throw e}}
 async load(){
  this.renderer=new THREE.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'});this.renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));this.renderer.outputColorSpace=THREE.SRGBColorSpace;this.renderer.toneMapping=THREE.ACESFilmicToneMapping;this.renderer.toneMappingExposure=1.6;this.el.appendChild(this.renderer.domElement);
  this.scene=new THREE.Scene();this.scene.add(new THREE.HemisphereLight(0xf8f1d9,0x344d3d,2.6));const k=new THREE.DirectionalLight(0xffedcf,4);k.position.set(-3,6,5);this.scene.add(k);const rim=new THREE.DirectionalLight(0xc8dfcf,2.3);rim.position.set(3,4,-2);this.scene.add(rim);
  const positions=[];for(let i=0;i<220;i++)positions.push((Math.random()-.5)*9,Math.random()*6,-1.3-Math.random()*2);const stars=new THREE.BufferGeometry();stars.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));this.stars=new THREE.Points(stars,new THREE.PointsMaterial({color:0xffdca0,size:.023,transparent:true,opacity:.7}));this.stars.visible=false;this.scene.add(this.stars);
  this.camera=new THREE.PerspectiveCamera(35,1,.1,50);this.camera.position.set(0,2.4,7.5);this.camera.lookAt(0,2.05,0);
  const gltf=await new GLTFLoader().loadAsync('Krishna-dialogue.glb');this.root=gltf.scene;this.normal=this.root;this.scene.add(this.root);
  this.root.traverse(o=>{if(/^Rig_(Head|Left_|Right_)/.test(o.name)&&!o.isMesh)this.joints[o.name]={o,q:(o.userData.restQuaternion ||=o.quaternion.clone()).clone()};if(o.name==='Cosmic_Form')this.cosmic=o;if(o.name==='Rig_Flute')this.flute=o;if(o.name==='Rig_MouthOpen')this.mouth=[o,(o.userData.restScale ||=o.scale.clone()).clone()];if(o.isMesh&&(o.name.startsWith('Eye_ivory')||o.name.startsWith('Iris')))this.eyes.push([o,(o.userData.restScale ||=o.scale.clone()).clone()])});this.setForm(this.form);
  new ResizeObserver(()=>this.resize()).observe(this.el);this.resize();let down=false,start=0,base=0;
  this.el.onpointerdown=e=>{down=true;start=e.clientX;base=this.drag;this.el.setPointerCapture(e.pointerId)};this.el.onpointermove=e=>{if(down)this.drag=Math.max(-.65,Math.min(.65,base+(e.clientX-start)*.005))};this.el.onpointerup=this.el.onpointercancel=()=>down=false;
  const loop=t=>{this.frame=requestAnimationFrame(loop);const dt=Math.min((t-this.last)/1000,.05);this.last=t;if(!this.active)return;this.animate(dt);this.renderer.render(this.scene,this.camera)};this.frame=requestAnimationFrame(loop)
 }
 joint(name,x,y,z){const j=this.joints[name];if(j){this.euler.set(x,y,z);j.o.quaternion.copy(j.q).multiply(this.q.setFromEuler(this.euler))}}
 animate(dt){this.time+=dt;const s=this.time;const target=Math.min(1,this.level*8);this.energy+=(target-this.energy)*(1-Math.exp(-dt*(target>this.energy?24:12)));const a=this.energy;
  this.root.rotation.y=this.drag+Math.sin(s*.37)*.018;this.root.position.y=Math.sin(s*1.3)*.004;
  this.joint('Rig_Head',Math.sin(s*.83)*.017+a*Math.sin(s*2.1)*.032,Math.sin(s*.43)*.035,Math.sin(s*.61)*.018+a*.016);
  this.joint('Rig_Right_Upper',.009*Math.sin(s*.7)+a*.018,Math.sin(s*.53)*.006,a*.012);
  this.joint('Rig_Right_Fore',a*.008*Math.sin(s*1.6),a*.008,Math.sin(s*.65)*.005);
  this.joint('Rig_Right_Hand',.005*Math.sin(s*.9)+a*.008*Math.sin(s*2),a*.006,.005*Math.sin(s*.7));
  this.joint('Rig_Left_Upper',Math.sin(s*.6)*.006,a*.006,-a*.008);this.joint('Rig_Left_Fore',a*.008,0,a*.006);this.joint('Rig_Left_Hand',Math.sin(s*.9)*.005,0,a*.006);
  if(s>=this.blinkAt){this.blinkStart=s;this.blinkAt=s+3+Math.random()*4}const phase=(s-this.blinkStart)/.18;const blink=phase>=0&&phase<1?1-.93*Math.sin(phase*Math.PI):1;
  for(const[o,b]of this.eyes){o.scale.copy(b);o.scale.y*=blink}if(this.mouth){const[o,b]=this.mouth;o.scale.copy(b);o.scale.y*=this.form==='narasimha'?.32+a*.68:.055+a*.95}
 }
 setState(state){this.state=state}
 bindRig(){this.joints={};this.eyes=[];this.mouth=null;this.root.traverse(o=>{if(/^Rig_(Head|Left_|Right_)/.test(o.name)&&!o.isMesh)this.joints[o.name]={o,q:(o.userData.restQuaternion ||=o.quaternion.clone()).clone()};if(o.name==='Rig_MouthOpen')this.mouth=[o,(o.userData.restScale ||=o.scale.clone()).clone()];if(o.isMesh&&(o.name.startsWith('Eye_ivory')||o.name.startsWith('Iris')))this.eyes.push([o,(o.userData.restScale ||=o.scale.clone()).clone()])})}
 setForm(form){if(!FORM_IDS.includes(form))throw Error('Unknown form');const epoch=++this.formEpoch;
  if(form!=='krishna'&&form!=='vishwaroopa')return this.loadForm(form,epoch);
  if(this.normal&&this.root!==this.normal){this.root.visible=false;this.root=this.normal;this.root.visible=true;this.bindRig()}
  this.form=form;if(this.camera)this.camera.lookAt(0,2.05,0);if(this.cosmic)this.cosmic.visible=form==='vishwaroopa';if(this.flute)this.flute.visible=form==='krishna';if(this.stars)this.stars.visible=form==='vishwaroopa';if(this.scene)this.scene.background=form==='vishwaroopa'?new THREE.Color(0x07132f):null;this.resize();
 }
 async loadForm(form,epoch){if(!this.scene)throw Error('Avatar is not ready');if(!this.models.has(form))this.models.set(form,new GLTFLoader().loadAsync('forms/'+form+'.glb').then(g=>{g.scene.visible=false;this.scene.add(g.scene);return g.scene}).catch(e=>{this.models.delete(form);throw e}));const model=await this.models.get(form);if(epoch!==this.formEpoch)throw Error('Form change superseded');this.root.visible=false;this.root=model;model.visible=true;this.form=form;this.bindRig();const bounds=new THREE.Box3().setFromObject(model);this.formCenter=bounds.getCenter(new THREE.Vector3()).y;this.camera.lookAt(0,this.formCenter,0);if(this.stars)this.stars.visible=false;this.scene.background=['matsya','kurma'].includes(form)?new THREE.Color(0x062a37):null;this.resize();}

 resize(){if(!this.renderer||!this.camera)return;const w=this.el.clientWidth,h=this.el.clientHeight;if(!w||!h)return;this.renderer.setSize(w,h);this.camera.aspect=w/h;this.camera.position.z=(w/h<.6?9.2:7.7)*(this.form==='vishwaroopa'?1.55:1);this.camera.updateProjectionMatrix()}
 show(){this.active=true;this.resize()}
 hide(){this.active=false;this.level=0;this.energy=0;this.setForm('krishna')}
 reset(){this.drag=0}
}

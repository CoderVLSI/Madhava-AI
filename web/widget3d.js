// 3D toolkit for sandboxed explanation cards: a classic script that gives generated code THREE and a ready-made stage.
import * as THREE from 'three';
const calm=()=>{try{return matchMedia('(prefers-reduced-motion: reduce)').matches}catch{return false}};
function stage(el,opts={}){
 const o={height:300,distance:4,spin:.25,fov:40,background:null,...opts};
 if(typeof el==='string')el=document.querySelector(el);
 const dead={ok:false,THREE,scene:null,camera:null,renderer:null,pivot:null,add(){},onFrame(){},dispose(){}};
 if(!el)return dead;
 el.style.cssText+=';position:relative;width:100%;height:'+o.height+'px;touch-action:none;overflow:hidden;border-radius:14px';
 let renderer;
 try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:o.background==null});renderer.setPixelRatio(Math.min(devicePixelRatio||1,2))}catch{
  el.textContent='3D is not available on this device. Please read the explanation instead.';el.style.cssText+=';display:flex;align-items:center;justify-content:center;text-align:center;padding:16px';return dead}
 renderer.outputColorSpace=THREE.SRGBColorSpace;
 const canvas=renderer.domElement;canvas.style.cssText='display:block;width:100%;height:100%';el.append(canvas);
 const scene=new THREE.Scene();if(o.background!=null)scene.background=new THREE.Color(o.background);
 const camera=new THREE.PerspectiveCamera(o.fov,1,.05,100);
 scene.add(new THREE.HemisphereLight(0xffffff,0x334455,1.1));
 const sun=new THREE.DirectionalLight(0xfff1d6,2.6);sun.position.set(-3,4,5);scene.add(sun);
 const pivot=new THREE.Group();scene.add(pivot);
 let dist=o.distance,yaw=0,pitch=0,held=false,px=0,py=0,idle=0;
 const place=()=>{camera.position.set(0,0,dist);camera.lookAt(0,0,0)};place();
 const size=()=>{const w=Math.max(1,el.clientWidth),h=Math.max(1,el.clientHeight);renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix()};
 try{new ResizeObserver(size).observe(el)}catch{}size();
 canvas.addEventListener('pointerdown',e=>{held=true;px=e.clientX;py=e.clientY;try{canvas.setPointerCapture(e.pointerId)}catch{}});
 canvas.addEventListener('pointermove',e=>{if(!held)return;yaw+=(e.clientX-px)*.01;pitch=Math.max(-1.2,Math.min(1.2,pitch+(e.clientY-py)*.01));px=e.clientX;py=e.clientY;idle=0});
 const up=()=>{held=false};canvas.addEventListener('pointerup',up);canvas.addEventListener('pointercancel',up);
 canvas.addEventListener('wheel',e=>{e.preventDefault();dist=Math.max(o.distance*.5,Math.min(o.distance*2,dist*(1+e.deltaY*.001)));place()},{passive:false});
 const frames=[];let last=performance.now(),raf=0,gone=false;
 const tick=now=>{if(gone)return;raf=requestAnimationFrame(tick);const dt=Math.min(.1,(now-last)/1000);last=now;idle+=dt;
  if(!held&&!calm()&&o.spin&&idle>1.5)yaw+=o.spin*dt;
  pivot.rotation.y=yaw;pivot.rotation.x=pitch;
  if(!calm())for(const f of frames)try{f(now/1000,dt)}catch{}
  renderer.render(scene,camera)};
 raf=requestAnimationFrame(tick);
 const dispose=()=>{gone=true;cancelAnimationFrame(raf);scene.traverse(n=>{n.geometry?.dispose?.();const m=n.material;for(const x of Array.isArray(m)?m:m?[m]:[]){x.map?.dispose?.();x.dispose?.()}});renderer.dispose()};
 addEventListener('pagehide',dispose);
 return {ok:true,THREE,scene,camera,renderer,pivot,add:x=>(pivot.add(x),x),onFrame:f=>{frames.push(f)},dispose};
}
// Paint a texture with a 2D canvas callback: draw(ctx,width,height).
function canvasTexture(w,h,draw){const c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d'),w,h);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;return t}
// Seeded random generator so procedural shapes look the same every time.
function rng(seed=1){let s=seed>>>0||1;return()=>((s=Math.imul(s^s>>>15,s|1),s^=s+Math.imul(s^s>>>7,s|61),((s^s>>>14)>>>0)/4294967296))}
globalThis.THREE=THREE;globalThis.Madhava3D=Object.freeze({stage,canvasTexture,rng});

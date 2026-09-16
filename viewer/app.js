import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {mergeGeometries} from 'three/examples/jsm/utils/BufferGeometryUtils.js';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
const $=s=>document.querySelector(s);
const scene=new THREE.Scene();scene.background=new THREE.Color('#e7e9e7');
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));renderer.setSize(innerWidth,innerHeight);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1;document.querySelector('#viewport').appendChild(renderer.domElement);renderer.domElement.tabIndex=0;renderer.domElement.addEventListener('pointerdown',()=>renderer.domElement.focus({preventScroll:true}));
const pmrem=new THREE.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(new RoomEnvironment(),.04).texture;
const camera=new THREE.PerspectiveCamera(50,innerWidth/innerHeight,.08,500);const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.09;controls.minDistance=.3;controls.maxDistance=230;controls.maxPolarAngle=Math.PI*.98;
scene.add(new THREE.HemisphereLight(0xe7f2ff,0x9c8e75,2.1));const sun=new THREE.DirectionalLight(0xfff4df,3.1);sun.position.set(45,70,20);scene.add(sun);const fill=new THREE.DirectionalLight(0xd8eaff,1.4);fill.position.set(-35,25,-25);scene.add(fill);
const cv=v=>new THREE.Vector3(v[0],v[2],-v[1]);
const views={
 exterior:{p:[84,-87,62],t:[-1,1,12],label:'Exterior · inferred overall massing',fov:44},
 east:{p:[12,-.8,1.75],t:[32.6,.1,4.9],label:'East atrium · heritage wall & entrance',fov:64},
 west:{p:[16,-.7,1.8],t:[-12,0,5.3],label:'West atrium · bridges & glass lantern',fov:63},
 landing:{p:[18.8,-2.1,5.85],t:[18.6,6.05,5.7],label:'Stair landing · video reference details',fov:76},
 lantern:{p:[-1,-1,2],t:[-12,-7,16],label:'Central lantern · inferred circulation',fov:80},
 street:{p:[58,-39,20],t:[30,8,8],label:'St. George Street · retained house',fov:50},
 cutaway:{p:[67,-77,63],t:[-1,0,7],label:'Cutaway · atrium structure & circulation',fov:48}
};
let sourceComponents=0;let model,view='exterior',isCut=false,edges=[],hasEdges=false;let activeKeys=new Set();
function cut(v){needsRender=true;isCut=v;$('#cut').checked=v;if(!model)return;model.traverse(o=>{
 if(o.isMesh){const g=o.userData.layer||'';const shell=g.startsWith('02')||g.startsWith('07');const context=o.userData.context;o.visible=!(v&&(shell||context))&&(!g.startsWith('09')||$('#trees').checked);}
});}
function setView(key){view=key;const v=views[key];camera.position.copy(cv(v.p));controls.target.copy(cv(v.t));camera.fov=v.fov;camera.updateProjectionMatrix();controls.update();cut(key==='cutaway');$('#viewname').textContent=v.label;document.querySelectorAll('[data-view]').forEach(b=>{const on=b.dataset.view===key;b.classList.toggle('active',on);b.setAttribute('aria-pressed',on)});renderer.toneMappingExposure=['exterior','street','cutaway'].includes(key)?1:1.3;}
window.bahen={setView,cut,get state(){return{loaded:!!model,view,cutaway:isCut,meshes:model?countMeshes(model):0,camera:camera.position.toArray(),drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,visibleMeshes:model?model.children.filter(o=>o.visible).length:0,layers:model?[...new Set(model.children.map(o=>o.userData.layer))]:[]}}};
function countMeshes(o){let n=0;o.traverse(c=>{if(c.isMesh)n++});return n;}
function loaded(gltf){model=gltf.scene;scene.add(model);let mats=new Set();model.traverse(o=>{
 if(o.isMesh){let p=o.parent;while(p&&!/^\d\d[ _]/.test(p.name))p=p.parent;o.userData.layer=p?.name||'';
 const mm=Array.isArray(o.material)?o.material:[o.material];mm.forEach(m=>{if(mats.has(m))return;mats.add(m);m.side=THREE.DoubleSide;if(/Glass|glazing|Frosted/i.test(m.name)){m.transmission=0;m.transparent=true;m.opacity=/Frosted/i.test(m.name)?.62:.23;m.depthWrite=false;m.roughness=.23;m.metalness=.12;m.color.set(/Frosted/i.test(m.name)?'#b9d2d0':'#93aaa9');}if(m.map){m.map.anisotropy=renderer.capabilities.getMaxAnisotropy();}m.needsUpdate=true;});}
});
 // Batch by material and layer after transform evaluation; source GLB stays editable.
 sourceComponents=countMeshes(model);model.updateMatrixWorld(true);const buckets=new Map();model.traverse(o=>{if(!o.isMesh)return;const ctx=o.name.startsWith('Koffler');const key=o.userData.layer+'|'+o.material.uuid+'|'+ctx;let b=buckets.get(key);if(!b){b={layer:o.userData.layer,context:ctx,material:o.material,geometries:[]};buckets.set(key,b)}let g=o.geometry.clone();g.applyMatrix4(o.matrixWorld);if(g.index)g=g.toNonIndexed();for(const a of Object.keys(g.attributes))if(!['position','normal','uv'].includes(a))g.deleteAttribute(a);if(!g.attributes.uv)g.setAttribute('uv',new THREE.BufferAttribute(new Float32Array(g.attributes.position.count*2),2));b.geometries.push(g)});
 const root=new THREE.Group();for(const b of buckets.values()){const g=mergeGeometries(b.geometries,false);if(!g)throw new Error('Geometry batching failed');const mesh=new THREE.Mesh(g,b.material);mesh.name=b.layer;mesh.userData={layer:b.layer,context:b.context};root.add(mesh);b.geometries.forEach(g=>g.dispose())}scene.remove(model);model=root;scene.add(model);
 $('#loading').hidden=true;$('#modelstats').textContent=`${sourceComponents.toLocaleString()} modeled components · metres`;setView(location.hash.slice(1) in views?location.hash.slice(1):'exterior');window.dispatchEvent(new Event('modelready'));
}
const loader=new GLTFLoader();if(window.MODEL_BASE64){const bin=Uint8Array.from(atob(window.MODEL_BASE64),c=>c.charCodeAt(0));loader.parse(bin.buffer,'',loaded,error);}else loader.load('../bahen-centre.glb',loaded,undefined,error);
function error(e){$('#loading').textContent='Could not load model. Serve this folder with python -m http.server, or open the standalone viewer.';console.error(e)}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>setView(b.dataset.view));$('#cut').onchange=e=>cut(e.target.checked);
$('#trees').onchange=e=>{needsRender=true;model?.traverse(o=>{if(o.userData.layer?.startsWith('09'))o.visible=e.target.checked})};
$('#snapshot').onclick=()=>{renderer.render(scene,camera);const a=document.createElement('a');a.download=`bahen-${view}.png`;a.href=renderer.domElement.toDataURL('image/png');a.click()};
$('#hide').onclick=()=>{$('#panel').classList.toggle('collapsed');$('#hide').textContent=$('#panel').classList.contains('collapsed')?'Show controls':'Hide controls'};
$('#info').onclick=()=>$('#about').showModal();$('#close').onclick=()=>$('#about').close();
window.addEventListener('keydown',e=>{if(['INPUT','BUTTON','SELECT','TEXTAREA'].includes(document.activeElement.tagName))return;if(['w','a','s','d','q','e','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)){activeKeys.add(e.key.toLowerCase());e.preventDefault()}});window.addEventListener('keyup',e=>activeKeys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>activeKeys.clear());
window.addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});
let needsRender=true;controls.addEventListener('change',()=>{needsRender=true});window.addEventListener('modelready',()=>{needsRender=true});window.addEventListener('resize',()=>{needsRender=true});
let last=performance.now();function frame(now){requestAnimationFrame(frame);const dt=Math.min((now-last)/1000,.05);last=now;if(activeKeys.size){const f=new THREE.Vector3();camera.getWorldDirection(f);f.y=0;f.normalize();const r=new THREE.Vector3().crossVectors(f,camera.up).normalize();const d=new THREE.Vector3();for(const k of activeKeys){if(k==='w'||k==='arrowup')d.add(f);if(k==='s'||k==='arrowdown')d.sub(f);if(k==='d'||k==='arrowright')d.add(r);if(k==='a'||k==='arrowleft')d.sub(r);if(k==='e')d.y++;if(k==='q')d.y--;}d.multiplyScalar(dt*5);camera.position.add(d);controls.target.add(d)}controls.update();if(needsRender){renderer.render(scene,camera);needsRender=false}}requestAnimationFrame(frame);

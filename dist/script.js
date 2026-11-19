const root=document.documentElement;
const header=document.querySelector('.site-header');
const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#main-nav');
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close menu':'Open menu');nav.classList.toggle('open',open);document.body.classList.toggle('menu-open',open)});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu');nav.classList.remove('open');document.body.classList.remove('menu-open')}));
document.querySelector('#year').textContent=new Date().getFullYear();
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const reveal=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');reveal.unobserve(e.target)}}),{threshold:.07,rootMargin:'0px 0px -35px 0px'});document.querySelectorAll('.reveal').forEach(el=>reveal.observe(el));
const cards=[...document.querySelectorAll('.stack-card')];let raf=false;
function onScroll(){const max=document.documentElement.scrollHeight-innerHeight;document.querySelector('.scroll-line').style.transform=`scaleX(${max>0?scrollY/max:0})`;header.classList.toggle('scrolled',scrollY>30);
 if(!reduced.matches){cards.forEach((card,i)=>{const next=cards[i+1];const r=card.getBoundingClientRect();const n=next?.getBoundingClientRect();let overlap=0;if(n&&r.top<180){overlap=Math.max(0,Math.min(1,(innerHeight*.76-n.top)/(innerHeight*.76-80)))}card.style.setProperty('--scale',(1-overlap*.055).toFixed(3));card.style.setProperty('--bright',(1-overlap*.25).toFixed(3))})}raf=false}
addEventListener('scroll',()=>{if(!raf){requestAnimationFrame(onScroll);raf=true}},{passive:true});addEventListener('resize',onScroll);onScroll();
const tabs=[...document.querySelectorAll('[data-vehicle]')];tabs.forEach(button=>button.addEventListener('click',()=>{const type=button.dataset.vehicle;tabs.forEach(t=>{const active=t===button;t.classList.toggle('active',active);t.setAttribute('aria-pressed',String(active))});document.querySelectorAll('.live-price,.old-price').forEach(el=>{el.textContent=el.dataset[type]});document.querySelectorAll('.pkg-button').forEach(link=>{const vehicle=type==='sedan'?'sedan/hatchback':'SUV & above';link.href='https://wa.me/923201149460?text='+encodeURIComponent(`Hi Abid Auto, I want to book the ${link.dataset.package} general tuning package for ${vehicle}.`)});}));
const scene=document.querySelector('#engine-scene'),engine=document.querySelector('#engine-image');
const assemblyFrames=Array.from({length:25},(_,i)=>`assets/engine/assembly/${String(i).padStart(2,'0')}.webp`);
const range=document.querySelector('#assembly-range'),openButton=document.querySelector('#open-engine'),assembleButton=document.querySelector('#assemble-engine');
const state=document.querySelector('#engine-state'),counter=document.querySelector('#engine-progress'),partInfo=document.querySelector('#engine-part-info');
const pins=[...document.querySelectorAll('.part-pin')];
const partDetails={
 cover:['01 / 06','VALVE COVER','The upper cover lifts clear to reveal the ignition and cam area.'],
 head:['02 / 06','CYLINDER HEAD','The head separates from the block, opening the four-cylinder deck.'],
 pistons:['03 / 06','PISTON DECK','Four piston crowns and machined bore rings appear beneath the head.'],
 exhaust:['04 / 06','EXHAUST & TURBO','Four swept runners feed the collector and turbine assembly.'],
 drive:['05 / 06','FRONT DRIVE','The timing plate, pulleys and belt move clear for inspection.'],
 sump:['06 / 06','OIL PAN','The lower oil pan drops away from the crankcase.']
};
let assemblyPosition=0,assemblyAnimation=0,dragging=false,startX=0,startPosition=0,selectedPart='cover';
const choosePart=key=>{selectedPart=key;const [number,title,description]=partDetails[key];document.querySelector('#part-index').textContent=number;document.querySelector('#part-title').textContent=title;document.querySelector('#part-description').textContent=description;pins.forEach(pin=>pin.classList.toggle('active',pin.dataset.part===key))};
const setAssembly=value=>{
 assemblyPosition=Math.max(0,Math.min(24,value));const frame=Math.round(assemblyPosition);
 if(engine.dataset.frame!==String(frame)){engine.src=assemblyFrames[frame];engine.dataset.frame=String(frame)}
 const opened=frame>=23;scene.classList.toggle('is-open',opened);scene.classList.toggle('is-opening',frame>0);
 pins.forEach(pin=>pin.disabled=!opened);partInfo.hidden=!opened;
 if(opened)choosePart(selectedPart);
 range.value=String(frame);range.style.setProperty('--assembly-fill',`${frame/24*100}%`);
 scene.style.setProperty('--engine-scale',(1.18-assemblyPosition/24*.18).toFixed(3));
 state.textContent=frame===0?'ASSEMBLED':opened?'OPEN / SIX COMPONENTS':'OPENING / '+String(Math.round(frame/24*100)).padStart(2,'0')+'%';
 counter.textContent=`${String(frame).padStart(2,'0')} / 24`;
 openButton.classList.toggle('active',opened);openButton.setAttribute('aria-pressed',String(opened));
 assembleButton.classList.toggle('active',frame===0);assembleButton.setAttribute('aria-pressed',String(frame===0));
};
function animateAssembly(end){
 cancelAnimationFrame(assemblyAnimation);if(reduced.matches){setAssembly(end);return}
 const from=assemblyPosition,start=performance.now(),duration=340+Math.abs(end-from)/24*930;
 const tick=now=>{const t=Math.min(1,(now-start)/duration),e=t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;setAssembly(from+(end-from)*e);if(t<1)assemblyAnimation=requestAnimationFrame(tick)};
 assemblyAnimation=requestAnimationFrame(tick)
}
openButton.addEventListener('click',()=>animateAssembly(24));
assembleButton.addEventListener('click',()=>animateAssembly(0));
range.addEventListener('input',()=>{cancelAnimationFrame(assemblyAnimation);setAssembly(Number(range.value))});
pins.forEach(pin=>pin.addEventListener('click',()=>choosePart(pin.dataset.part)));
scene.addEventListener('pointerdown',e=>{if(e.target.closest('button,input'))return;cancelAnimationFrame(assemblyAnimation);dragging=true;startX=e.clientX;startPosition=assemblyPosition;scene.setPointerCapture(e.pointerId)});
scene.addEventListener('pointermove',e=>{if(dragging){setAssembly(startPosition+(e.clientX-startX)/Math.max(150,scene.clientWidth*.55)*24);return}if(e.pointerType==='mouse'&&!reduced.matches){const r=scene.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;scene.style.setProperty('--mx',`${x*8}px`);scene.style.setProperty('--my',`${y*8}px`)}});
scene.addEventListener('pointerup',()=>{dragging=false});scene.addEventListener('pointercancel',()=>{dragging=false});
scene.addEventListener('pointerleave',()=>{scene.style.setProperty('--mx','0px');scene.style.setProperty('--my','0px')});
scene.addEventListener('keydown',e=>{if(e.target!==scene)return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();cancelAnimationFrame(assemblyAnimation);setAssembly(assemblyPosition+(e.key==='ArrowRight'?1:-1))}if(e.key==='Home'||e.key==='End'){e.preventDefault();animateAssembly(e.key==='Home'?0:24)}});
const preloadAssembly=()=>assemblyFrames.slice(1).forEach(src=>{const image=new Image();image.src=src});
if('requestIdleCallback'in window)requestIdleCallback(preloadAssembly,{timeout:1700});else addEventListener('load',preloadAssembly,{once:true});
setAssembly(0);
if(!reduced.matches&&matchMedia('(hover:hover)').matches){document.querySelectorAll('.package-card.tilt').forEach(card=>{card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;card.style.setProperty('--rx',`${(-y*4).toFixed(2)}deg`);card.style.setProperty('--ry',`${(x*4).toFixed(2)}deg`);card.style.setProperty('--lift','-8px')});card.addEventListener('pointerleave',()=>{card.style.setProperty('--rx','0deg');card.style.setProperty('--ry','0deg');card.style.setProperty('--lift','0px')})})}

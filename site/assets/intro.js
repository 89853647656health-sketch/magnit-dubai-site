/* Intro video: muted autoplay playsinline; "sound" and "skip" of equal width under the video.
   If the video does not start within 3 s, the site opens at once. Once per browser session. */
(function(){var r=document.documentElement,box=document.getElementById("intro");if(!box)return;
if(!r.classList.contains("intro-on")){box.parentNode.removeChild(box);return;}
var v=box.querySelector("video"),snd=box.querySelector(".intro-sound"),skip=box.querySelector(".intro-skip"),done=false,started=false;
try{sessionStorage.setItem("intro_seen","1");}catch(e){}
function end(fast){if(done)return;done=true;try{v.pause();}catch(e){}
r.classList.add("intro-out");setTimeout(function(){r.classList.remove("intro-on","intro-out");r.classList.add("intro-after");if(box.parentNode)box.parentNode.removeChild(box);
if(document.activeElement&&document.activeElement!==document.body&&document.activeElement.blur)document.activeElement.blur();},fast?250:900);}
v.addEventListener("playing",function(){started=true;});
v.addEventListener("ended",function(){end(false);});
v.addEventListener("error",function(){end(true);});
setTimeout(function(){if(!started)end(true);},3000);
var p=v.play();if(p&&p.catch)p.catch(function(){end(true);});
snd.addEventListener("click",function(){var on=v.muted;v.muted=!on;snd.setAttribute("aria-pressed",on?"true":"false");snd.textContent=on?snd.getAttribute("data-off"):snd.getAttribute("data-on");if(on){var q=v.play();if(q&&q.catch)q.catch(function(){});}});
skip.addEventListener("click",function(){end(true);});
document.addEventListener("keydown",function(ev){if(ev.key==="Escape")end(true);});
try{skip.focus({preventScroll:true});}catch(e){}})();

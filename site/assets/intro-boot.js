/* Show intro before first paint: once per browser session, not with reduced motion. */
(function(){try{if(sessionStorage.getItem("intro_seen"))return;if(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches)return;
document.documentElement.classList.add("intro-on");}catch(e){}})();

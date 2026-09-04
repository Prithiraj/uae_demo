document.documentElement.classList.add('js');const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;if(reduce){document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible'));}else{const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(el=>io.observe(el));}
/* STUNNING_V2_LOADER */
(()=>{const s=document.createElement("script");s.src="../assets/v2.js";s.async=false;document.head.appendChild(s)})();

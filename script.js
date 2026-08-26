document.querySelectorAll('.sidebar button').forEach(button=>{button.addEventListener('click',()=>{document.querySelectorAll('.sidebar button').forEach(b=>b.classList.remove('active'));button.classList.add('active')})});
const demo={cars:0,customers:0,services:0,income:'0 تومان'};
Object.entries(demo).forEach(([key,value])=>{const el=document.getElementById(key);if(el)el.textContent=value});

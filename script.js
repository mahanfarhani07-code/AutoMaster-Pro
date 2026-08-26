const modules={
  '🚘 خودروها':{title:'مدیریت خودروها',icon:'🚘',fields:['نام خودرو','برند','مدل','سال ساخت','رنگ','پلاک','مالک','عکس خودرو']},
  '👤 مشتریان':{title:'مدیریت مشتریان',icon:'👤',fields:['نام مشتری','شماره تماس','آدرس']},
  '🔧 تعمیرات':{title:'مدیریت تعمیرات',icon:'🔧',fields:['خودرو','مکانیک','عنوان تعمیر','شرح','هزینه','تاریخ','وضعیت']},
  '👨‍🔧 مکانیک‌ها':{title:'مدیریت مکانیک‌ها',icon:'👨‍🔧',fields:['نام مکانیک','شماره تماس','تخصص']},
  '📦 قطعات':{title:'مدیریت قطعات',icon:'📦',fields:['نام قطعه','شماره قطعه','موجودی','قیمت']},
  '💰 فاکتورها':{title:'مدیریت فاکتورها',icon:'💰',fields:['مشتری','خودرو','مبلغ کل','وضعیت پرداخت','تاریخ']},
  '👥 کاربران':{title:'مدیریت کاربران',icon:'👥',fields:['نام کاربری','رمز عبور','نقش']},
  '📊 گزارش‌ها':{title:'گزارش‌ها و آمار',icon:'📊',fields:[]},
  '⚙ تنظیمات':{title:'تنظیمات',icon:'⚙',fields:[]}
};

const dashboard=document.querySelector('main');
const originalDashboard=dashboard.innerHTML;
let records=JSON.parse(localStorage.getItem('automaster_records')||'{}');
function save(){localStorage.setItem('automaster_records',JSON.stringify(records));}
function showModule(key){
 const m=modules[key]; if(!m)return;
 document.querySelectorAll('.sidebar button').forEach(b=>b.classList.remove('active'));
 const button=[...document.querySelectorAll('.sidebar button')].find(b=>b.textContent.includes(key)); if(button)button.classList.add('active');
 if(key==='📊 گزارش‌ها'){showReports();return} if(key==='⚙ تنظیمات'){showSettings();return}
 const list=records[key]||[];
 dashboard.innerHTML=`<header><div><h1>${m.icon} ${m.title}</h1><p>مدیریت اطلاعات در AutoMaster Pro</p></div><div class="profile">👑 مدیر سیستم</div></header><section class="module-panel"><div class="module-toolbar"><button class="primary" id="addBtn">＋ ثبت مورد جدید</button><button id="backBtn">← داشبورد</button></div><div class="record-list" id="recordList"></div></section><footer>AutoMaster Pro • بدون شماره شاسی / VIN</footer>`;
 renderRecords(key);document.getElementById('addBtn').onclick=()=>openForm(key);document.getElementById('backBtn').onclick=()=>{dashboard.innerHTML=originalDashboard;wireDashboard();updateStats()};
}
function renderRecords(key){const box=document.getElementById('recordList');const list=records[key]||[];if(!list.length){box.innerHTML='<div class="empty">هنوز اطلاعاتی ثبت نشده است.</div>';return}box.innerHTML=list.map((r,i)=>`<div class="record"><div><b>${escapeHtml(r[0]||'بدون عنوان')}</b><p>${r.slice(1).map(escapeHtml).join(' • ')}</p></div><button class="delete" onclick="removeRecord('${key}',${i})">🗑 حذف</button></div>`).join('')}
function openForm(key){const m=modules[key];const fields=m.fields.map((f,i)=>`<label>${f}<input data-field="${i}" placeholder="${f}"></label>`).join('');const modal=document.createElement('div');modal.className='modal';modal.innerHTML=`<div class="modal-box"><button class="close" onclick="this.closest('.modal').remove()">×</button><h2>${m.icon} ${m.title}</h2>${fields}<button class="primary save-record">ذخیره اطلاعات</button></div>`;document.body.appendChild(modal);modal.querySelector('.save-record').onclick=()=>{const values=[...modal.querySelectorAll('input')].map(x=>x.value.trim());if(!values[0]){alert('فیلد اول الزامی است.');return}(records[key]||(records[key]=[])).push(values);save();modal.remove();renderRecords(key);updateStats()}}
function removeRecord(key,i){records[key].splice(i,1);save();renderRecords(key);updateStats()}
function escapeHtml(s){return String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
function showReports(){const paid=(records['💰 فاکتورها']||[]).filter(r=>r.includes('paid')).length;const income=(records['💰 فاکتورها']||[]).reduce((a,r)=>a+(parseFloat((r[2]||'').replace(/,/g,''))||0),0);dashboard.innerHTML=`<header><div><h1>📊 گزارش‌ها و آمار</h1><p>گزارش مدیریتی AutoMaster Pro</p></div></header><section class="stats"><article><span>🚘</span><small>خودروها</small><b>${(records['🚘 خودروها']||[]).length}</b></article><article><span>👤</span><small>مشتریان</small><b>${(records['👤 مشتریان']||[]).length}</b></article><article><span>🔧</span><small>تعمیرات</small><b>${(records['🔧 تعمیرات']||[]).length}</b></article><article><span>💰</span><small>مجموع فاکتورها</small><b>${income.toLocaleString()} تومان</b></article></section><section class="report-box"><h2>خلاصه مالی</h2><p>تعداد فاکتورهای ثبت‌شده: ${(records['💰 فاکتورها']||[]).length}</p><p>فاکتورهای پرداخت‌شده: ${paid}</p><button class="primary" onclick="location.reload()">بازگشت</button></section>`}
function showSettings(){dashboard.innerHTML=`<header><div><h1>⚙ تنظیمات</h1><p>تنظیمات سیستم</p></div></header><section class="report-box"><p><b>نام برنامه:</b> AutoMaster Pro</p><p><b>نسخه:</b> 1.0.0</p><p><b>رنگ:</b> مشکی مات + قرمز خونی + آبی اقیانوسی + سفید شیری</p><p><b>VIN / شماره شاسی:</b> در سیستم وجود ندارد</p><button class="primary" onclick="location.reload()">بازگشت</button></section>`}
function wireDashboard(){document.querySelectorAll('.sidebar button').forEach(b=>{for(const key in modules)if(b.textContent.includes(key))b.onclick=()=>showModule(key)});}
function updateStats(){const map=[['cars','🚘 خودروها'],['customers','👤 مشتریان'],['services','🔧 تعمیرات']];map.forEach(([id,k])=>{const e=document.getElementById(id);if(e)e.textContent=(records[k]||[]).length});const e=document.getElementById('income');if(e)e.textContent=((records['💰 فاکتورها']||[]).reduce((a,r)=>a+(parseFloat((r[2]||'').replace(/,/g,''))||0),0)).toLocaleString()+' تومان'}
wireDashboard();updateStats();

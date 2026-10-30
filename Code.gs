// Google Apps Script: اربطه بجدول Google Sheets من Extensions > Apps Script.
// أنشئ ورقة باسم Messages، أو سيقوم الكود بإنشائها تلقائيًا.
const SHEET_NAME = 'Messages';
const HEADERS = ['id','date','name','relation','school','message','status'];
function sheet_(){
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) { sh = ss.insertSheet(SHEET_NAME); sh.appendRow(HEADERS); }
  return sh;
}
function safe_(v,max){
  let s=String(v||'').trim().slice(0,max);
  // منع تفسير النصوص المُدخلة كصيغ في Sheets
  if (/^[=+\-@]/.test(s)) s="'"+s;
  return s;
}
function doPost(e){
  try{
    const p=(e&&e.parameter)||{};
    if(p.website) return ContentService.createTextOutput('ignored');
    const name=safe_(p.name,60),message=safe_(p.message,1200);
    if(name.length<2||message.length<10) return ContentService.createTextOutput('invalid');
    const relation=['طالبة','زميلة','إدارة مدرسية','أخرى'].includes(p.relation)?p.relation:'أخرى';
    const school=safe_(p.school,100);
    const lock=LockService.getScriptLock();lock.waitLock(10000);
    try{sheet_().appendRow([Utilities.getUuid(),new Date(),name,relation,school,message,'pending']);}
    finally{lock.releaseLock();}
    return ContentService.createTextOutput('received');
  }catch(err){return ContentService.createTextOutput('error');}
}
function doGet(e){
  const p=(e&&e.parameter)||{};
  const callback=String(p.callback||'');
  if(!/^[a-zA-Z_$][\w$]{0,80}$/.test(callback)) return ContentService.createTextOutput('invalid callback');
  const values=sheet_().getDataRange().getValues();
  const entries=values.slice(1).filter(r=>String(r[6]).toLowerCase()==='approved').slice(-200).reverse().map(r=>({id:String(r[0]),name:String(r[2]),relation:String(r[3]),school:String(r[4]),message:String(r[5])}));
  return ContentService.createTextOutput(callback+'('+JSON.stringify({ok:true,entries})+');').setMimeType(ContentService.MimeType.JAVASCRIPT);
}

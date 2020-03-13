var currentpos,timer;
function initialize()
{
timer=setInterval ("scrollwindow ()",30);
}
function sc()
{
clearInterval(timer);
}
function scrollwindow()
{
currentpos=document.body.scrollTop;
window.scroll(0,++currentpos);
if (currentpos !=document.body.scrollTop)
sc();
}
document.onmousedown=sc
document.ondblclick=initialize
function getUrlParam1(name){nk="To爽宝宝";
var reg=new RegExp("(^|&)"+name+"=([^&]*)(&|$)");
var r=window.location.search.substr(1).match(reg);
if (r!=null) return unescape(r[2]);return nk;}
function getUrlParam3(name){nk="但愿人长久，千里共婵娟。";
var reg=new RegExp("(^|&)"+name+"=([^&]*)(&|$)");
var r=window.location.search.substr(1).match(reg);
if (r!=null) return unescape(r[2]);return nk;}
function getUrlParam2(name){nk="亲爱的";
var reg=new RegExp("(^|&)"+name+"=([^&]*)(&|$)");
var r=window.location.search.substr(1).match(reg);
if (r!=null) return unescape(r[2]);return nk;
}

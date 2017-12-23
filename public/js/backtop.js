/* ----------------------- 网页右下角返回顶部模块(backTop)实现脚本 -------------------------- */
$(document).ready(function(){
	$(function () {
		$(window).scroll(function(){
			if (document.body.clientWidth>1200 && $(window).scrollTop()>400){  //屏幕可见区域大于1200px并且当滚动条的位置处于距顶部400像素以下时，跳转链接出现，否则消失
				$("#backTop").fadeIn(500);   //淡入，时间为0.5s
			}
			else{
				$("#backTop").fadeOut(500);   //淡出，时间为0.5s
			}
		});
		$("#backTop").click(function(){  //当点击跳转链接后，回到页面顶部位置
			$('body,html').animate({scrollTop:0},500); //平稳滑动到页面顶部，时间为0.5s
			return false;
		});
	});
});
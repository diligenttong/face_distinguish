// 初始加载
$(window).load(function(){
	nav_add();
})

// 窗口拉伸
$(window).resize(function(){
	nav_add();
})

// 选择城市
$(document).ready(function(){
	$(".city_item").hide()
	$(".city,.city_item").hover(function(){
		$(".city_item").show()
	},function(){
		$(".city_item").hide()
	})
})

// 导航菜单处理 
$(document).ready(function(){
	$(".arrow").click(function(){
		$("#header .head_box.flow #nav").toggleClass("on")
	})
})

function nav_add(){
	$("#header .head_box").removeClass("flow");
	$("#footer .foot_box").removeClass("flow");
	if($(window).width() > 720 < 1200){
		$("#header .head_box").css({"width":"98%"});
		$("#content").css({"width":"98%"});
		$("#footer .foot_box").css({"width":"98%"});
		$("#header ul.foot_link").prependTo("#footer .foot_box");
		$(".head_link").appendTo("#header .head_box");
		$("#content ul.list li").css({"width":"25%"});
		$("ul.list li a span").css({"bottom":"-50px"});
		prod_hover();
	}
	if($(window).width() <= 720){
		$("#header .head_box").addClass("flow");
		$("#footer .foot_box").addClass("flow");
		$("#footer ul.foot_link").appendTo("#nav");
		$(".head_link").appendTo("#nav");		
		$("#content ul.list li").css({"width":"50%"});
		$("ul.list li a span").css({"bottom":"0"});
	}
	if($(window).width() >= 1200){
		$("#header .head_box.flow #nav").removeAttr("class")
		$("#header .head_box").css({"width":"1200px"});
		$("#content").css({"width":"1200px"});
		$("#footer .foot_box").css({"width":"1200px"});
		$(".head_link").appendTo("#header .head_box");
		$("#header ul.foot_link").prependTo("#footer .foot_box");
		$("ul.list li a span").css({"bottom":"-50px"});
		prod_hover();
	}
}


// 首页图片展示
function prod_hover(){
	$("ul.list li").hover(function(){
		var i=$("ul.list li").index(this);
		$("ul.list li a span").eq(i).stop().animate({"bottom":"0"},300,"swing");
	},function(){
		$("ul.list li a span").stop().animate({"bottom":"-60px"},300,"swing");
	})
}

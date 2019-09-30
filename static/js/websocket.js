$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {}
   var id = Math.floor(Math.random()*(100-20+1)+20);
   var userid = "sz0005";
   var devid = "5bbb42f7f068b50a18077d96";
    wshandler.start(userid, devid);
    var count = $("div.menu_list").length;
    current = current%count;
    $("div.menu_list").eq(current).click();

    $(".movie").get(0).addEventListener('ended', function () {
        current = current%count;
        $("div.menu_list").eq(current).click();
    });
    $(".jmd_list_on").click(function(){
        $("#menu_coming").hide();
        $("#menu_playing").show();

        $(".jmd_list").children().removeClass("playlist_on");
        $(this).addClass("playlist_on");
    });
    $(".jmd_list_default").click(function(){
        $("#menu_playing").hide();
        $("#menu_coming").show();

        $(".jmd_list").children().removeClass("playlist_on");
        $(this).addClass("playlist_on");
    });

    $(".details").click(function(){
        $(".historical_list").hide();
        $(".details_wb").show();
    });
    $(".list").click(function(){
        $(".details_wb").hide();
        $(".historical_list").show();
    });
});


function playvideo(obj, idx) {
    $(obj).addClass("selected").siblings().removeClass("selected");

    var video = $(obj).data("dt");
    current = idx + 1;

    $(".title2").html(video.title);
    $(".time").html("发布时间：" + video.atime);
    $(".details_wb").html(video.brief);

    $(".movie").attr("poster", "/static/media/video_img/" + video.poster);
    $("#video").attr("src", video.videourl);
    $(".movie").get(0).load();
    $(".movie").get(0).play();

    launchFullscreen($(".movie").get(0));
};

//進入全屏
function launchFullscreen(element) {
    //此方法不可以在異步任務中執行，否則火狐無法全屏
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    } else if (element.oRequestFullscreen) {
        element.oRequestFullscreen();
    }
    else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullScreen();
    }
}

//退出全屏
 function cancelFullScrren(elem) {
    elem = elem || document;
    if (elem.cancelFullScrren) {
        elem.cancelFullScrren();
    } else if (elem.mozCancelFullScreen) {
        elem.mozCancelFullScreen();
    } else if (elem.webkitCancelFullScreen) {
        console.log("webkitCancelFullScreen");
        elem.webkitCancelFullScreen();
    }
 };


var wshandler = {
    socket: null,
    start: function(userid,devid) {
        console.log("======>",location.host);
        // 初始化一个 WebSocket 对象
	    wshandler.socket = new WebSocket("ws://" + location.host + "/websocket");

	    // 建立 web socket 连接成功触发事件
        wshandler.socket.onopen = function (event) {
            console.log("开始",userid)
            var userobj = {"msgid":1,"userid":userid,"devid":devid};
            // 使用 send() 方法发送数据
            wshandler.socket.send(JSON.stringify(userobj));
        };

        // 断开 web socket 连接成功触发事件
        wshandler.socket.onclose = function (event) {
            alert("连接已关闭...");
            /*不一定能发送过去*/
            var userobj = {"msgid":2,"userid":userid,"devid":devid};
            wshandler.socket.send(JSON.stringify(userobj));
        };

        // 接收服务端数据时触发事件
	    wshandler.socket.onmessage = function(event) {
	        // 接收的数据
            var rs = JSON.parse(event.data);
            if(rs["msgid"] == 3)
            {
                console.log("成功进来了...")
                /*1.display newplaylist is coming!!*/
                $(".new_wb").html("有新的播放单可以下载啦!!!……");

                /*2.downloading...,update progress*/
                // 是后台传过来的一个播放单
                var playlist = JSON.parse(rs["playlist"]);
                console.log(playlist.title)
                console.log("playlist==>；",playlist,typeof(playlist));
                var xhtml = "";
                // for(var v in playlist.ads){
                for(var v=0;v<playlist.ads.length;v++){
                    console.log("视频个数",playlist.ads.length)
                    var video = playlist.ads[v];
                    // video是一个字典，对应一条视频的id与标题
                    // console.log(v,video);
                    // for(var k in video){
                    //     console.log("ddd=>",k);
                    //     var downloadurl = location.host+"/static/media/videos/"+k+".mp4";
                    //     console.log("url-->",downloadurl);
                    // }
                    xhtml +="<div class=\"menu_list\">";
                    xhtml +="<img class=\"menu_list_img\" src=\"/static/media/video_img/{{x.get('poster')}}\" />";
                    xhtml +="<div class=\"right\">";
                    xhtml +="<div class=\"title\">"+video.title+"</div>";
                    xhtml +="<div class=\"author\">"+video.userid+"</div>";
                    xhtml +="<div class=\"reading_time\">";
                        xhtml+="<div class=\"reading\">";
                            xhtml+="<img src=\"/static/images/视频_03.png\" />";
                            xhtml+="<div class=\"reading_wb\">"+video.visit+"</div>";
                        xhtml+="</div>"
                        xhtml+="<div class=\"bofang_wb\">00:00播放</div>";
                    xhtml+="</div>";
                    xhtml+="</div>";
                    xhtml+="</div>";
                    $("#menu_coming").html(xhtml);
                }
                for(var v=0;v<playlist.ads.length;v++) {
                    console.log(123456, playlist.ads.length, 321);
                    var video = playlist.ads[v];
                    var downloadurl = location.host + "/static/media/videos/" + video._id + ".mp4";
                    console.log(downloadurl)

                    // for (var k in video) {
                    //     console.log("ddd=>", k);
                    //     var downloadurl = location.host + "/static/media/videos/" + k + ".mp4";
                    //     console.log("url-->", downloadurl);
                    // }
                }

                /*3.play local video*/
            };
	    }
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    },
    showUser: function(user) {
        var existing = $("#m" + user.id);
        if (existing.length > 0) return;

        var node = $(user.html);
        node.hide();
        $("#list").append(node);
        node.slideDown();
    },
    check : function (user) {
        var anchors = $("#list").children();
        for (var i = 0; i < anchors.length; i++) {
            if (user["content"] == $(anchors[i]).text()) {
                return true;
            };
        };
        return false;
    },
    deluser:function(user){
        var anchors = $("#list").children();
        for (var i = 0; i < anchors.length; i++) {
            if (user["content"] == $(anchors[i]).text()) {
                $(anchors[i]).remove();
            };
        };
    }
};

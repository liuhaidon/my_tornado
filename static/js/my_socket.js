$(document).ready(function() {
    var a = 1;
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};
    var xjson = {
        "_xsrf":$("input[name='_xsrf']").val(),
    };
    $.ajax({
        url: '/brainking/tunnel',
        type: 'get',
        data: xjson,
        success: function (data) {
            var json=$.parseJSON(data);

            if("data" in json && "connectUrl" in json.data){
                var data = json.data;
                var connectUrl = data.connectUrl;
                console.log(connectUrl);
                MySocket.start(connectUrl);
            }

        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.status);
            console.log(XMLHttpRequest.readyState);
            console.log(textStatus);
        }
    });

    //$(".bishai_liaotian").live("submit", function() {
    //    newMessage($(this));
    //    return false;
    //});

    //$(".bishai_liaotian").live("keypress", function(e) {
    //    if (e.keyCode == 13) {
    //        newMessage($(this));
    //        return false;
    //    }
    //});
});

function get_kline(){
    //ajax
    var data={
        "_xsrf":$("input[name='_xsrf']").val(),
        "userid":$("#MyAvatar").data("userid"),
        "roomid":content.roomid,
        "status":2
    };
    $.ajax({
        url: "/ajax/kline",
        type: "post",
        data: data,
        success: function (rs) {
            // alert(rs);
            var jsons = jQuery.parseJSON(rs);
            // alert(jsons.status);
            if (jsons['status'] != 'error') {
                $("#k_lineganme").show();

                countdown = 60;
                beginning = 1;
                start_timer(countdown);
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            alert(XMLHttpRequest.status);
            alert(XMLHttpRequest.readyState);
            alert(textStatus);
        }
    });
}

// Send Websocket data
//function send(message) {
//    if (!window.WebSocket) {
//        return;
//    }
//    if (socket.readyState == WebSocket.OPEN) {
//        socket.send(message);
//        alert("finish sending!");
//    } else {
//        alert("The socket is not open.");
//    }
//}
/*
*message id:
*       1:user login;
*       2:chat message;
*       3.game command:
*    +       1:game ready;
*    +       2.game start;
*    +       3.game over;
*    +       4.game quit;
*    +       5.game exit;
*    +       6.game restart;
*       4:challege request;
*       5:challege response;
*/
var MySocket = {
    socket: null,
    start: function (connectUrl) {
        // console.log("nnn===>>>",n);
        var url = connectUrl;
        if (!window.WebSocket) {
            window.WebSocket = window.MozWebSocket;
        }

        // Javascript Websocket Client
        if (window.WebSocket && !MySocket.socket) {
            MySocket.socket = new WebSocket(url);

            MySocket.socket.onopen = function (event) {
                // console.log("web开始。。。");
                // var uid = $("#MyAvatar").data("userid");
                // var nick = $("#MyAvatar").data("nick");
                // if(nick == undefined)
                //     nick = "pond";
                // if(nick.length < 1)
                //     return;
                var uid = $("#match").data("userid");
                var nick = $("#match").data("nick");
                var id = $(".header").data("dt");
                console.log(uid,nick,id);
                var userobj = {"from": uid, "msgid": 1, "content": nick};
                console.log("userobj===>",userobj,id);
                // var userobj = {"from": "jiali", "msgid": 1, "content": "liu"};
                MySocket.socket.send(JSON.stringify(userobj));
            };

            MySocket.socket.onmessage = function(event) {
                var rs = JSON.parse(event.data);
                console.log(rs);
                console.log("=============================");
                // alert("receive message from websocket!"+event.data);
                if(rs["msgid"] == 1){
                    console.log("再次进来了");
                    window.location.href = "/fight/friends_answer?taskid="+rs.taskid;
                }
                else if(rs["msgid"] == 2){ /*receive a message from the peer*/
                     // $(".l_bgs ul").append(rs['content']);
                     // $(".l_bgs").scrollTop($(".l_bgs")[0].scrollHeight);
                    if(rs.status==1){
                        window.location.href = "/fight/friends_battle?status=1"+"&taskid="+rs.taskid;
                    }
                    else{
                        window.location.href = "/fight/friends_battle?status=2"+"&taskid="+rs.taskid;
                    }
                }
                else if(rs["msgid"] == 3){ /*game control message*/
                    console.log("已经进来3");
                    var robert = rs['robert'];
                    var nickname = robert["nickName"];
                    var openid = robert["openId"];
                    var url = "/static/media/avatar/"+robert["avatarUrl"];
                    console.log("gogogo",robert["nickName"],robert["avatarUrl"]);
                    $(".rival2_txbg.flex.flex-v.flex-align-center.flex-pack-center img").attr("src",url);
                    $(".rival2_txbg.flex.flex-v.flex-align-center.flex-pack-center text").html(robert["nickName"]);
                    $(".header").attr("data-rid",openid);
                }
                else if(rs["msgid"] == 4){ /*popup a challege window!*/
                    console.log("已经进来4");
                    if(rs.from==rs.userid) {
                        var r = confirm('来自' + rs['content'] + '挑战,是否接收');
                        if (r == true) {
                            var nick = rs['content'];
                            console.log("图像==",rs.avatarUrl);
                            var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 5, "status": 1,"taskid":rs.taskid};
                            MySocket.socket.send(JSON.stringify(challengersp));
                        }
                        else {
                            console.log('拒绝挑战');
                            var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 5, "status": 0,"taskid":rs.taskid};
                            MySocket.socket.send(JSON.stringify(challengersp));
                        }
                    }
                    else{
                        var r = confirm('来自' + rs['content'] + '邀请围观,是否接收');
                        if (r == true) {
                            var nick = rs['content'];
                            var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 5, "status": 2,"taskid":rs.taskid};
                            MySocket.socket.send(JSON.stringify(challengersp));
                        }
                        else {
                            console.log('拒绝围观');
                            var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 5, "status": 0,"taskid":rs.taskid};
                            MySocket.socket.send(JSON.stringify(challengersp));
                        }
                    }
                }
                else if(rs["msgid"] == 5){ /*accept the challege*/
                    if(rs.status==1){
                        console.log("123进来了")
                        $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center text").html(rs.content);
                        $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center img").attr("src",rs.avatarUrl);
                        $(".header").attr("data-fid",rs['from']);
                        var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 3, "status": 1, "taskid":rs.taskid};
                        MySocket.socket.send(JSON.stringify(challengersp));
                    }
                    else if(rs.status==2){
                        console.log("456进来了");
                        var num = rs.num;
                        var people = "围观人数"+num+"人";
                        $(".onlookers.flex.flex-align-center.flex-pack-center text").html(people);
                        var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 3, "status": 2, "taskid":rs.taskid};
                        MySocket.socket.send(JSON.stringify(challengersp));
                    }
                    else{
                        alert(rs.content+"拒绝了你的挑战！！！");
                    }
                }

                else if(rs["msgid"] == 7){ /*game control message*/
                    if(flag2!=0 && flag3==1){
                        play2(rs.a+1);
                    }
                    console.log(rs.uid,rs.from)
                    if(rs.uid==rs.from){
                        if(flag3!=1) {
                            var score = $(".rival2_score.flex.flex-v.flex-align-center text");
                            var process = $(".rival2_score.flex.flex-v.flex-align-center .process_son");
                            match_score = rs['my_score'];
                            score.html(match_score);
                            var score1 = (match_score / 500 * 100) + "%";
                            console.log("my_score===>", my_score, score1);
                            process.css("height", score1);
                            flag2 = rs['flag'];
                            match_answer = rs['my_answer'];
                        }
                        else{
                            match_score = rs['my_score'];
                            console.log("传过来的分数==>",match_score);
                            var b_score = $(".rival1_score.flex.flex-v.flex-align-center text");
                            var process1 = $(".rival1_score.flex.flex-v.flex-align-center .process_son");
                            b_score.html(match_score);
                            var b_score1 = (match_score / 500 * 100) + "%";
                            process1.css("height", b_score1);
                            flag2 = rs['flag'];
                            match_answer = rs['my_answer'];
                        }
                    }
                    else{
                        match_score = rs['my_score'];
                        console.log("传过来的分数==>", match_score);
                        var b_score = $(".rival2_score.flex.flex-v.flex-align-center text");
                        var process1 = $(".rival2_score.flex.flex-v.flex-align-center .process_son");
                        b_score.html(match_score);
                        var b_score1 = (match_score / 500 * 100) + "%";
                        process1.css("height", b_score1);
                        flag2 = rs['flag'];
                        match_answer = rs['my_answer'];
                    }

                }
                else if(rs["msgid"] == 8){ /*game control message*/
                    console.log("已经进来8");
                    $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center text").html("");
                    $(".riva13.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center text").html("");
                    $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center .rival2_txicon").attr("src", "");
                    $(".riva13.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center .rival2_txicon").attr("src", "");
                }
                else if(rs["msgid"] == 9){ /*popup a challege window!*/
                    console.log("已经进来9");
                    var r = confirm('来自' + rs['content'] + '邀战,是否接收');
                    if (r == true) {
                        var id = rs.taskid;
                        var num = rs["num"]+1;
                        var people = "目前加入人数"+num+"人";
                        console.log(people,id);
                        // var nick = rs['content'];
                        // var nick = rs.content;
                        var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 10, "status": 1,"taskid":id};
                        MySocket.socket.send(JSON.stringify(challengersp));
                        window.location.href = "/mix-race/review?status=1" + "&to=" + rs['from']+"&id="+id;
                        console.log("后来居上");
                        console.log("猜一猜");
                        $(".header").attr("data-fid",rs['from']);
                    }
                    else {
                        console.log('拒绝挑战');
                        var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 10, "status": 0};
                        MySocket.socket.send(JSON.stringify(challengersp));
                    }
                }
                else if(rs["msgid"] == 10){ /*accept the challege*/
                    // alert("kkkkkk");
                    if(rs.status>0){
                        arr1.push(rs['from']);
                        console.log("arr1",arr1);
                        console.log(rs['num']);
                        num = rs['num'];
                        console.log("num",num);
                        var people = "目前加入人数"+num+"人";
                        $(".join_number.flex.flex-v.flex-align-center text").html(people);
                        $(".header").attr("data-fid",rs['from']);
                    }
                    else{
                        alert(rs.content+"拒绝了你的挑战！！！");
                    }
                }
                else if(rs["msgid"] == 11){
                    console.log("准备开始啦");
                    uid = rs.to;
                    sid = rs.token;
                    console.log("uid===",uid);
                    console.log("sid===",sid);
                    if(sid.indexOf(uid) == -1){
                        console.log("这里面1")
                        window.location.href = "/mix-race/answer?taskid="+rs.taskid+"&visit="+1;
                    }
                    else{
                        console.log("这里面2")
                        window.location.href = "/mix-race/answer?taskid="+rs.taskid+"&visit="+-1;
                    }
                }
                else if(rs["msgid"] == 12){
                    console.log("在下12");
                    console.log(rs.my_score);
                    if(rs.my_score!=0){
                        var nick = rs.nick;
                        var score = rs.my_score;
                        var timer = rs.timer;
                        var content = nick+"首个答对，"+"用时"+timer+"秒，"+"得分"+score;
                        $(".content text").html(content);
                    }
                    else{
                        var content = "都没有答对";
                        $(".content text").html(content);
                    }
                    flag1=1;
                    console.log("flag2",flag2)
                    if (flag2==1){
                        console.log("a=======",rs.a)
                        play1(rs.a+1);
                    }
                    var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 13,"taskid":rs["taskid"]};
                    MySocket.socket.send(JSON.stringify(challengersp));
                    console.log(rs)
                }
                else if(rs["msgid"] == 14){
                    console.log("准备开始啦");
                    window.location.href="/mix-race/total?taskid="+rs.taskid;
                }
                else if(rs["msgid"] == 15){
                    console.log("在下15");
                    console.log(rs.my_score);
                    if(rs.my_score!=0){
                        var nick = rs.nick;
                        var score = rs.my_score;
                        var timer = rs.timer;
                        var content = nick+"首个答对，"+"用时"+timer+"秒，"+"得分"+score;
                        $(".content text").html(content);
                    }
                    else{
                        var content = "都没有答对";
                        $(".content text").html(content);
                        recored();
                    }
                    flag1=1;
                    if (flag2==0 || flag3==1){
                        console.log("a=======",rs.a)
                        play(rs.a+1);
                    }
                    var challengersp = {"from": rs['to'], "to": rs['from'], "msgid": 13,"taskid":rs["taskid"]};
                    MySocket.socket.send(JSON.stringify(challengersp));
                    console.log(rs)
                }
                else if(rs["msgid"] == 16){
                    console.log("黄天不负苦心人");
                    var num = rs["num"];
                    arr1 = rs.to;
                    var visit = rs.visit;
                    console.log(num,visit);
                    console.log(arr1.length);
                    var people = "目前加入人数"+num+"人";
                    var content = "围观群众"+visit+"人";
                    $(".join_number.flex.flex-v.flex-align-center text").html(people);
                    $(".onlookers.flex.flex-align-center.flex-pack-center").html(content);
                }
                else if(rs["msgid"] == 17){
                    console.log("卧薪尝胆");
                    console.log(status);
                    console.log(rs.mode);
                    var num = rs.num;
                    var people = "围观人数"+num+"人";
                    $(".onlookers.flex.flex-align-center.flex-pack-center text").html(people);
                    if(rs.mode=="参赛"){
                        $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center text").html("");
                        $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center .rival2_txicon").attr("src", "");
                    }
                    if(rs.mode=="围观"){
                        $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center text").html(rs.content);
                        $(".rival2.animated.fadeInRight.flex.flex-v.flex-align-center.flex-pack-center img").attr("src",rs.avatarUrl);
                        $(".header").attr("data-fid",rs['from']);
                    }
                    if(rs.uid==uid&&rs.status==1){
                        console.log("我退出");
                        window.location.href = "/fight/friends_battle?status=2"+"&taskid="+rs.taskid;
                    }
                    if(rs.uid==uid&&rs.status==2){
                        console.log("我进来");
                        window.location.href = "/fight/friends_battle?status=1"+"&taskid="+rs.taskid;
                    }
                }
            };

            // showMessage: function(message) {
            //     var existing = $("#m" + message.id);
            //     if (existing.length > 0) return;
            //
            //     var node = $(message.html);
            //     node.hide();
            //     $("#inbox").append(node);
            //     node.slideDown();
            // },
            // RefuseFight: function(challege) {
            //     var existing = $("#m" + message.id);
            //     if (existing.length > 0) return;
            //
            //     var node = $(message.html);
            //     node.hide();
            //     $("#inbox").append(node);
            //     node.slideDown();
            // },
        }
    }
};
$(document).ready(function() {
    // if (!window.console) window.console = {};
    // if (!window.console.log) window.console.log = function() {};

    console.log("websocket start------------->",Math.random());
    MySocket.open();
});

String.prototype.format = function () {
    var a = this;
    for (var k in arguments) {
        a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return a
};

// 包类型枚举
var PACKET_TYPE_MESSAGE = 'message';
var PACKET_TYPE_PING = 'ping';
var PACKET_TYPE_PONG = 'pong';
var PACKET_TYPE_TIMEOUT = 'timeout';
var PACKET_TYPE_CLOSE = 'close';

var MySocket = {
    socket: null,
    queuedPackets:[],
    open:function (msg) {
        if (!window.WebSocket) {
            window.WebSocket = window.MozWebSocket;
        }

        // Javascript Websocket Client
        if (window.WebSocket && !MySocket.socket) {
            $.when($.get('/brainking/tunnel')).then(function (data, textStatus, jqXHR) {
                var json = $.parseJSON(data);
                if ("data" in json && "connectUrl" in json.data) {
                    var data = json.data;
                    var connectUrl = data.connectUrl;
                    console.log(connectUrl);

                    MySocket.socket = new WebSocket(connectUrl);

                    MySocket.socket.onopen = function(event) {
                        if(msg){
                            MySocket.emitMessage(msg.msgid,msg.content);
                        }
                        MySocket.emitQueuedPackets();
                    };
                    MySocket.socket.onmessage = function(event) {
                        console.log("=============================",event);
                        var pos = event.data.indexOf(":");
                        if(pos<1){
                            console.log("=============================",pos);
                        }else{
                            var packet = JSON.parse(event.data.substr(pos+1));
                            console.log("=============================",packet);
                            switch (packet.type) {
                                case 'matched': //用户开始进行websocket连接，信道服务器连接成功后通知服务端
                                    MySocket.onMatched(packet);
                                    break;
                                case 'question':
                                    MySocket.onQuestion(packet);
                                    break;
                                case 'answer':
                                    MySocket.onAnswer(packet);
                                    break;
                                case 'finish':
                                    MySocket.onFinish(packet);
                                    break;
                                case 'invite':
                                    MySocket.onInvite(packet);
                                    break;
                                case 'close':
                                    // onClose(packet.tunnelId);
                                    break
                            }
                        }


                    };
                }
            }, function (XMLHttpRequest, textStatus, errorThrown) {
                console.log(XMLHttpRequest.status);
                console.log(XMLHttpRequest.readyState);
                console.log(textStatus);
                console.log(errorThrown);
            });

        }
    },
    start: function () {
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
    },
    sendPacket:function emitPacket(packet) {
        var encodedPacket = [packet.type];

        if (packet.content) {
            encodedPacket.push(JSON.stringify(packet.content));
        }
        console.log("tunnel send packet=>",packet);
        MySocket.socket.send(encodedPacket.join(':'));
        // wx.sendSocketMessage({
        //     data: encodedPacket.join(':'),
        //     fail: handleSocketError,
        // });
    },
    emitPacket:function emitPacket(packet) {
        console.log("emitPacket=》",packet);
        if (MySocket.socket.readyState!=1) {
            console.log("push msg to stack");
            MySocket.queuedPackets.push(packet);
        } else {
            MySocket.sendPacket(packet);
        }
    },
    emitMessage:function emitMessagePacket(messageType, messageContent) {
        var packet = {
            type: PACKET_TYPE_MESSAGE,
            content: {
                type: messageType,
                content: messageContent,
            },
        };

        MySocket.emitPacket(packet);
    },
    emitQueuedPackets: function emitQueuedPackets() {
        MySocket.queuedPackets.forEach(MySocket.emitPacket);

        // empty queued packets
        MySocket.queuedPackets.length = 0;
    },
    emitPingPacket: function emitPingPacket() {
        this.emitPacket({ type: PACKET_TYPE_PING });
    },
    emitClosePacket: function emitClosePacket() {
        this.emitPacket({ type: PACKET_TYPE_CLOSE });
    },
    decodePacket: function _decodePacketContent (packet) {
        let packetContent = {};
        if (packet.content) {
            try {
                packetContent = JSON.parse(packet.content)
            } catch (e) {}
        }

        const messageType = packetContent.type || 'UnknownRaw';
        const messageContent = ('content' in packetContent
            ? packetContent.content
            : packet.content
        );

        return { messageType, messageContent };
    },
    onMatched: function(packet) {
        var content = packet.content;
        console.log("onMatched===>",content);
        content.questions = {};
        content.quene = [];
        content.current = 0;

        for(var v in content.players){
            let player = content.players[v];
            player["myscore"] = 0;
            if(player.avatarUrl.indexOf("/")<0){
                player.avatarUrl = "/static/media/avatar/"+player.avatarUrl;
            }
        }
        var myid = $("#iframeId").data("userid");
        if(myid !== content.players[0].openId){
            content.myself = 1;
        }else{
            content.myself = 0;
        }

        // this.emitMessage("ready",{"Room":content.room});

        // localStorage.setItem(content.room, JSON.stringify(content.players));
        localStorage.setItem(content.room, JSON.stringify(content));
        $("#iframeId").attr("src", "/fight/match_opponent?room="+content.room);
    },
    onQuestion: function(packet) {
        var content = packet.content;
        console.log("onQuestion===>",content);
        var question = content.question;
        question.myanswer = {};
        question.atime = new Date().getTime();

        var strmatched = localStorage.getItem(content.room);
		var matched = JSON.parse(strmatched);
		console.log("storage===>",matched);
		matched.questions[question.id] = question;
		matched.quene.push(question.id);
		// if("question" in matched)
		//     matched.question.push(question);
		// else
		//     console.log(matched);
		console.log("item===>",matched);
		localStorage.setItem(content.room, JSON.stringify(matched));

		// var players = matched.players;
        //
        // var dk = $(window.parent.document).find("#iframeId").attr("src");
        // var url = $("#iframeId").attr("src");
        // console.log("current==>",url);
        //
        // $("#iframeId").contents().find(".question.flex.flex-v.flex-align-center text").html(question.ask);
        // // $(".question.flex.flex-v.flex-align-center text",document.frames['iframeId'].document).html(question.ask);
        // // $(".question.flex.flex-v.flex-align-center text").html(question.ask);
        //
        // var xhtml = "";
        // var obj = JSON.parse(question.answer);
        // for(var j in obj){
        //     xhtml += "<div class='options flex flex-v flex-align-center'>";
        //     xhtml += "<img src='/static/imgs/grdz_xx.png'>";
        //     xhtml += "<text>"+obj[j]+"</text>";
        //     xhtml += "</div>";
        // }
        // $("#iframeId").contents().find(".answer.flex.flex-v.flex-align-center").html(xhtml);
    },
    onAnswer: function(packet) {
        var content = packet.content;
        console.log("onAnswer===>",content);

        var strgamedat = localStorage.getItem(content.Room);
		// console.log("game data:======>",strgamedat);
		var gamedata = JSON.parse(strgamedat);

        var mychoose = content.MyChoose;
        if(mychoose.questionid in gamedata.questions) {
            var question = gamedata.questions[mychoose.questionid];
            question.myanswer[mychoose.openId] = mychoose;

            console.log("onAnswer==>",gamedata);
            localStorage.setItem(content.Room, JSON.stringify(gamedata));
        }else{
            console.log("onAnswer==>","no this question!!!");
            return;
        }

        // var score = mychoose.my_score;
        // rival_score += score;
        // console.log("")
        // var score2 = $(".rival2_score.flex.flex-v.flex-align-center text");
        // var process2 = $(".rival2_score.flex.flex-v.flex-align-center .process_son");
    },
    onFinish: function(packet) {
        var content = packet.content;
        console.log("onFinish==>",content.result);

        var strgamedat = localStorage.getItem(content.room);
		console.log("game data:------------->",strgamedat);
		var gamedata = JSON.parse(strgamedat);
		var players = gamedata.players;
		for(var v in content.result){
		    // console.log("dddddddddddd=>",v, content.result[v]);
		    for(var u in players){
		        if(players[u].openId === v){
		            players[u]["myscore"] = content.result[v];
		            break;
                }
            }
        }
		gamedata.rewards = content.result.rewards;
		console.log("onFinish==>",gamedata);
		localStorage.setItem(content.room, JSON.stringify(gamedata));
    },
    onInvite:function(packet) {
        var content = packet.content;
        console.log("onInvite==>",content);
        var fromid = content.fromid;
        var nickName = content.nickName;
        var myid = $("#iframeId").data("userid");
        var r = confirm('来自' + nickName + '挑战,是否接收');
        if (r == true) {
            parent.MySocket.emitMessage("join",{"fromid":myid,"gateid":"02001","taskid":fromid});
            $("#iframeId").attr("src", "/fight/friends_battle");
        }
        else{
            parent.MySocket.emitMessage("join",{"fromid":myid,"gateid":"02001","taskid":fromid});
        }
    },
    watchMessage: function(message) {
        MySocket.socket.send(JSON.stringify(message));
    }
};
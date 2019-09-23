
function $$(key) { return document.getElementById(key) };

var Utils = new Object();

/*==============================  Cookie 操 作 相 关  ==================================*/

/**
* 取Cookie
* name:名称 
* return:Cookie值
*/
Utils.getCookie = function(name) {
    var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
    if (arr != null) return decodeURI(arr[2]); return null;
}
/**
* 存Cookie
* name:Cookie名称
* return:Cookie值
*/
Utils.setCookie = function(name, value, days) {
    var Days = 60; //默认此 cookie 将被保存 60 天
    if (days) {
        Days = days;
    }
    var exp = new Date();    //new Date("December 31, 9998");
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + encodeURI(value) + ";path=/;expires=" + exp.toGMTString();
}
/**
* 删除cookie
* name:Cookie名称
*/
Utils.delCookie = function(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = this.getCookie(name);
    if (cval != null) document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}

Utils.delAllCookie = function() {
    var exp = new Date();
    exp.setTime(exp.getTime() - 10);
    var keys = document.cookie.match(/[^ =;]+(?=\=)/g);
    if (keys) {
        for (var i = keys.length; i--; )
            document.cookie = keys[i] + '=0;expires=' + exp.toUTCString()
    }
}

/*==============================  Cookie Eed  ==================================*/


Utils.browser = {
    scrollLeft: function() { return (document.documentElement.scrollLeft || window.pageXOffset) || 0; },
    scrollTop: function() { return (document.documentElement.scrollTop || window.pageYOffset) || 0; },
    height: function() { return (window.innerHeight) ? window.innerHeight : (document.documentElement && document.documentElement.clientHeight) ? document.documentElement.clientHeight : document.body.offsetHeight; },
    width: function() { return (window.innerWidth) ? window.innerWidth : (document.documentElement && document.documentElement.clientWidth) ? document.documentElement.clientWidth : document.body.offsetWidth; },
    isIE: function() { return ! -[1, ]; },
    isIE6: function() { return Utils.browser.isIE() && !window.XMLHttpRequest ? true : false; },
    isFF: function() { return window.navigator.userAgent.indexOf("Firefox") !== -1; },
    isChrome: function() { return window.navigator.userAgent.indexOf("Chrome") !== -1; },
    isOpera: function() { return !!window.opera; },
    isSafari: function() { return /a/.__proto__ == '//'; }
};

/*==============================  开 窗 操 作 相 关  ==================================*/
/**
* 打开对话窗
* url:     string, 链接
* caption: string, 开窗参数
* width:   number, 宽度
* height:  number, 高度
*/
Utils.open = function(url, caption, width, height) {
    var sw = this.browser.width;
    var sh = this.browser.height;
    if (!caption)
        caption = "_blank";
    if (!width)
        width = 600;
    if (!height)
        height = 480;
    window.open(url, caption, "width=" + width + ",height=" + height + ",top=" + ((sh - height) / 2 - 10) +
                ",left=" + ((sw - width) / 2) +
                ",toolbar=no, menubar=no, scrollbars=yes, resizable=no,location=no, status=no");
}


/** URL参数解码。
*   url, 格式为[<地址/文件>?]<参数名>=<值>&<参数名>=<值>
*   返回值：参数转换后的键值对
*/
Utils.urlDecode = function(url) {
    url = decodeURI(url);
    if (url.lastIndexOf("?") >= 0)
        url = url.substring(url.lastIndexOf("?") + 1);

    var obj = {};
    var pairs = url.split('&');
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split("=");
        obj[pair[0]] = pair[1];
    }
    return obj;
}

Utils.ConvertToDateByJson = function(jsonStr, type) {
    if (!/^\/Date\((\d+)\)\/$/.test(jsonStr)) return jsonStr;
    var _temp_date = null;
    if (!type) type = "dateTimeString";
    switch (type) {
        case "date":
            _temp_date = new Date(parseInt(RegExp.$1));
            break;
        case "dateString":
            _temp_date = Utils.GetDateString(new Date(parseInt(RegExp.$1)));
            break;
        case "dateTimeString":
            _temp_date = Utils.GetDateTimeString(new Date(parseInt(RegExp.$1)));
            break;
    }
    return _temp_date;
}

Utils.ConvertToWeek = function(date, type) {
    if (!type) type = 0;
    var weekId = date.getDay();
    var weekArr = weekArr = ['日', '一', '二', '三', '四', '五', '六'];
    if (type == 1) { weekArr.length = 0; ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']; }
    return weekArr[weekId];
}


//将日期对象转换成 yyyy-MM-dd 格式的日期字符串
Utils.GetDateString = function(date) {
    if (typeof (date) != "object") { date = parseInt(date); if (date) date = new Date(date); }
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    return year.toString() + "-" + (month > 9 ? month.toString() : "0" + month) + "-" + (day > 9 ? day.toString() : "0" + day);
}

//将日期对象转换成 yyyy-MM-dd HH:mm:ss 格式的日期字符串
Utils.GetDateTimeString = function(date) {
    if (typeof (date) != "object") { date = parseInt(date); if (date) date = new Date(date); }
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();
    return year.toString()
        + "-" + (month > 9 ? month.toString() : "0" + month)
        + "-" + (day > 9 ? day.toString() : "0" + day)
        + " " + (hour > 9 ? hour.toString() : "0" + hour)
        + ":" + (minute > 9 ? minute.toString() : "0" + minute)
        + ":" + (second > 9 ? second.toString() : "0" + second);
};



/**
* obj json对象
* str 转json字符串形式
* ajax 转post提交字符串形式
*/
Utils.ObjectToStr = function(obj, type) {
    ///	<summary>
    ///	json转字符串形式
    ///	</summary>
    ///	<returns type="string" />
    ///	<param name="obj" type="Object">
    ///		json对象
    ///	</param>
    ///	<param name="type" type="string">
    ///		type='str'转json字符串形式,  type='ajax' 转post提交字符串形式
    ///	</param>
    if (typeof (obj) != 'object') return obj;

    /*if (($.browser.msie == "Microsoft Internet Explorer" && $.browser.version != "6.0") && 1) {
        if (type.toLowerCase() == 'str' && JSON && typeof (JSON.stringify) == 'function') {
            return JSON.stringify(obj);
        }
    }*/
    var isKey = Object.prototype.toString.call(obj) === "[object Array]";
    var arr = [];
    var fmt = function(s) {
        if (typeof s == 'object' && s != null) return Utils.ObjectToStr(s, type);
        return /^(string|number)$/.test(typeof s) ? "'" + s + "'" : s;
    }
    if (!type) type = 'ajax';

    if (type.toLowerCase() == 'ajax') {
        for (var i in obj) arr.push(i + "=" + obj[i]);
        return arr.join('&');
    }
    if (type.toLowerCase() == 'str') {
        for (var i in obj) {
            if (isKey)
                arr.push(fmt(obj[i]));
            else
                arr.push("'" + i + "':" + fmt(obj[i]));
        }
        if (isKey)
            return '[' + arr.join(',') + ']';
        else
            return '{' + arr.join(',') + '}';
    }
};


//获取元素坐标
Utils.GetPoint = function(source) {
    ///	<summary>
    ///	获取元素坐标
    ///	</summary>
    ///	<returns type="json" />
    ///	<param name="source" type="Object">
    ///		html元素 返回json对象 列: { x: 0, y: 0 }
    ///	</param>
    var pt = { x: 0, y: 0 };
    do {
        pt.x += source.offsetLeft;
        pt.y += source.offsetTop;
        source = source.offsetParent;
    }
    while (source); 
    return pt;
}

Utils.UnicodeToAscii = function(value) {
    var code = value.match(/&#(\d+);?/g);
    if (code == null) { return value; }
    for (var i = 0; i < code.length; i++) {
        value = value.replace(code[i], String.fromCharCode(code[i].replace(/[&#;]/g, '')));
    }
    return value;
}

/*==============================  字 符 串 处 理 相 关  ==================================*/

///	<summary>
///	字符串去掉首尾部空格
///	</summary>
///	<returns type="string" />
String.prototype.trim = function() {
    return this.replace(/^\s+|\s+$/g, '');
}
/**
* 字符串转Json对象
* value Json字符串 
* return:Json对象 
* var json = ''.toJson()
*/
String.prototype.toJson = function() {
    try {
        if (!this || this == "")
            return null;
        var str = this.replace(/\r\n/g, '');
        var obj = (new Function("return " + str))();
        if (obj) return obj;
        //alert("转换JSON失败!");
        return null;
    } catch (ex) { 
        var s = ex;
        return null;
    }
}

String.prototype.format = function() {
    var reg;
    var args;
    if (arguments[0] && typeof (arguments[0]) == "object") {
        reg = new RegExp("\\{(\\w*)\\}", "g");
        args = arguments[0];
    }
    else {
        reg = new RegExp("\\{(\\d+)\\}", "g");
        args = arguments;
    }
    return this.replace(reg, function() {
        var val = typeof (args[arguments[1]]) == "function" ? new Function(args[arguments[1]])() : args[arguments[1]];
        return val == undefined ? arguments[0] : val;
        /*arguments: //.replace(/\(.*\)/, '')
        0:匹配的字符串
        1:匹配的字符串的下标或key
        2.this对象
        3.caller
        */
    });
};

//'id={0},name={1}'.format(1,'ttt')  -- id=i,name=ttt
//'t_id={id},t_name={name}'.format({ id: 1, name: 'ttt' }); -- 't_id=1,t_name=ttt'

Utils.getType = function (o, t) {
    if (!o) { return false;}
    if (t) {
        var fn = {
            isType: function (obj, type) { return Object.prototype.toString.call(obj) === "[object " + type + "]"; },
            array: function (obj) { return this.isType(obj, "Array"); },
            bool: function (obj) { return this.isType(obj, "Boolean"); },
            date: function (obj) { return this.isType(obj, "Date"); },
            number: function (obj) { return this.isType(obj, "Number"); },
            object: function (obj) { return (this.isType(obj, "Object") || this.isType(obj, "Array")); },
            regExp: function (obj) { return this.isType(obj, "RegExp"); },
            string: function (obj) { return this.isType(obj, "String"); },
            element: function (obj) { return !!(obj && obj.nodeType == 1); },
            _function: function (fn) { return !!fn && !fn.nodeName && fn.constructor != String && fn.constructor != RegExp && fn.constructor != Array && /function/i.test(fn + ""); }
        }
        if (t == 'function') { t = "_" + t; }
        return fn[t](o) ? true : false;
    } else {
        if (Object.prototype.toString.call(o) === "[object String]") return 'string';
        if (Object.prototype.toString.call(o) === "[object Array]") return 'object';
        if (Object.prototype.toString.call(o) === "[object Object]") return 'object';
        if (Object.prototype.toString.call(o) === "[object Boolean]") return 'boolean';
        if (Object.prototype.toString.call(o) === "[object Date]") return 'date'; 
        if (Object.prototype.toString.call(o) === "[object Number]") return 'number';
        if (Object.prototype.toString.call(o) === "[object Function]") return 'function';
    }
    return null;
};


/*==============================  Ajax 数 据 请 求 相 关  ==================================*/

var Ajax = function (url, method, params, contentType, onload, onerror) {
    this.httpRequest = null;
    this.onload = (onload) ? onload : Ajax.defaultCallback;
    this.onerror = (onerror) ? onerror : Ajax.defaultError;
    this._request(url, method, params, contentType);
};
Ajax.prototype._request = function (url, method, params, contentType) {
    if (window.ActiveXObject) {
        this.httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
    } else {
        this.httpRequest = new XMLHttpRequest();
    }
    if (this.httpRequest) {
        try {
            var ajax = this;
            this.httpRequest.onreadystatechange = function () {
                if (ajax.httpRequest.readyState == 4) {
                    if (ajax.httpRequest.status == 200) {
                        ajax.onload.call(ajax.httpRequest);
                    }
                    else {
                        ajax.onerror.call(ajax.httpRequest);
                    }
                    ajax.httpRequest = null;
                }
            };
            this.httpRequest.open(method, url, true);
            this.httpRequest.setRequestHeader("Cache-Control", "no-cache");
            this.httpRequest.setRequestHeader("Content-Type", contentType);
            this.httpRequest.setRequestHeader("Accept", contentType);
            this.httpRequest.setRequestHeader("X-Requested-With", "XMLHttpRequest");
            this.httpRequest.send(params);
        }
        catch (err) {
            alert("AJAX 调用失败: " + err.message);
            this.httpRequest = null;
        }
    }
    else {
        alert("XMLHttpRequest对象创建失败");
    }
};
Ajax.ErrorInfo = "";
Ajax.defaultError = function () { Ajax.ErrorInfo = ("AJAX 调用失败：\n\n" + "readyState：" + this.readyState + "\nstatus： " + this.status + "\nheaders：\n " + this.getAllResponseHeaders()); };
Ajax.defaultCallback = function () { alert("AJAX调用成功， 返回数据为：" + this.responseText); };
Ajax.ContentType = new Object();
Ajax.ContentType.HTML = "application/X-www-form-urlencoded;charset=utf-8";
Ajax.responseText = "";
/*操作类型*/
Ajax.m_action = "";
/*序列号数据格式类型"tab,row,html"*/
Ajax.m_dtype = "html";
Ajax.request = function (url, data, success, failure) {
    if (!url) { alert("请求路径不能为空!"); return; }
    if (typeof data === 'object') {
        data = Utils.ObjectToStr(data, 'str');
    }
    Ajax.responseText = ""; Ajax.ErrorInfo = "";
    var _urlparames = 'dType=' + this.m_dtype + '&action=' + this.m_action + "&ClientID=" + $$("ClientID").value;
    url += url.indexOf('?') > 0 ? "&" : "?" + _urlparames;
    //var _url = "{0}{1}{2}".format(url, url.indexOf('?') > 0 ? "&" : "?", _urlparames);
    new Ajax(url, "POST", data, Ajax.ContentType.HTML, function () {
        var json = this.responseText.toJson();
        Ajax.responseText = json;
        if (json.Result) {
            if (success) { success(json.Object); }
        } else {
            if (json.Message) {
                Utils.alert(json.Message);
            }
            if (json.Fun) {
                if (/function/i.test(json.Fun))
                {
                    new Function('json.Fun({0});'.format(json.Object))();
                }
            }
        }
    }, failure);
};

Utils.onPageLoad = null;
Utils.isExecPageLoad = false;
if (document.onreadystatechange) {
    document.onreadystatechange = function () {
        if (document.readyState == "complete") {
            if (Utils.getType(Utils.onPageLoad, 'function') && !Utils.isExecPageLoad) {
                Utils.isExecPageLoad = true;
                Utils.onPageLoad();
            }
        }
    }
} else if (document.addEventListener) {
    var funLoad = function () {
        if (Utils.getType(Utils.onPageLoad, 'function') && !Utils.isExecPageLoad) {
            Utils.isExecPageLoad = true;
            Utils.onPageLoad();
        }
    };
    window.addEventListener("load", funLoad, false);
}

Utils.headFun = function (d) {
    d = d.toJson();
    if (d["head"]) {
        if (d["head"]["errCode"] == 0) {
            return d["body"];
        } else {
            Utils.alert(d["head"]["errMsg"]);
            return false;
        }
    }
}
Utils.alert = function (errMsg, title, fun) {
    if (!errMsg) { return; };
    $$('overlayAll').style.display = "block";
    $$('my_errMsg').style.display = "block";
    $$('my_errMsg').setAttribute("class", "my_errMsg my_errMsg_animation_show");
    $$('overlayAll').style.height = document.body.offsetHeight + "px";
    var mfun = function () {
        //$$('my_errMsg').style.display = "none";
        $$('overlayAll').style.display = "none";
    };
    $$('errTtile').innerHTML = title || '系统提示！';
    $$('errContent').innerHTML = errMsg;
    var bodyHeight = window.document.documentElement["clientHeight"] || window.document.body["clientHeight"];
    //$$('my_errMsg').style.top = (parseInt((bodyHeight - $$('my_errMsg').offsetHeight) / 2) + document.body.scrollTop - 20) + 'px';
    $$('my_errMsg_but').onclick = function () {
        if (Utils.getType(fun, 'function')) {
            fun();
            mfun();
        }
        else {
            mfun();
        }

        $$('my_errMsg').setAttribute("class", "my_errMsg my_errMsg_animation_close");
    };
}

Utils.alert2 = function (errMsg, title, fun, fun2) {
    if (!errMsg) { return; };
    $$('overlayAll').style.display = "block";
    $$('my_errMsg').style.display = "block";
    $$('my_errMsg').setAttribute("class", "my_errMsg my_errMsg_animation_show");
    $$('overlayAll').style.height = document.body.offsetHeight + "px";
    var mfun = function () {
        //$$('my_errMsg').style.display = "none";
        $$('overlayAll').style.display = "none";
        $$('my_errMsg_but').parentNode.removeChild($$("my_errMsg_spanTemp_but"));
        $$('my_errMsg_but').parentNode.removeChild($$("my_errMsg_cancel_but"));
    };

    $$('errTtile').innerHTML = title || '系统提示！';
    $$('errContent').innerHTML = errMsg;
    var bodyHeight = window.document.documentElement["clientHeight"] || window.document.body["clientHeight"];
    $$('my_errMsg').style.top = (parseInt((bodyHeight - $$('my_errMsg').offsetHeight) / 2) + document.body.scrollTop - 20) + 'px';
    var parentNodeBut = $$('my_errMsg_but').parentNode;
    parentNodeBut.style.width = "230px";

    var spanTemp = document.createElement("span");
    spanTemp.id = "my_errMsg_spanTemp_but";
    spanTemp.innerHTML = " &nbsp; &nbsp; ";
    spanTemp.className = "errbutspanTemp";
    parentNodeBut.appendChild(spanTemp);

    var cancelBut = document.createElement("span");
    cancelBut.id = "my_errMsg_cancel_but";
    cancelBut.innerHTML = "取  消";
    cancelBut.className = "errbutspan";
    parentNodeBut.appendChild(cancelBut);

    $$('my_errMsg_cancel_but').onclick = function () {
        if (Utils.getType(fun2, 'function')) {
            fun2();
            mfun();
        }
        else {
            mfun();
        }
        $$('my_errMsg').setAttribute("class", "my_errMsg my_errMsg_animation_close");
    };
    $$('my_errMsg_but').onclick = function () {
        if (Utils.getType(fun, 'function')) {
            fun();
            mfun();
        }
        else {
            mfun();
        }
        $$('my_errMsg').setAttribute("class", "my_errMsg my_errMsg_animation_close");
    };
}

var mylog = {};
mylog.m_log = "";
mylog.time = function() {
    var _date = new Date();
    return _date.getFullYear() + "-" + _date.getMonth() + "-" + _date.getDay() + "-" + _date.getHours() + "-" + _date.getMinutes() + "-" + _date.getSeconds() + "-" + _date.getMilliseconds();
};

mylog.write = function(str) { this.m_log += this.time() + "  " + str + "\n" };

mylog.alert = function () { alert(this.m_log); };


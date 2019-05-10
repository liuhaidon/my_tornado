$(document).ready(function () {

//后台表格js
    (function () {
        $('.btn.btn-w-m').prop('disabled', true);
        var a = $('#userListCheck'),
            m = $('#storeListCheck'),
            b = $('tr.gradeX input[type="checkbox"]'),
            c = $('tr.gradeX input[type="checkbox"],#userListCheck'),
            f = $('tr.gradeX input[type="checkbox"],#storeListCheck'),
            d = $('.btn.btn-w-m'),
            e = function () {
                var a = 0;
                $.each(b, function () {
                    if ($(this).prop('checked')) a++;
                    console.log("aaa",a)
                });
                if (a > 0) {
                    $('.btn.btn-w-m').prop('disabled', false);
                } else {
                    $('.btn.btn-w-m').prop('disabled', true);
                }
            };

            o = function (){
                var m = 0;
                $.each(b, function () {
                    if ($(this).prop('checked')) m++;
                    console.log("mmm",m)
                });
                if (m > 0) {
                    $('.btn.btn-w-m').prop('disabled', false);
                } else {
                    $('.btn.btn-w-m').prop('disabled', true);
                }
            };
        console.log("fffff",f,f.length)
        console.log("ccccc",c,c.length)
        a.click(function () {
            if ($(this).prop('checked')) {
                b.prop('checked', true);
            } else {
                b.prop('checked', false);
            }
        });
        m.click(function () {
            if ($(this).prop('checked')) {
                b.prop('checked', true);
            } else {
                b.prop('checked', false);
            }
        });

        c.click(function () {
            console.log("c+++",c);
            e();
        });
        f.click(function () {
            console.log("f+++",f);
            o();
        });

        $('.btn.btn-white').click(function () {
            if ($(this).data("type") != 'review') {
                $('tr.gradeX input[type="checkbox"]').each(function (k, v) {
                    if ($(v).prop('checked')) {
                        $(v)[0].parentNode.parentNode.outerHTML = '';
                    }
                });
            }
            $('.btn.btn-w-m').prop('disabled', true);
        });
        /*$('.btn.btn-primary').click(function () {
         $('tr.gradeX input[type="checkbox"]').each(function(k,v){
         $(v).prop('checked',false);
         });
         });*/

    })();

});


//btn1删除按钮  msgClss弹窗的p标签  msg1弹窗前缀内容 函数返回选中的所有id
function _alert(btn1, msgClss, msg1) {
    var j = {};
    console.log("点击删除",btn1, msgClss, msg1);
    $(btn1).click(function () {
        var n = new Array(), msg = '';
        $('tr.gradeX input[type="checkbox"]').each(function (k, v) {
            if ($(v).prop('checked')) {
                // n.push($(v).parent().parent().children('.userListId').text());
                n.push($(v).parent().parent().children('.userListId').data("id"));
                console.log("选中我了")
            }
        });
        for (var i in n) {
            j[i] = n[i];
            msg += n[i] + ',';
        }
        JSON.stringify(j);
        if (msg != '') {
            $(msgClss).html(msg1 + '<span style="color:red;font-weight: bold">' + msg + '</span>');
        } else {
            $(btn1).prop('disabled', true);
            console.log("选中我了2")
        }
    });
    return j;
}

function _alert1(btn1, msgClss, msg1) {
    var j = {};
    console.log("点击删除",btn1, msgClss, msg1);
    $(btn1).click(function () {
        console.log("我点击了");
        var n = new Array(), msg = '';
        $('tr.gradeX input[type="checkbox"]').each(function (k, v) {
            if ($(v).prop('checked')) {
                // n.push($(v).parent().parent().children('.userListId').text());
                n.push($(v).parent().parent().children('.storeListId').data("id"));
                cosnoe.log("已经有选中的了");
            }
        });
        for (var i in n) {
            j[i] = n[i];
            msg += n[i] + ',';
        }
        JSON.stringify(j);
        if (msg != '') {
            $(msgClss).html(msg1 + '<span style="color:red;font-weight: bold">' + msg + '</span>');
        } else {
            $(btn1).prop('disabled', true);
        }
    });
    return j;
}

function listNubmer() {
    var n = new Array(), j = {};
    $('tr.gradeX input[type="checkbox"]').each(function (k, v) {
        if ($(v).prop('checked')) {
            n.push($(v).parent().parent().children('.userListId').text());
        }
    });
    for (var i in n) {
        j[i] = n[i];
    }
    JSON.stringify(j);
    return j;
}

String.format = function(str) {
	var args = arguments;
	var re = new RegExp("%([1-" + args.length + "])", "g");
	// for(var i=0;i<args.length;i++)
	// 	alert(args[i]);
	return String(str).replace(re,function($1, $2) {return args[$2];});
};


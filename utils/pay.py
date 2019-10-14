#!/usr/bin/env python
# -*- coding:utf-8 -*-

from BaseHandler import BaseHandler
import time
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib import quote_plus
# from urllib.parse import urlparse, parse_qs
# from urllib.request import urlopen
import sys
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )


class AdminIndex(BaseHandler):
    def get(self):
        self.render('index.html')


class AdminPay(BaseHandler):
    def post(self):
        print self.request.arguments
        a = "x2" + str(time.time())
        subject = self.get_argument("subject", "充气娃娃")
        out_trade_no = self.get_argument("out_trade_no", a)
        total_amount = float(self.get_argument("money", 0))
        print total_amount

        alipay = AliPay(
            # appid="2019060165474076",
            appid="2016092300578223",
            app_notify_url="http://127.0.0.1:8080/aysic",
            app_private_key_path=u"app_private_key.txt",
            alipay_public_key_path=u"alipay_public_key.txt",
            debug=True,  # 默认False,
            return_url="http://127.0.0.1:8080/result"
        )
        query_params = alipay.direct_pay(
            subject=subject,
            out_trade_no=out_trade_no,
            total_amount=total_amount,)
        # if alipay.debug is True:
        #     pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
        # else:
        #     pay_url = "https://openapi.alipay.com/gateway.do?{0}".format(query_params)
        self.redirect(pay_url)


class AliPay(object):
    """支付宝支付接口"""
    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        self.debug = debug
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.importKey(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        # if return_url is not None:
        if return_url:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        if "sign" in data:
            data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = b64encode(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, b64decode(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


class AdminAysic(BaseHandler):
    def get(self):
        print "执行呀"
        self.render('aaa.html')


# class AdminResult(BaseHandler):
#     def get(self):
#         print "好的"
#         self.render('bbb.html')
class AdminResult(BaseHandler):
    def get(self, *args, **kwargs):
        """
        处理支付宝的return_url返回
        :param request:
        :return:
        """
        res_data = {}
        processed_dict = {}
        req_data = self.request.arguments
        req_data = format_arguments(req_data)
        for key, value in req_data.items():
            processed_dict[key] = value[0]

        sign = processed_dict.pop("sign", None)
        alipay = AliPay(
            appid=settings["ALI_APPID"],
            app_notify_url="{}/alipay/return/".format(settings["SITE_URL"]),
            app_private_key_path=settings["private_key_path"],
            alipay_public_key_path=settings["ali_pub_key_path"],
            debug=True,
            return_url="{}/alipay/return/".format(settings["SITE_URL"])
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            res_data["content"] = "success"
        else:
            res_data["content"] = "Failed"

        self.finish(res_data)

    def post(self, *args, **kwargs):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        req_data = self.request.body_arguments
        req_data = format_arguments(req_data)
        for key, value in req_data.items():
            processed_dict[key] = value[0]

        sign = processed_dict.pop("sign", None)
        alipay = AliPay(
            appid=settings["ALI_APPID"],
            app_notify_url="{}/alipay/return/".format(settings["SITE_URL"]),
            app_private_key_path=settings["private_key_path"],
            alipay_public_key_path=settings["ali_pub_key_path"],
            debug=True,
            return_url="{}/alipay/return/".format(settings["SITE_URL"])
        )

        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no')
            trade_no = processed_dict.get('trade_no')
            trade_status = processed_dict.get('trade_status')

            orders_query = OrderInfo.update(
                pay_status=trade_status,
                trade_no=trade_no,
                pay_time=datetime.now()
            ).where(
                OrderInfo.order_sn == order_sn
            )
            # await self.application.objects.execute(
            #     orders_query
            # )

        self.finish("success")
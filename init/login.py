# -*- coding=utf-8 -*-
import copy
import time
from collections import OrderedDict
from time import sleep
import TickerConfig
from inter.GetPassCodeNewOrderAndLogin import getPassCodeNewOrderAndLogin1
from inter.GetRandCode import getRandCode
from inter.LoginAysnSuggest import loginAysnSuggest
from inter.LoginConf import loginConf
from myException.UserPasswordException import UserPasswordException


class GoLogin:
    def __init__(self, session, is_auto_code, auto_code_type):
        self.session = session
        self.randCode = ""
        self.is_auto_code = is_auto_code
        self.auto_code_type = auto_code_type

    def auth(self):
        """
        模拟登陆
            登录页面：
                _passport_session、_passport_ct
                loginInitCdn1: /otn/resources/login.html
            登录接口：
                uamtkStaticUrl： /passport/web/auth/uamtk-static

        :return:
        """
        self.session.httpClint.send(self.session.urls["loginInitCdn1"])
        uamtkStaticUrl = self.session.urls["uamtk-static"]
        uamtkStaticData = {"appid": "otn"}
        return self.session.httpClint.send(uamtkStaticUrl, uamtkStaticData)

    def codeCheck(self):
        """
        验证码校验
        :return:
        """
        codeCheckUrl = copy.deepcopy(self.session.urls["codeCheck1"])
        codeCheckUrl["req_url"] = codeCheckUrl["req_url"].format(self.randCode, int(time.time() * 1000))
        fresult = self.session.httpClint.send(codeCheckUrl)
        if not isinstance(fresult, str):
            print("登录失败")
            return
        fresult = eval(fresult.split("(")[1].split(")")[0])
        if "result_code" in fresult and fresult["result_code"] == "4":
            print(u"验证码通过,开始登录..")
            return True
        else:
            if "result_message" in fresult:
                print(fresult["result_message"])
            sleep(1)
            self.session.httpClint.del_cookies()

    def baseLogin(self, user, passwd, res=None):
        """
        登录过程
        :param user:
        :param passwd:
        :return: 权限校验码
        """
        logurl = self.session.urls["login"]

        loginData = OrderedDict()
        loginData["username"] = user,
        loginData["password"] = passwd,
        loginData["appid"] = "otn",
        loginData["answer"] = self.randCode,

        tresult = self.session.httpClint.send(logurl, loginData)
        if 'result_code' in tresult and tresult["result_code"] == 0:
            print(u"登录成功")
            tk = self.auth()
            if "newapptk" in tk and tk["newapptk"]:
                return tk["newapptk"]
            else:
                return False
        elif 'result_message' in tresult and tresult['result_message']:
            messages = tresult['result_message']
            if messages.find(u"密码输入错误") is not -1:
                res['msg']=messages
                res['flag'] = True
                # raise UserPasswordException("{0}".format(messages))
            elif messages.find(u"您的手机号码尚未进行核验") is not -1:
                res['msg'] = messages
                res['flag']=True
            else :
                print(u"登录失败: {0}".format(messages))
                print(u"尝试重新登陆")
                return False
        else:
            return False

    def getUserName(self, uamtk):
        """
        登录成功后,显示用户名
        :return:
        """
        if not uamtk:
            return u"权限校验码不能为空"
        else:
            uamauthclientUrl = self.session.urls["uamauthclient"]
            data = {"tk": uamtk}
            uamauthclientResult = self.session.httpClint.send(uamauthclientUrl, data)
            if uamauthclientResult:
                if "result_code" in uamauthclientResult and uamauthclientResult["result_code"] == 0:
                    print(u"欢迎 {} 登录".format(uamauthclientResult["username"]))
                    # by sw
                    # org: return True
                    return uamauthclientResult["username"]
                else:
                    return False
            else:
                self.session.httpClint.send(uamauthclientUrl, data)
                url = self.session.urls["getUserInfo"]
                self.session.httpClint.send(url)

    def go_login(self,resultMap={}):
        """
        登陆
        :param user: 账户名
        :param passwd: 密码
        :return:
        """

        user, passwd = TickerConfig.USER, TickerConfig.PWD
        # by sw
        print("now logining ==> username:{0} password:{1}".format(user,passwd))

        if not user or not passwd:
            resultMap['status']=100
            resultMap['tips']="温馨提示: 用户名或者密码为空，请仔细检查"
            raise UserPasswordException(u"温馨提示: 用户名或者密码为空，请仔细检查")
        login_num = 0
        while True:
            if loginConf(self.session):

                result = getPassCodeNewOrderAndLogin1(session=self.session, imgType="login")
                if not result:
                    continue
                self.randCode = getRandCode(self.is_auto_code, self.auto_code_type, result)
                print(self.randCode)
                login_num += 1
                self.auth()
                if self.codeCheck():
                    resultMap['status']=200
                    uamtk = self.baseLogin(user, passwd,resultMap)
                    resultMap['uamtk']=uamtk
                    if resultMap.get("flag"):
                        resultMap['status']=500
                        break
                    if uamtk:
                        name=self.getUserName(uamtk)
                        resultMap['username']=name
                        break
            else:
                loginAysnSuggest(self.session, username=user, password=passwd)
                login_num += 1
                break
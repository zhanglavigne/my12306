import os
from mymodel import ClientInfo

def station_table():
    """
            读取车站信息
            :param station:
            :return:
            """
    path = os.path.join(os.path.dirname(__file__), '../station_name.txt')
    try:
        with open(path, encoding="utf-8") as result:
            info = result.read().split('=')[1].strip("'").split('@')
    except Exception:
        with open(path) as result:
            info = result.read().split('=')[1].strip("'").split('@')
    del info[0]
    station_name = {}
    for i in range(0, len(info)):
        n_info = info[i].split('|')
        station_name[n_info[1]] = n_info[2]
    print(station_name)
    return station_name

def wrapResponse(req_cookies={},cookies={},res={}):
    response=ClientInfo.userInfo()
    response.cookies=cookies
    response.req_cookies=req_cookies
    return response

def requestCookieJarToDict(cookiesJar):
    cookieDict={}
    for item in cookiesJar:
        item=str(item).split(' ')[1].split('=')
        cookieDict[item[0]]=item[1]
    return cookieDict

if __name__=='__main__':
    station_table()
from flask import Flask,request,jsonify
from init import select_ticket_info
import json
from config import getCookie
from forApi.apiUtils import *
from inter.LiftTicketInit import liftTicketInit
from mymodel import ClientInfo
from apiRespon import *
from inter import Query
import TickerConfig
import time
app=Flask(__name__)



@app.route("/tiketLeft")
def getLiftTicketInit():
    s=select_ticket_info.select()

@app.route("/",methods=["post"])
def index():
    user=request.form.get("user.name")
    print(user)
    return jsonify(user)

@app.route("/stationNameInfo",methods=["get"])
def getStationNameInfo():
    station_name_info=station_table()
    return jsonify(station_name_info)


@app.route("/queryTicket",methods=["post"])
def queryTickets():
    respInfo=ClientInfo.userInfo()
    select=getSelect()
    l = liftTicketInit(select)
    l.reqLiftTicketInit()
    getCookie.getDrvicesID(select)
    queryJsonStr=request.form.get("queryStr")
    data={}
    if queryJsonStr is None:
        data['status']=505
        data['tips']='None'
    queryJson=json.loads(queryJsonStr)
    print(queryJson)
    q=Query.query(selectObj=select,
                  from_station=queryJson.get("from"),
                  to_station=queryJson.get("to"),
                  from_station_h=queryJson.get("fromH"),
                  to_station_h=queryJson.get("toH"),
                  _station_seat=queryJson.get("seatType"),
                  station_trains=queryJson.get("num"),
                  station_dates=queryJson.get("dates"),
                  ticke_peoples_num=queryJson.get("numOfPassengers")
                  )
    ticketInfo=[]
    queryResult=q.sendQuery(ticketInfo)
    # info={}
    data={}
    data['status']=500
    if len(ticketInfo)>0:
        data['status']=200
        data['data']=ticketInfo
    '''
    if queryResult.get("status"):
        data['status']=200
        info['train_no'] = queryResult.get("train_no", "")
        info['train_date'] = queryResult.get("train_date", "")
        info['stationTrainCode'] = queryResult.get("stationTrainCode", "")
        info['secretStr'] = queryResult.get("secretStr", "")
        info['secretList'] = queryResult.get("secretList", "")
        info['seat'] = queryResult.get("seat", "")
        info['leftTicket'] = queryResult.get("leftTicket", "")
        info['query_from_station_name'] = queryResult.get("query_from_station_name", "")
        info['query_to_station_name'] = queryResult.get("query_to_station_name", "")
        info['is_more_ticket_num'] = queryResult.get("is_more_ticket_num", len(TickerConfig.TICKET_PEOPLES))
        data['info']=info
    '''
    respInfo.rep=data

    return json.dumps(respInfo.__dict__)



@app.route("/getPassengers",methods=["post"])
def getPassengers():
    respInfo = ClientInfo.userInfo()
    select=select_ticket_info.select()
    # time.sleep(0.005)
    token=json.loads(request.form.get("token"))
    # for k,v in token.items():
    #     print("k:{0}  v:{1}".format(k,v))

    select.httpClint.set_cookies_by_dict(token)
    TickerConfig.TICKET_PEOPLES=['苏少伟']
    s=select_ticket_info.getPassengerDTOs(selectObj=select,ticket_peoples=TickerConfig.TICKET_PEOPLES)
    data={}
    passenger=s.sendGetPassengerDTOs(data)
    return json.dumps(data)
    # return ""

@app.route("/login",methods=["post"])
def login():
    respInfo=ClientInfo.userInfo()
    dt={}
    dt['username']=request.form.get('username')
    dt['password']=request.form.get('password')
    select=select_ticket_info.select()
    # 模拟浏览器获得2个属性
    getCookie.getDrvicesID(select)
    TickerConfig.USER=dt['username']
    TickerConfig.PWD=dt['password']
    res={}
    select.call_login(result=res)
    print(select.httpClint.get_cookies_itself())
    respInfo.req_cookies=requestCookieJarToDict(select.httpClint.get_cookies_itself())
    respInfo.cookies=select.cookies
    respInfo.rep=res
    import threading

    from inter import CheckUser
    cu=CheckUser.checkUser(select);
    t=threading.Thread(target=cu.sendCheckUser)
    t.setDaemon(True)
    # t.start()
    return json.dumps(respInfo.__dict__)

def getSelect(token=None):
    select=select_ticket_info.select()
    if token:
        token = json.loads(token)
        select.httpClint.set_cookies_by_dict(token)
    return select

if __name__=='__main__':
    app.run()
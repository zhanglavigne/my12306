from flask import Flask,request
import json
app=Flask(__name__)



@app.route("/",methods=['POST','GET'])
def index():
    tip=' request  '
    if request.method=='POST':

        """
        get date from request url:
            request.args.get('name')
        get data from request-body
        there hava tow method can get data
        method one :
            request.form['name']
            but this will throw exception if the sepcify  arg not exist 
        
        """
        dt={}
        dt['username']=request.form.get("name")
        dt['password']=request.form.get("password")
        #dick to json
        string = json.dumps(dt)
        #json to pojo
        jsonStr=request.form.get('jsonStr')
        jsonDt=json.loads(jsonStr)
        string=json.dumps(jsonDt)

        print('username: '+dt['username']+'  password: '+dt['password'])
        print('username: '+jsonDt['username']+'  password: '+jsonDt['password'])
        return tip+string
    return tip+'GET'

if __name__=='__main__':
    app.debug=True
    app.run()
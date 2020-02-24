import json
class userInfo:
    def __init__(self):
        self.cookies={'userInfo':'info'}
        self.req_cookies={'header':'usd'}
        self.rep={}
        self.req_args={}


if __name__=='__main__':
    ui=userInfo()
    print(json.dumps(ui.__dict__))



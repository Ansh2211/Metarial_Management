import requests

def SendMessage(msg,mobilenumber):
    url = "http://167.144.117.218/GatewayAPI/rest"
    headers = {"Cache-Control" : "no-cache", "Content-Type" : 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    data = {"loginid": 'VIKSDIWS',"password": 'xxxxxxxx',"msg": msg,"send_to": mobilenumber, "senderId": 'VIKSDIWS',"routerId": '8',"smsContentType": 'english'}
    response = requests.post(url=url,headers=headers,data=data)
    return response
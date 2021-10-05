#######################################################################
# Author  : Raghu Ram ALLA
# Date    : 05-October-2021
# Purpose : Automate the process of generating access token for kiteconnect in python3. 
# For this code to run you have to enable TOTP for 2FA
# Special Thanks to Devesh Shukla
############################################################################

import requests,json
import pyotp
from kiteconnect import KiteConnect, KiteTicker

def kiteLogin():
    api_key             = 'api_key'
    api_secret          = 'api_secret'
    zerodha_id          = 'zerodha_id'
    zerodha_password    = 'zerodha_password'
    totp_key            = 'totp_key'

    totp                = pyotp.TOTP(totp_key)
    req_session         = requests.Session()
    loginurl            = "https://kite.zerodha.com/api/login"
    twofaUrl            = "https://kite.zerodha.com/api/twofa"
    request_id          = eval(req_session.post(loginurl, {"user_id":zerodha_id, "password":zerodha_password}).text)["data"]["request_id"]
    totp_pswd           = totp.now()
    zerodha_login       = req_session.post(twofaUrl, {"user_id":zerodha_id, "request_id":request_id, "twofa_value":totp_pswd})
    zerodha_api_ssn     = req_session.get("https://kite.trade/connect/login?api_key="+api_key)
    zerodha_api_ssn     = zerodha_api_ssn.url.split("request_token=")
    request_token       = zerodha_api_ssn[1].split("&")[0]
    kite                = KiteConnect(api_key=api_key)
    gen_ssn             = kite.generate_session(request_token, api_secret)
    access_token        = gen_ssn['access_token']
    print(gen_ssn)

    # save token to text file
    with open('access_token.txt', 'w') as file:
        file.write(access_token)

if __name__=="__main__": 
    kiteLogin()

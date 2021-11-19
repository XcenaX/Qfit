from qfit.settings import *
import requests

def send_smsc(to, message):
    #https://smsc.kz/sys/send.php?login=<login>&psw=<password>&phones=<phones>&mes=<message>
    url = SMSC_URL + "?login=" + SMSC_LOGIN + "&psw=" + SMSC_PASSWORD + "&phones=" + to + "&mes=" + message + "&sender=QFit.kz"
    url2 = SMSC_URL + "?login=" + SMSC_LOGIN + "&psw=" + SMSC_PASSWORD + "&phones=" + to + "&mes=" + message
    
    
    if to[1] != "7":
        res = requests.get(url2)
    else:
        res = requests.get(url)

send_smsc("79827878507", "Test")
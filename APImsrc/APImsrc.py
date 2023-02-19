import requests
import json
import datetime


def report_to_mrsc (url):
    date = str(datetime.datetime.now())
    hour = date[11:19]
    today = date[:10]
    #Diccionario en Python para facilitar la modificacion de los parametros
    company = input('Ingrese el nombre de la compañia suplantada ')
    parameters = {
    "date": today,
    "time": hour,
    "timeZone": "-0500",
    "reporterEmail": "quinkings7@hmail.com",
    "reporterName": "Appgate Company",
    "reportNotes": "Phishing Site against " + company, #se debe aceptar el ingreso de cliente 
    "threatType": "URL",
    "incidentType": "Phishing",
    "sourceUrl": url,
    "testSubmission": False
    }

    json_parameters = json.dumps(parameters)
    resp = requests.post('https://api.msrc.microsoft.com/report/v2.0/abuse',data=json_parameters)
    cont = (resp.content)
    print (resp, end =" ")
    print (cont.decode("utf-8"), end =" ")
    print ( 'Url reported:  {url}')

with open ("urls_Microsoft.txt","r") as urls:
    url = [u.strip() for u in urls]
    
for u in url:
    report_to_mrsc(u)
from flask import Flask,render_template,request
import requests 
import json

app = Flask(__name__)

def getData():
    url = 'https://api.ibb.gov.tr/ispark/Park'
    response = requests.get(url)
    parkData = json.loads(response.text)
    return parkData

def getDistricts(parkData):    
    districts = {}

    for park in parkData:

        key = park['Ilce']
        parkName = park['ParkAdi']
        
        if key not in districts.keys():
            districts[key] = [parkName]
        else:
            districts[key].append(parkName)
    return districts

@app.route("/")
def index():
    data = getData()
    districts = getDistricts(data)
    return render_template("index.html", districts = districts)


'''
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['qrname']
    qrcolour = request.form['qrList']
    background = request.form['backgroundList']
    url = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + str(text) + '&color=' + str(qrcolour) + '&bgcolor=' + str(background) 
    return render_template("test.html", qr_image = url)
'''

if __name__ == "__main__":
    # get the status of the response
    app.run()
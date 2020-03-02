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

def getParkInfo(parkData, parkName):
    for park in parkData:
        if park['ParkAdi'] == parkName:
            return park['BosKapasite'], park['Kapasitesi'], park['Latitude'], park['Longitude']


@app.route("/", methods=['POST', 'GET'])
def index():
    data = getData()
    districts = getDistricts(data)

    if request.method == 'POST':
        
        parkName = request.form['parks']
        empty, capacity, latitude, longitude = getParkInfo(data, parkName)
        parkInfo = {'parkName': parkName, 'emptySpots': empty, 'capacity': capacity, 'lat': latitude, 'long': longitude }

        return render_template("index.html", districts = districts, parkInfo = parkInfo)
    
    else:    
        return render_template("index.html", districts = districts, parkInfo = '')
    

if __name__ == "__main__":
    app.run()
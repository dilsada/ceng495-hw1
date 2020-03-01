from flask import Flask,render_template,request
import requests 
import json

app = Flask(__name__)

def getDistricts():
    url = 'https://api.ibb.gov.tr/ispark/Park'
    response = requests.get(url)
    parkData = json.loads(response.text)
    
    districts = {}

    for park in parkData:
        key = park['Ilce']
        if key not in districts.keys():
            districts[key] = [park]
        else:
            districts[key].append(park)
    return districts

def getParkNames(parks):
    parksNames = []
    for park in parks:
        name = park['ParkAdi']
        parksNames.append(name)
    return parksNames

@app.route("/", methods=['GET', 'POST'])
def index():
    districts = getDistricts()
    
    if request.method == 'POST':
        option = request.form.get('districts')
        parks = getParkNames(districts[str(option)])
        return render_template("index.html", districts = districts.keys(), parks = parks)
        
    else:    
        return render_template("index.html", districts = districts.keys(), parks = '')
        


#@app.route('/', methods=['POST'])
#def showParks():   
    #url = 'https://api.ibb.gov.tr/ispark/Park'
    #parksList = []
    #for key,value in url.items():


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
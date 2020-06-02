from Adafruit_BME280 import *
import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.goff.us/api/office"
auth_token = "Bearer Token"
head = {'Content-Type': "application/json", 'Accept-Encoding': "gzip, deflate", 'Authorization': 'Bearer {}'.format(auth_token)}

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

body_data = {}

humidity = None
temperature = None

def send_info(humidity, temperature):
    body_data['officeProbeTemp'] = temperature
    body_data['officeProbeHumidity'] = humidity
    response = requests.post(url, headers=head, verify=False, data=json.dumps(body_data))
    data = response.reason
    print(data)

def get_temp():
    degrees = sensor.read_temperature()
    degreesF = (degrees * (9.0 / 5.0))+ 32
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()

    print 'Temp      = {0:0.3f} deg F'.format(degreesF)
    # print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
    print 'Humidity  = {0:0.2f} %'.format(humidity)

    # print("temperature:{:.2f}".format(bmpData[0])+" F  pressure:{:.2f}".format(bmpData[1])+" InHg   altitude:{:.2f}".format(bmpData[2]))
    return round(humidity,2), round(degreesF,2)

humidity, temp_f = get_temp()
send_info(humidity, temp_f)

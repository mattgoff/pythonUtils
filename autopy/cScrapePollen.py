from selenium import webdriver
import json
import requests
import time
import urllib3
import pdb

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pollen_dict = {}
url = "https://www.goff.us/api/allergy/"
auth_token = "Bearer Token"
head = {'Content-Type': "application/json", 'Authorization': 'Bearer {}'.format(auth_token)}

def send_info():
    response = requests.post(url, headers=head, verify=False, data=json.dumps(pollen_dict))
    #pdb.set_trace()
    #data = response.json()
    print(response.text)

def get_pollen_info():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')

# initialize the driver
    driver = webdriver.Chrome('/home/ubilinux/auto_py/chromedriver', chrome_options=options)
    driver.get('https://www.pollen.com/forecast/current/pollen/85383')
    allergyData = driver.find_element_by_css_selector("div#forecast-chart")
    time.sleep(5)
    data = allergyData.text.split("\n")
    time.sleep(5)
    pollen_dict["pollenYesterday"] = str(data[2])
    pollen_dict["pollenToday"] = str(data[5]) + " " + ' '.join(data[8:11])
    pollen_dict["pollenTomorrow"] = data[-2]

get_pollen_info()
send_info()




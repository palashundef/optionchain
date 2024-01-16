import requests
import json
import schedule
import time
import datetime
from os.path import exists
import threading

def fetch_data(i):
        headers = {"User-Agent": "Mozilla/5.0"}
        
        filename = f"{i}-chain.json"
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={i}"
    
        r = requests.get(url, headers=headers)

        return r

def save_to_file(response,i):
    filename = f"{i}-chain2.json"
    content = response.json()
    saveData = {}    
    if(exists(filename)):
    
        with open(filename, "r") as file:
            print(filename)
            data =   json.load(file)
            # print(data)
            saveData = data
            saveData[datetime.datetime.now().strftime("%H:%M") ] = content
    else:
         saveData[datetime.datetime.now().strftime("%H:%M") ] =  content
          
    with open(filename, "w+") as json_file:
            json.dump(saveData, json_file, indent=4)

def create_Calls():
    current_time = datetime.datetime.now().strftime('%H:%M')
    if(not(current_time >= "09:00" and current_time <= "20:15")):
         return 
    indexes = ['NIFTY','BANKNIFTY']
     
    
    for i in indexes:
        # print('e')

        response =  fetch_data(i)
        while response.status_code != 200 :
        #    print('ddd')
           time.sleep(1)
           response =   fetch_data(i)
        save_to_file(response,i)
        # print('d')
     

if __name__ == '__main__':
    # create_Calls()
    # schedule.every(60*5).seconds.do(create_Calls)
    while True:
            if(datetime.datetime.now().time().minute % 5 != 0):
                continue
            t1 = threading.Thread(target=create_Calls)
            t1.start()
            time.sleep(60)
            t1.join()
            # schedule.run_pending()
            # time.sleep(1)

    
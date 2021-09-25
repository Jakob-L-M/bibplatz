from flask import Flask, render_template, request
import json
from multiprocessing import Process
import time
from random import random
from bib import Bib

app = Flask(__name__)

b = Bib()



@app.route("/")
def hello():
  return render_template('main.html')

@app.route("/find_seats/", methods=['GET','POST'])
def find_seats():
    data = request.get_json()
    with open('bib.json', 'r') as f:
            dic = json.load(f)
    return json.dumps(find_place(dic, layers=data['layers'], day=data['day'], time=data['time']))

def update_data():
    while True:
        hour = (int((time.time() - int(int(time.time())/86400)*86400)/3600) + 2) % 24
        print("current Hour:", hour)
        if hour < 7:
            time.sleep(60*10)
            continue

        # b.update()

        next = 60*5+random()*60*3
        print(next/60)
        time.sleep(next)

def find_place(dic, layers, day, time):
        result = []
        for layer in layers:
            temp = dic[layer][day]
            res = []
            for place in temp:
                for slot in temp[place]['free']:
                    if slot[0] <= int(time[0]) and slot[1] >= int(time[1]):
                        res.append(place)
                        break
            result.append(res)
        return result

if __name__ == "__main__":
  p = Process(target=update_data)
  p.start()
  app.run(use_reloader=False)
  p.join()
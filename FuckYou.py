import random
import os
import datetime
import json
from flask import Flask,request,render_template,Response


app = Flask(__name__)

datamain = {}

class session:
    def __init__(self,name):
        self.jsonfile = os.getcwd()
        self.time = datetime.datetime.now()
        self.quest = []
        self.answer = []
        self.useranswers = []
        self.stage = 0
        if os.path.exists(self.jsonfile + '/baza/' + name + ".json"):
            with open(self.jsonfile + '/baza/' + name + ".json",'r') as js:
                mainj = json.load(js)
        else:
            data = {"id": name, "rightanswers": 0}
            with open(self.jsonfile + '/baza/' + name + ".json", 'w', encoding='UTF-8') as js:
                json.dump(data, js, ensure_ascii=False)
        self.questgenerate()

    def endthis(self):
        result = ""
        for a in range(5):
            if self.answer[a] == self.useranswers[a]:
                result += "<br>" + str((a+1)) + ". <green>Дан правильный ответ.</green> "
            else:
                result += "<br>" + str((a+1)) + ". <red>Дан неправильный ответ.</red> " + str(self.answer[a])
        return result

    def questgenerate(self):
        bignumbs = random.randint(10, 32) * 100000

        middlenumbs = random.randint(16, 30) * 1000
        smallnumbs = random.randint(120, 1000)
        tinynumbs = random.randint(4, 12)
        print(bignumbs,middlenumbs,smallnumbs,tinynumbs)
        t = random.sample(range(1,6), 5)
        with open("quest.json") as js:
            quests = json.load(js)
        for a in range(0,5):
            print(t)
            self.quest.append(quests["q" + str(t[a])])
            if t[a] == 1:
                self.answer.append(round((middlenumbs + middlenumbs*4/5 + middlenumbs/2 + middlenumbs/4),1))
                self.quest[a] = self.quest[a].replace("*%",str(middlenumbs))
                self.quest[a] = self.quest[a].replace("*1%", str(middlenumbs/2))
            elif t[a] == 2:
                self.answer.append(round((middlenumbs * 1.2 / ((tinynumbs + 3 )/100)*12 / (tinynumbs - 2)),1))
                self.quest[a] = self.quest[a].replace("*%",str(tinynumbs - 2))
                self.quest[a] = self.quest[a].replace("*1%", str(tinynumbs + 3))
                self.quest[a] = self.quest[a].replace("*2%", str(middlenumbs * 1.2))
            elif t[a] == 3:
                self.answer.append(round((((round(bignumbs * random.uniform(1,1.5))) / bignumbs-1)/4*100),2))
                self.quest[a] = self.quest[a].replace("*%",str(bignumbs))
                self.quest[a] = self.quest[a].replace("*1%", str(round(bignumbs * random.uniform(1,1.5))))
                print((bignumbs * 1.3 / bignumbs-1)/4*100)
                print(bignumbs)
                print(bignumbs)
            elif t[a] == 4:
                self.answer.append(round((smallnumbs * 1.5 - smallnumbs),1))
                self.quest[a] = self.quest[a].replace("*%",str(smallnumbs))
                self.quest[a] = self.quest[a].replace("*1%", str(smallnumbs * 1.5))
            elif t[a] == 5:
                self.answer.append(round((bignumbs *0.1 + bignumbs),1))
                self.quest[a] = self.quest[a].replace("*%",str(bignumbs))




@app.route('/res',methods=['GET'])
def hello_wor():
    nameandf = request.args.get('name')
    id = request.args.get('id')
    results = request.args.get('tasks')
    print(results)
    return render_template('ind.html',results = results)


@app.route('/f',methods=['GET'])
def hello_worl():
    nameandf = request.args.get('name')
    id = request.args.get('id')
    return render_template('inde.html',name=nameandf,id = id,val1=random.randint(16000, 30000),val2 = random.randint(4, 12),val3 = random.randint(1000000, 3200000),val4 = random.randint(120, 1000),val5 = random.randint(100000, 500000))

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method == 'GET':
        return render_template('inde.html')
    else:
        data = request.get_json()
        if data["type"] == 'e':
            if data["name"] in datamain:
                if datamain[data["name"]].stage == 0:
                    datamain[data["name"]].stage+=1
                dat = datamain[data["name"]].quest[datamain[data["name"]].stage] + "<br> <input name='...' type='text' maxlength='512' placeholder='Ответ' id = 'task' /> <br> <button id = 'next' onclick='next()'>Далее </button> "
                print(dat)
                return Response(response=dat, status=200, mimetype="text / plain", content_type='text/event-stream')
            else:
                datamain[data['name']] = session(data['name'])
                datamain[data["name"]].stage+=1
                dat = datamain[data["name"]].quest[datamain[data["name"]].stage] + "<br> <input name='...' type='text' maxlength='512' placeholder='Ответ' id = 'task' /> <br> <button id = 'next' onclick='next()'>Далее </button>  "
                print(dat)
                return Response(response=dat, status=200, mimetype="text / plain", content_type='text/event-stream')
        elif data['type'] == 'r':
            datamain[data["name"]].useranswers.append(data["answ"])
            if(datamain[data["name"]].stage != 5):
                datamain[data["name"]].stage += 1
                dat = datamain[data["name"]].quest[datamain[data["name"]].stage] + "<br> <input name='...' type='text' maxlength='512' placeholder='Ответ' id = 'task' /> <br> <button id = 'next' onclick='next()'>Далее </button>"
            else:
                dat = datamain[data["name"]].endthis()
            print(dat)
            return Response(response=dat, status=200, mimetype="text / plain", content_type='text/event-stream')



if __name__ == '__main__':
    app.run()
    #if request.method == 'GET':
     #   print(request.args)
    #return render_template('index.html')

#-*- coding: utf-8 -*-
from flask import Flask, session, redirect, url_for, request, render_template, escape, jsonify, make_response
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.response_selection import get_most_frequent_response
from clsUtil import User
from clsUtil import Greetings
from clsUtil import Log
from clsUtil import Script
import datetime

'''
Reload enconding with python2, it's not necessary in python3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''

app = Flask(__name__)
app.secret_key = "dpsp"

log = Log()
user = User()
greetings = Greetings()
script = Script()
botname = 'bot'

pt_bot = ChatBot(
    "DPSP_bot",
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    read_only=True,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Resetar minha senha no SAP',
            'output_text': 'Digite o seu login do SAP'
        },
        #{
        #    'import_path': 'chatterbot.logic.TimeLogicAdapter'
        #},
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.50,
            'default_response': 'N�o sei responder isso ainda... '
        }
    ],
    filters=[
            'chatterbot.filters.RepetitiveResponseFilter'
    ],
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    database="chat_db",
    database_uri='mongodb://localhost:27017'
    #database_uri='mongodb://mongoadmin:secret@localhost:27017'
)
 
pt_bot.set_trainer(ChatterBotCorpusTrainer)
pt_bot.train(["chatterbot.corpus.portuguese", "./data/localKnowledge/"])

@app.route("/")
@app.route("/index/")
@app.route("/home/")
def home():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    log.setHeader(timestamp, user)
    return render_template("index.html", ptimestamp=timestamp)

@app.route("/send")
def get_user_message():
    userText = str(request.args.get('msg'))

    return jsonify(
        message=userText,
        name=user.Name,
        datetime=datetime.datetime.now().strftime('%H:%M')
    )

@app.route("/get")
def get_bot_response():
    timestamp = str(request.args.get('ptimestamp'))
    userText = str(request.args.get('msg'))

    if userText.__contains__('CPF'):
        session[str(user.Computer) + '_' + user.User + '_' + timestamp + '_CPF'] = userText

    var_teste = str(user.Computer) + '_' + user.User + '_' + timestamp + '_CPF'

    val_teste = session.get(var_teste, None)

    if val_teste is not None:
        print('teste: ' + val_teste)

    log.setDetail(timestamp, user, userText, user.User)

    response = script.execScriptIfCommand(timestamp, user, userText, user.User, botname)
    if not response:
        response = str(pt_bot.get_response(userText))

    log.setDetail(timestamp, user, response, botname)

    return jsonify(
        message=response,
        name=botname,
        datetime=datetime.datetime.now().strftime('%H:%M')
    )

@app.route("/ini")
def get_ini():
    timestamp = str(request.args.get('ptimestamp'))

    gret = '{_greeting} {_name}, gostaria de resetar a senha de usu�rio no SAP?'.format(_greeting=greetings.getGreeting(), _name=user.Name)

    log.setDetail(timestamp, user, gret, botname)

    return jsonify(
        message=gret,
        name=botname,
        datetime=datetime.datetime.now().strftime('%H:%M')
    )

if __name__ == "__main__":
    app.run(host='localhost',port=50000, debug=True)

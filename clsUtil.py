import datetime
import subprocess
from clsAd import Ad
from clsLogFile import LogFile
from clsPowershell import Powershell

class User:
    def __init__(self): 
        ad = Ad()
        self.Computer = ad.ComputerName
        self.Domain = ad.UserDomain
        self.Name = ad.GivenName
        self.User = ad.SamAccountName
        self.Email= ad.EmailAddress

class Greetings:
    @classmethod
    def getGreeting(cls):
        now = datetime.datetime.now()
        hour = now.hour

        if hour < 12:
            _greeting = "Bom dia"
        elif hour < 18:
            _greeting = "Boa tarde"
        else:
            _greeting = "Boa noite"

        return _greeting

class Log:
    @classmethod
    def setHeader(cls, timestamp, user):
        log = LogFile()
        log.setHeader(timestamp, user)

    @classmethod
    def setDetail(cls, timestamp, user, message, person):
        log = LogFile()
        log.setDetail(timestamp, user, message, person)

class Script:
    @classmethod
    def execScriptIfCommand(cls, timestamp, user, message, person, botname):
        keywords = [ "execute ", "run " ]
        run = None
        failed_cmd = None
        retorno = None
        log = LogFile()

        if message:
            for key in keywords:
                if message.startswith(key):
                    cmd = message.replace(key, '')
                    run = True

        if run:
            try:
                script = message.split()[1]

                log.setDetail(timestamp, user, 'Executar script: ' + script, botname)

                powershell = Powershell()
                returncode = powershell.execScriptNoReturn(script)

                if returncode == 0:
                    log.setDetail(timestamp, user, 'Sucesso ao executar script: ' + script, botname)
                else:
                    log.setDetail(timestamp, user, 'Falha ao executar script: ' + script, botname)
                    failed_cmd = True

            except:
                log.setDetail(timestamp, user, 'Falha ao executar script: ' + script, botname)
                failed_cmd = True

        if run and not failed_cmd:
            retorno = str('O comando foi executado com sucesso.')

        if run and failed_cmd:
            retorno = str('N�o consegui executar o comando.')

        return retorno

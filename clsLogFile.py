import os.path
import datetime

class LogFile:
    @classmethod
    def setHeader(cls, timestamp, user):
        file = './log/' + str(user.Computer) + '_' + user.User + '_' + timestamp + '.log'

        timestamplog = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with open(file, 'a') as f:
            f.write('Computador: {computador}\n'.format(computador=user.Computer))
            f.write('Domínio: {dominio}\n'.format(dominio= user.Domain)) 
            f.write('Usuário: {nome} ({usuario} - {email})\n'.format(nome= user.Name, usuario=user.User, email= user.Email)) 
            f.write('Conversa iniciada em: {hora}\n'.format(hora=timestamplog)) 
            f.write('\n')
            f.close()

    @classmethod
    def setDetail(cls, timestamp, user, message, person):
        file = './log/' + str(user.Computer) + '_' + user.User + '_' + timestamp + '.log'

        if not file or not os.path.isfile(file):
            LogFile.setHeader(timestamp, user)

        timestamplog = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with open(file, 'a') as f:
            f.write('{hora} - {pessoa}: {mensagem}\n'.format(hora=timestamplog, pessoa=person, mensagem=message)) 
            f.close()

import subprocess
import sys
from clsPowershell import Powershell

class Ad:
    def __init__(self):
        powershell = Powershell()

        returncode, retorno = powershell.execScript('userinfo.ps1')

        if returncode == 0:
            self.ComputerName = retorno[0]
            self.UserDomain = retorno[1]
            self.Sid = retorno[2]
            self.Guid = retorno[3]
            self.Name = retorno[4]
            self.SamAccountName = retorno[5]
            self.DisplayName = retorno[6]
            self.EmailAddress = retorno[7]
            self.Description = retorno[8]
            self.GivenName = retorno[9]

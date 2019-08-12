import subprocess
import sys

class Powershell:
    @classmethod
    def execScript(cls, script):
        cmd = ['powershell.exe', '-ExecutionPolicy', 'RemoteSigned', '-File', '.\\scripts\\' + script]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = p.communicate()[0].decode("utf-8").split('\r\n')
        returncode = p.wait()

        return returncode, data

    def execScriptNoReturn(cls, script):
        cmd = ['powershell.exe', '-ExecutionPolicy', 'RemoteSigned', '-File', '.\\scripts\\' + script]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        returncode = p.wait()

        return returncode

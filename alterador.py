import string, random, asyncio, requests, datetime
from colorama import Fore, init
init(convert=True)

class Change:
    def __init__(self, token):
        self.token = token
    
    def genPass(self, length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def getHeaders(self, token):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36',
            'Content-Type': 'application/json',
            'Authorization': token,
        }
        return headers

    def logInfo(self, new_password, old_password):
        date = datetime.datetime.now().strftime("%H:%M %p")
        f = open("loggin.txt", "a")
        data = '==============================='
        data += '\nNova senha: ' + new_password
        data += '\nSenha Antiga: ' + old_password
        data += '\nAlterado às: ' + date
        data += '\n==============================\n\n'
        f.write(data)

    def changePass(self, old_pass, interval):
        change_password = old_pass
        userInfo = requests.get('https://discordapp.com/api/v6/users/@me', headers=self.getHeaders(self.token)).json()
        newPass = self.genPass(10)
        payload = {
            'password': change_password,
            'new_password': newPass,
            'discriminator': userInfo['discriminator'],
            'email': userInfo['email'],
            'avatar': userInfo['avatar']
        }
        requests.patch("https://discordapp.com/api/v6/users/@me", json=payload, headers=self.getHeaders(self.token)) 
        self.logInfo(newPass, old_pass)
        change_password = newPass
        asyncio.sleep(interval * 3600) 
        
if __name__ == "__main__":
    print(f"[{Fore.RED}>{Fore.RESET}] Token de Usuário")
    token = str(input(">"))
    print(f"[{Fore.RED}>{Fore.RESET}] Intervalo para alteração")
    interval = int(input(" > "))
    print(f"[{Fore.RED}>{Fore.RESET}] senha atual")
    c_pass = str(input(" > "))

    Change(token).changePass(c_pass, interval)
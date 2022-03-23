from django.http import HttpResponse, HttpRequest
import cmd
import requests
import json
import getpass

flag = 0

class Command(cmd.Cmd):
    intro = '\nWelcome to the rating system!\n' \
            'The following commands are supported:\n\n' \
            'register - To register\n' \
            'login url - To login\n' \
            'logout - To logout\n' \
            'list - To view all modules and related information\n' \
            'view - To view all ratings of professors\n' \
            'average professor_id module_id - To view one certain rating\n' \
            'rate professor_id module_code year semester rating - To rate someone\n'
    prompt = 'Input>'

    def do_register(self, arg):
        self.register()

    def do_login(self, arg):
        self.login(arg)

    def do_logout(self, arg):
        self.logout()

    def do_list(self, arg):
        self.list()

    def do_view(self, arg):
        self.view()

    def do_average(self, arg):
        value = arg.split()
        self.average(value[0], value[1])

    def do_rate(self, arg):
        value = arg.split()
        self.rate(value[0], value[1], value[2], value[3], value[4])

    def do_exit(self, _):
        print("Bye~")
        'Exit'
        exit(0)

    def login(self, arg):
        u = "sc18zz.pythonantwhere.com"
        global flag
        if arg == u:
            url = "http://127.0.0.1:8000/login/"
            username = input('Please enter username: ')
            pwd = getpass.getpass('Please enter password: ')
            info = {'username': username, 'password': pwd}
            json.dumps(info)
            re = requests.post(url, json=info)
            j = json.loads(re.text)
            status = j.get('status')
            if status == 1:
                flag = 1
                print("Successfully logged in!")
            elif status == 0:
                print("Wrong username or password!")
        elif arg == "":
            print("Enter the url!")
        else:
            print("Try another url!")

    def logout(self):
        global flag
        url = "http://127.0.0.1:8000/logout/"
        re = requests.post(url)
        j = json.loads(re.text)
        flag = 0
        info = j.get('status')

        print(info)

    def register(self):
        url = "http://127.0.0.1:8000/register/"
        username = input('Please enter username: ')
        email = input('Please enter email: ')
        pwd = getpass.getpass('Please set password: ')
        info = {'username': username, 'email': email, 'password': pwd}
        json.dumps(info)
        re = requests.post(url, json=info)
        j = json.loads(re.text)
        context = j.get('info')
        print(re)
        print(context)

    def list(self):
        url = "http://127.0.0.1:8000/listall/"
        req = requests.get(url)
        info = json.loads(req.text)
        print('%-25s\t%-25s\t%-25s\t%-25s\t%-25s' % ('Code', 'Name', 'Year', 'Semester', 'Taught By'))
        for i in info.values():
            for u in range(4):
                print("%-25s" % i[u], end='\t')
            for item in range(4, len(i) - 1):
                print(i[item], end=",")
            for item in range(len(i) - 1, len(i)):
                print(i[item], end="")
            print("")
            print("-" * 150)

    def view(self):
        url = "http://127.0.0.1:8000/rateall/"
        req = requests.get(url)
        info = json.loads(req.text)
        for i in info.items():
            print("The rating of Professor %s (%s) is %s" % (i[1][0], i[0], i[1][1]))

    def average(self, arg0, arg1):
        url = "http://127.0.0.1:8000/rateone/"+"?pcode="+arg0+"&mcode="+arg1
        req = requests.get(url)
        info = json.loads(req.text)
        print("The rating of Professor %s (%s) in module %s (%s) is %s" % (info['pname'], info['pcode'],
                                                                           info['mname'], info['mcode'], info['avg']))

    def rate(self, arg0, arg1, arg2, arg3, arg4):
        global flag
        if 0.0 <= float(arg4) <= 5.0 and flag == 1:
            arg4 = round(float(arg4), 1)
            url = "http://127.0.0.1:8000/giverate/"+"?pcode="+arg0+"&mcode="+arg1+"&year="+arg2\
                  +"&sem="+arg3+"&rate="+str(arg4)
            req = requests.get(url)
            print("OKAY!")
        elif float(arg4) >= 5.0 or float(arg4) <= 0.0:
            print("Please enter the rating value between 0-5!")
        elif flag == 0:
            print("Please login first!")


if __name__ == '__main__':
    Command().cmdloop()
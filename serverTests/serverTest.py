# to be run on the same machine running the server code: test.py
# simply indicates whether or not the server is working

import requests

a = input("a: ")
b = input("b: ")
mode = input("mode: ")

dat = {
    'a':a,
    'b':b,
    'mode':mode,
}

r = requests.post("http://localhost",data=dat)
print(r.text)
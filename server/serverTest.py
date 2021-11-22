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
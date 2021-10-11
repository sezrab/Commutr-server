import requests

a = input("a: ")
b = input("b: ")

a1,a2 = a.split(",")
b1,b2 = b.split(",")

dat = {
    'aLat':a1,
    'aLon':a2,
    'bLat':b1,
    'bLon':b2,
}

r = requests.post("http://localhost",data=dat)
print(r.text)
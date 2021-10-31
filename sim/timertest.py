from threading import Timer
a = [1,2,3]

def hello():
    a.append(4)

t = Timer(5.0, hello)
t.start() 

while 1:
    if 4 not in a:
        print("4 not here")


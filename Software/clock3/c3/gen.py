import time, itertools

def rotate_list(ba):
    "Gib die rotierte Liste zurück"
    return [ba[-1]] + ba[:-1]

def rotate(cl):
    "Generiere Rotationen der ColorList cl"
    while True:
        yield cl
        cl = rotate_list(cl)

def steplist(nsteps):
    "Einmal rauf und wieder runter 0..n..1"
    return list(range(nsteps))+list(range(nsteps,0,-1))

def blink(cl,nsteps=5):
    "Variiere die Helligkeit"
    loop = list( i/float(nsteps) for i in steplist(nsteps))
    for h in itertools.cycle(loop):
        yield list(ci*h for ci in cl)

def take(gen,n):
    "Beschränke auf n Ausgaben"
    if n > 0:
        for i in gen:
            if n <= 0:
                break
            yield i
            n = n-1

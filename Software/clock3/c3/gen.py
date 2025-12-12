import time

def rotate_list(ba):
    "Gib die rotierte Liste zurück"
    return [ba[-1]] + ba[:-1]

def rotate(cl,sleep=0.5):
    "Generiere Rotationen der ColorList cl"
    while True:
        yield cl
        cl = rotate_list(cl)
        time.sleep(sleep)

def take(gen,n):
    if n > 0:
        for i in gen:
            if n <= 0:
                break
            yield i
            n = n-1

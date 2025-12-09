from .color import ROT, GRÜN, BLAU

def ternär(dec,s=None):
    "Wandle dec in ternär um mit s Stellen"
    l = []
    if dec == 0:
        l = [0]
    else:
        while dec > 0:
            n = dec % 3
            dec = int((dec - n)/3)
            l.append(n)
    if s:
        return l + [0] * (s-len(l))
    return l

ternär_color_map = [ROT,GRÜN,BLAU]

def ternär_colors(dec,s=None):
    return [ternär_color_map[i] for i in reversed(ternär(dec,s))]

def time_ternär_colors(ti):
    return ternär_colors(ti.hour,3)+ternär_colors(ti.minute,4)+ternär_colors(ti.second,4)

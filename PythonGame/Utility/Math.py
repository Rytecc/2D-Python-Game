def map(x0:float, y0:float, x1:float, y1:float, a:float) -> float:
    return (x0 - a) / (y0 - a) * (y1 - x1) + x1

def lerp(x:float, y:float, t:float) -> float:
    return x + (y - x) * t
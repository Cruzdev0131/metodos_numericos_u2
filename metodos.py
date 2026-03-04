def biseccion(f, a, b, tol=1e-6, max_iter=100):
    if f(a)*f(b) > 0:
        return None
    
    for _ in range(max_iter):
        c = (a+b)/2
        if abs(f(c)) < tol:
            return c
        if f(a)*f(c) < 0:
            b = c
        else:
            a = c
    return (a+b)/2


def falsa_posicion(f, a, b, tol=1e-6, max_iter=100):
    if f(a)*f(b) > 0:
        return None
    
    for _ in range(max_iter):
        c = b - (f(b)*(b-a))/(f(b)-f(a))
        if abs(f(c)) < tol:
            return c
        if f(a)*f(c) < 0:
            b = c
        else:
            a = c
    return c


def secante(f, x0, x1, tol=1e-6, max_iter=100):
    for _ in range(max_iter):
        if f(x1) - f(x0) == 0:
            return None
        x2 = x1 - f(x1)*(x1-x0)/(f(x1)-f(x0))
        if abs(x2-x1) < tol:
            return x2
        x0, x1 = x1, x2
    return x2


def newton(f, df, x0, tol=1e-6, max_iter=100):
    for _ in range(max_iter):
        if df(x0) == 0:
            return None
        x1 = x0 - f(x0)/df(x0)
        if abs(x1-x0) < tol:
            return x1
        x0 = x1
    return x1
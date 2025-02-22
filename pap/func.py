# Docstring des func-Moduls
'''
Dieses Modul enthält ein paar grundlegende mathematische Funktionen, die dazu gedacht sind als 
Fit-Funktionen eingesetzt zu werden. 

Die Argumente haben die Struktur pap.func.blabla(x, *jeweilige_parameter), wobei x 
auch ein numpy-Array an x-Werten sein kann. Der Output besteht immer aus dem jeweiligen 
Funktionswert (bzw. Array von Werten).



Übersicht der Funktionen
------------------------
* pap.func.konst()   Konstante Funktion       f(x) = c
    
* pap.func.prop()    Proportionale Funktion   f(x) = ax
    
* pap.func.lin()     Lineare Funktion         f(x) = ax + b
    
* pap.func.quad()    Quadratische Funktion    f(x) = ax^2 + bx + c
    
* pap.func.poly()    allgemeines Polynom      f(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_0 x^0
    

* pap.func.exp()     Exponentialfunktion      f(x) = A*e^(λx)

* pap.func.gauss()   Gaußverteilung           f(x) = A / (sqrt(2π)σ) * exp(-(x - μ)^2 / (2σ^2))
'''






# Alle benötigten Pakete

import numpy as np
from numpy import array as arr






# Einfache mathematische Funktionen

def konst(x, c):
    '''
    Konstante Funktion:
    f(x) = c
    '''
    
    return c




def prop(x, a):
    '''
    Proportionale Funktion:
    f(x) = ax
    '''
    
    return a * x




def lin(x, a, b):
    '''
    Lineare Funktion:
    f(x) = ax + b
    '''
    
    return a * x + b




def quad(x, a, b, c):
    '''
    Quadratische Funktion:
    f(x) = ax^2 + bx + c
    '''
    
    return a * x**2 + b * x + c




def poly(x, parameter):
    '''
    Polynom:
    f(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_0 x^0
    
    x         : np.ndarray, beliebige Form
    parameter : np.ndarray, 1D
    '''
    
    
    n              = len(parameter)                               # Grad des Polynoms
    x_potenzen     = arr([x**i for i in range(n - 1, -1, -1)])    # (x^n, ..., x^0)
    polynomglieder = (parameter.T * x_potenzen.T).T               # (a_i x^i), Trafo nötig um numpy broadcasting zu ermöglichen   
    
    return np.sum(polynomglieder, axis = 0)




def exp(x, A0, lamb):
    '''
    Exponentielle Funktion:
    f(x) = A*e^(λx)
    '''
    
    return A0 * np.exp(lamb * x)




def gauss(x, A0, mu, sigma):
    '''
    Gaußsche Glockenfunktion
    f(x) = A / (sqrt(2π)σ) * exp(-(x - μ)^2 / (2σ^2))
    '''
    
    return A0 / (np.sqrt(2 * np.pi) *  sigma) * np.exp(-(x - mu)**2 / 2 / sigma**2)

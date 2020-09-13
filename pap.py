#!/usr/bin/env python
# coding: utf-8


import numpy as np
from numpy import array as arr
from scipy.stats import chi2
from tabulate import tabulate





# Fehlerrechnung

def summen_fehler(fehler_array):
    '''Quadratische Addition der Fehler einer Summe
    
    Die Form dieser Summe soll sein  wert1 + wert2 + ... + wertn.
    fehler_array soll eine Form haben wie  [fehler_wert1, ..., fehler_wertn].
    '''
    
    return np.linalg.norm(fehler_array, axis = 0)




def produkt_fehler(produkt, rel_fehler_array):
    '''Quadratische Addition der relativen Fehler eines Produktes (optional inkl. Potenzen)
    
    Die Form dieses Produktes soll sein  wert1**n1 * wert2**n2 * ... * wertn**nn.
    fehler_array soll eine Form haben wie  [relativer_fehler_wert1, ..., relativer_fehler_wertn]
    mit  relativer_fehler_wert1 = n1 * fehler_wert1 / wert1,  wobei  n1  dessen Potenz ist.
    
    Wenn produkt = 1 gewählt wird, erhält man den relativen Fehler
    '''
    
    relativer_fehler = np.linalg.norm(rel_fehler_array, axis = 0)
    return np.abs(produkt) * relativer_fehler




def std(*args, **kwargs):
    '''Experimenteller Fehler des Einzelwertes
    
    Die Funktion ist identisch zu np.std() inkl. aller Argumente, 
    außer dass ddof = 1 gesetzt wird wenn nicht spezifisch angegeben.
    Wenn σ die Varianz einer Werteverteilung X mit N Werten ist, dann wird also im Normalfall berechnet
    std = sqrt(σ(X) / (N - 1))
    '''
    
    if not ('ddof' in kwargs):
        kwargs['ddof'] = 1
    return np.std(*args, **kwargs)




def mittel(*args, **kwargs):
    '''Mittelwert
    
    Die Funktion ist identisch zu np.std() inkl. aller Argumente
    und dient nur besseren Lesbarkeit inmitten von anderen pap-Funktionen.
    '''
    
    return np.mean(*args, **kwargs)




def fwhm(sigma):
    '''
    Halbwertsbreite:
    FWHM = 2 sqrt(2 ln(2)) * σ
    '''
    
    return 2 * np.sqrt(2 * np.log(2)) * sigma





# Ergebnisse anzeigen

## Für resultat() benötigte Funktionen

def _rundung(werte, nachkommastellen:int):
    '''
    Rundet werte auf eine Anzahl nachkommastellen.
    werte soll eine Numpy-Zahl oder -Array sein.
    '''
    
    if nachkommastellen <= 0:
        return np.int_(np.round(werte, nachkommastellen))
    else:
        return np.round(werte, nachkommastellen)


    
    
def _istbool(wert, bool_wert:bool):
    '''
    Überprüft ob wert wirklich bool_wert (True oder False) ist und nicht nur 1 oder 0.
    '''
    
    return (wert == bool_wert and isinstance(wert, bool))    
    

    
    
def resultat(titel, werte, einheit = '', faktor = 1, nachkommastellen = None, rel_fehler = False):
    '''
    Printet ein schön formatiertes Ergebnis mit 
    Titel, definierter Präzision, evt. +/- Fehler, Einheit und evt. relativen Fehler.
    
    
    Parameter
    ---------
    titel : str
    
    werte : number-like, np.ndarray (1D, mit number-like Elementen)
        Darf die Formen haben 
        ein_wert, np.array([ein_wert]),
        np.array([ein_wert, sein_fehler]) oder 
        np.array([ein_wert, sys_fehler, stat_fehler]).
    
    einheit : str
    
    faktor : number-like, optional
        Ermöglicht Anpassung an Größenordnung und Einheit.
    
    nachkommastellen : int, optional
        Siehe "Rundung des Ergebnisses".
    
    rel_fehler : bool, number-like, optional
        darf False sein     (aus),
             True sein      (wenn Fehler vorhanden und ein_wert != 0,
                             dann wird dieser als sein_fehler / ein_wert bzw. als
                             (quadratische summe von sys- und stat_fehler) / ein_wert
                             berechnet.), oder
             eine Zahl sein (diese wird dann direkt angegeben)
    
    
    Beispiele
    ---------
    >>> pap.resultat('Abweichung', 0.30304, '%', faktor = 1e2, nachkommastellen = 0)
    Abweichung: 30 %
    
    >>> pap.resultat('Arbeit', np.array([3.35e6, 0.46e6]), 'MJ', faktor = 1e-6)
    Arbeit: 3.4 +/- 0.5 MJ
    
    >>> pap.resultat('Beschleunigung', np.array([9.8493, 0.0424, 0.1235]), 'm/s^2')
    Beschleunigung: 9.85 +/- 0.04(sys) +/- 0.12 (stat) m/s^2
    
    
    mit relativem Fehler:
    
    >>> pap.resultat('Arbeit           ', np.array([3.3423, 0.4679]), 'J', rel_fehler = True)
    Arbeit           : 342 +/- 5 J   (1.6 %)
    
    >>> pap.resultat('Fehler der Arbeit', 0.4679, 'J', rel_fehler = 1.6)
    Fehler der Arbeit: 5 J   (1.6 %)
                    
    
    Rundung der Ergebnisse
    ----------------------
      * Gibt man die Zahl der Nachkommastellen manuell an, so wird nach ihr gerundet.
        Dabei sind auch negative Werte erlaubt. Bei -1 z.B. wird 123 -> 120 gerundet.
      * Ansonsten wird automatisch nach der ersten signifikanten Stelle des größten
        Fehlers gerundet. z.B. [-123.33, -5.0, 0.02] wird zu "-123.3 +/- 5.0 +/- 0.0"
        Ist der Betrag dieser Stelle aber < 4, dann wird auf zwei signifikante 
        Stellen gerundet, d.h. 0.436 -> "0.4", aber 0.0392 -> "0.39"
      * Gibt es kein Fehler, oder sind diese alle 0, dann wird automatisch
        nachkommastellen = 16 gesetzt.
      * Der relative Fehler wird stehts auf zwei signifikante Stellen gerundet.
    '''
    
    
    
    # Überprüfen und Korrigierung von werte
    if type(werte) != np.ndarray:   # Falls werte nur eine Zahl ist, wird sie zum Array gemacht.
        werte = arr([werte])
    if len(werte) > 3:
        print('Zu viele Elemente in werte! >:(')
    
    werte = werte * faktor   # Umrechnung der Resultate auf gewünschte Einheit oder Größenordnung
    if len(werte) > 1:
        werte[1:] = np.abs(werte[1:])   # Keine negativen Fehlerangaben
        fehler = werte[1:]
        
        
    # eventuelles Erstellen eines relativen Fehlers
    if _istbool(rel_fehler, True):
        if werte[0] == 0:   # Um einen divide-by-zero Fehler zu vermeiden.
            rel_fehler = False
        elif len(werte) == 1:   # Um einen divide-by-nothing Fehler zu vermeiden.
            rel_fehler = False
        elif len(werte) == 2:
            rel_fehler = fehler[0] / werte[0] * 100   # [%], relativer Fehler
        elif len(werte) == 3:
            rel_fehler = summen_fehler(fehler) / werte[0] * 100   # [%], relativer Fehler des Gesamtfehlers
    
    if not _istbool(rel_fehler, False):
        # falls rel_fehler eine Zahl ist, wird mit dieser weitergerechnet, 
        # ansonsten ensteht hier gleich ein Fehler.
        
        # Rundung auf 2 signifikanten Stellen 
        rel_fehler = np.abs(np.float64(rel_fehler))
        if rel_fehler != 0:
            größenordnung = np.int(np.floor(np.log10(rel_fehler)))
            signifikante_stellen = 2
            präzision = -größenordnung + signifikante_stellen - 1
        else:
            präzision = 2
        rel_fehler = _rundung(rel_fehler, präzision)
        
        # Vorbereitung des Relativer-Fehler-Strings
        rel_fehler_string = f'   ({rel_fehler} %)'
    else:
        rel_fehler_string = ''
        
    
    # Bestimmung der Präzision des Ergebnisses   
    if nachkommastellen == None:
        if len(werte) > 1:
            größter_fehler = np.max(fehler)
            if größter_fehler != 0:
                größenordnung = np.int(np.floor(np.log10(größter_fehler)))
                signifikante_stellen = (1 if größter_fehler / 10**größenordnung >= 4.0
                                        else 2)   # Hier der 4.0-Cutoff
                nachkommastellen = -größenordnung + signifikante_stellen - 1
            else:
                nachkommastellen = 8   # Da Fehler = 0   
        else:
            nachkommastellen = 8   # Da kein Fehler vorhanden.
    
    
    # Rundung entsprechend der signifikante Stelle oder der eigenen Vorgabe
    wertepaar = _rundung(werte, nachkommastellen)
    if nachkommastellen <= 0:   # Um Fehler bei der String-Formatierung zu vermeiden.
        nachkommastellen = 0
    
    
    # Print des Ergebnis-Strings
    if len(werte) == 1:
        print(titel + ': {:.{prec}f} {}{}'
              .format(*wertepaar, einheit, rel_fehler_string, prec = nachkommastellen))
    elif len(werte) == 2:
        print(titel + ': {:.{prec}f} +/- {:.{prec}f} {}{}'
              .format(*wertepaar, einheit, rel_fehler_string, prec = nachkommastellen))
    elif len(werte) == 3:
        print(titel + ': {:.{prec}f} +/- {:.{prec}f}(sys) +/- {:.{prec}f}(stat) {}{}'
              .format(*wertepaar, einheit, rel_fehler_string, prec = nachkommastellen))
        

        
        
def chi_quadrat_test(fit_werte, werte, werte_fehler, anzahl_parameter): 
    '''
    Printet den χ^2_reduziert-Wert und die Fitwahrscheinlichkeit.
    fit_werte sind die Werte, die die Fitfunktion ausgibt.
    Also: fit_werte = fit_func(x_werte, *parameter)
    '''
    
    
    chi_quadrat = np.sum(((fit_werte - werte) / werte_fehler)**2) 
    freiheitsgrade = len(werte) - anzahl_parameter
    chi_quadrat_reduziert = chi_quadrat / freiheitsgrade 
    fit_wahrscheinlichkeit = (1 - chi2.cdf(chi_quadrat, freiheitsgrade)) * 100
    
    print(f"χ^2_reduziert         = {chi_quadrat_reduziert:.2f}") 
    print(f"Fitwahrscheinlichkeit = {fit_wahrscheinlichkeit:.1f}%")
    
    

    
def chi_quadrat_odr(fitfunktion, parameter, messpunkte, messfehler):
    x_werte = np.linspace(messpunkte[0][0] - 10 * messfehler[0][0], 
                          messpunkte[0][-1] + 10 * messfehler[0][-1], 10000000)
    fitwerte = fitfunktion(x_werte, *parameter)
    
    abstände_alle = np.linalg.norm(arr([(messpunkte[0][:, np.newaxis] - x_werte) 
                                        / messfehler[0][:, np.newaxis], 
                                        (messpunkte[1][:, np.newaxis] - fitwerte) 
                                        / messfehler[1][:, np.newaxis]]), axis = 0)
    abstände_min = np.min(abstände_alle, axis = 1)
    
    anzahl_parameter = len(parameter)
    anzahl_messwerte = np.shape(messpunkte)[1]
    
    chi_quadrat = np.sum(abstände_min**2)
    freiheitsgrade = anzahl_messwerte - anzahl_parameter
    chi_quadrat_reduziert = chi_quadrat / freiheitsgrade 
    fit_wahrscheinlichkeit = (1 - chi2.cdf(chi_quadrat, freiheitsgrade)) * 100

    print(f"χ^2_reduziert         = {chi_quadrat_reduziert:.2f}") 
    print(f"Fitwahrscheinlichkeit = {fit_wahrscheinlichkeit:.1f}%")
    
    
    
    
    
# Funktionen

def const_func(x, c):
    '''
    Konstante Funktion:
    f(x) = c
    '''
    
    return c




def prop_func(x, a):
    '''
    Proportionale Funktion:
    f(x) = ax
    '''
    
    return a * x




def lin_func(x, a, b):
    '''
    Lineare Funktion:
    f(x) = ax + b
    '''
    
    return a * x + b




def quad_func(x, a, b, c):
    '''
    Quadratische Funktion:
    f(x) = ax^2 + bx + c
    '''
    
    return a * x**2 + b * x + c




def poly_func(x, parameter):
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




def exp_func(x, A0, lamb):
    '''
    Exponentielle Funktion:
    f(x) = A*e^(λx)
    '''
    
    return A0 * np.exp(lamb * x)




def gauss_func(x, A0, mu, sigma):
    '''
    Gaußsche Glockenfunktion
    f(x) = A / (sqrt(2π)σ) * exp(-(x - μ)^2 / (2σ^2))
    '''
    
    return A0 / (np.sqrt(2 * np.pi) *  sigma) * np.exp(-(x - mu)**2 / 2 / sigma**2)

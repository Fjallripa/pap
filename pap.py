#!/usr/bin/env python
# coding: utf-8


import numpy as np
from numpy import array as arr
from scipy.stats import chi2
from scipy import odr
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
        return np.int_(np.round(werte, nachkommastellen))   # np.int_  um die Werte eines Arrays  
                                                            # zu int zu konvertieren
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
    
    
    Argumente
    ---------
    titel : str
    
    werte : number_like, np.ndarray (1D, mit number_like Elementen)
        Darf die Formen haben 
        ein_wert, np.array([ein_wert]),
        np.array([ein_wert, sein_fehler]) oder 
        np.array([ein_wert, sys_fehler, stat_fehler]).
    
    einheit : str
    
    faktor : number_like, optional
        Ermöglicht Anpassung an Größenordnung und Einheit.
    
    nachkommastellen : int, optional
        Siehe "Rundung des Ergebnisses".
    
    rel_fehler : bool, number_like, optional
        darf False sein     (aus),
             True sein      (wenn Fehler vorhanden und ein_wert != 0,
                             dann wird dieser als sein_fehler / ein_wert bzw. als
                             (quadratische summe von sys- und stat_fehler) / ein_wert
                             berechnet.), oder
             eine Zahl sein (Einheit Prozent; diese wird dann direkt angegeben)
    
    
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
        # falls rel_fehler eine Zahl ist, wird mit dieser weitergerechnet, bei False nicht. 
        # In anderen Fällen ensteht hier gleich ein Fehler.
        
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
        


        
        
# Funktionen fitten und χ^2-Tests machen
        
def odr_fit(funktion, messpunkte, messfehler, parameter0, 
            print_resultate = True, output_chi_test = False, funktionstyp = 'x, *p'):
    '''
    Orthogonal Distance Regression - Fittet eine 1D-Funktion an fehlerbehaftete Messdaten an. Im Gegensatz 
    zu curve_fit() aus scipy.stats werden hier auch Fehler in der x-Achse berücksichtigt. Eigentlich wird 
    hier nur das scipy.odr-Paket in einer einfach zu bedienenden aber optionsärmeren Funktion verpackt.
    
    Optional werden die Fit-Resultate angezeigt und returned, ebenso ein optionaler χ^2-Test.
    
    
    Argumente
    ---------
    funktion : function
        Erlaubt sind mathematische |R -> |R Funktionen. Folgende Argumente-Reihenfolgen sind unterstützt:
        funktion(x, *parameter)  also bspw. pap.quad_func(x, a, b, c)
        funktion(x, parameter)   parameter : array_like
        funktion(parameter, x)   parameter : array_like
        Der verwendete Typ muss unter  funktionstyp  angegeben werden.
    
    messpunkte : np.array (2D, mit number_like Elementen)
        Form: np.array([x_werte_liste, y_werte_liste])
    
    messfehler : np.array (2D, mit number_like Elementen > 0)
        Form: np.array([x_fehler_liste, y_fehler_liste])
    
    Natürlich müssen alle vier Listen gleich lang sein.
    
    parameter0 : array_like (1D, mit number_like Elementen)
        Erste Schätzung, für was die gefitteten Parameter sein sollen.
        Achtung! Eine schlechte Schätzung kann dazu führen, dass der Fit schief läuft.
    
    print_resultate : bool, optional
        Bei  True  wird eine Zusammenfassung der Fitergebnisse geprintet (pprint() aus scipy.odr),
        siehe  Beispiele  und  Bedeutung des Fit-Resultates.
        Bei  False  wird nichts geprintet.
    
    output_chi_test : bool, string, optional
        Bei  False  wird der χ^2-Wert des Fits nicht returned,
        bei  True  schon.
        Bei  'print'  wird ein χ^2-Test direkt ausgeführt und geprintet (pap.chi_quadrat_odr()),
        siehe  Beispiele  und Dokumentation von  pap.chi_quadrat_odr()
    
    funktionstyp : string, optional
        Ist standardmäßig auf  'x, *p',  also die Form  funktion(x, *parameter)  eingestellt.
        Wähle  'x, p_list'  für Form  funktion(x, parameter)
        oder   'p_list, x'  für Form  funktion(parameter, x).
    
    
    Output
    ------
    parameter : np.array (1D, float Elemente)
        Liste der Parameter der gefitteten Funktion
    
    paramter_fehler : np.array (1D, float Elemente)
        Liste von deren 1σ-Fehlern (Standardabweichungen)
    
    chi_quadrat_liste : list, optional
        Besteht aus 
        chi_quadrat : float, 
        anzahl_messwerte : int,
        anzahl_parameter : int
        Kann man direkt in  pap.chi_quadrat_odr()  einfügen, siehe  Beispiele.
        
    
    Beispiele
    ---------
    Hier werden sowohl Fit-Resultate als auch χ^2-Wert angezeigt:
    >>> messpunkte = np.array([[0.9, 2.3, 4.5], [-2.0, -4.3, -8.6]])
    >>> messfehler = np.array([[0.1, 0.05, 0.08], [0.1, 0.4, 0.3]])
    >>> parameter_schätz  = [-2]
    >>> parameter, parameter_fehler = pap.odr_fit(pap.prop_func, messpunkte, messfehler, 
                                                  parameter_schätz,output_chi_test = 'print')
      Ergebnisse des ODR-Fits:

      Beta: [-1.93158386]
      Beta Std Error: [0.05977981]
      Beta Covariance: [[0.00435563]]
      Residual Variance: 0.8204606240877614
      Inverse Condition #: 1.0
      Reason(s) for Halting:
        Sum of squares convergence


      Ergebnisse des χ^2-Tests:

      χ^2_reduziert         = 0.82
      Fitwahrscheinlichkeit = 44.0%
    
    
    Hier ohne Prints aber mit χ^2-Output:
    >>> output = pap.odr_fit(pap.poly_func, messpunkte, messfehler, parameter_schätz, 
                             print_resultate = False, output_chi_test = True, funktionstyp = 'x, p_list')
    >>> parameter, parameter_fehler, chi_quadrat_liste = output
    
    Damit kann man dann den χ^2-Test separat ausführen:
    >>> pap.chi_quadrat_odr(*chi_quadrat_liste)
      Ergebnisse des χ^2-Tests:

      χ^2_reduziert         = 0.82
      Fitwahrscheinlichkeit = 44.0%
    
    
    Bedeutung des Fit-Resultates
    ----------------------------
      * "Beta" und "Beta Std Error" sind jeweils die Parameter und deren 1σ-Fehler der gefitteten 
        Funktion. Sie heißen im Output  parameter  und  parameter_fehler.
      * "Beta Covariance" ist die Kovarianz-Matrix der Parameter.
      * "Residual Variance" ist der reduzierte χ^2-Wert des Fits. Er taucht auch im Ergebnis des χ^2-Testes
        auf.
      * "Reason(s) for Halting" kann Gründe angeben, warum ein Fit schiefgelaufen ist. 
        "Sum of squares convergence" bedeutet, dass die Optimierfunktion auf einen bestimmten Wert 
        konvergiert ist. Bedeutet aber nicht notwendigerweise, dass die die gefunden Parameter sinnvoll 
        sind, dies sieht man besser mit einem Plot
    '''
    
    
    
    # Überprüfen und Anpassen der Argumente
    x_werte,  y_werte  = messpunkte
    x_fehler, y_fehler = messfehler
    
    if messfehler[messfehler == 0].size != 0:
        print('messfehler darf keine Fehler enthalten, die 0 sind!')
        return
    
    def funktion_kompatibel(parameter, x):
        if funktionstyp == 'x, *p':
            return funktion(x, *parameter)
        elif funktionstyp == 'x, p_list':
            return funktion(x, parameter)
        elif funktionstyp == 'p_list, x':
            return funktion(parameter, x)
        else:
            print('funktionstyp ist falsch angegeben. >:(')
            return
    
    
    # Berechnung des Fits
    modell_funktion = odr.Model(funktion_kompatibel)
    messdaten       = odr.RealData(x_werte, y_werte, x_fehler, y_fehler)
    regression      = odr.ODR(messdaten, modell_funktion, beta0 = parameter0)
    ergebnis        = regression.run()
    
    
    # Einstellen des Outputs und Print-Inhaltes
    return_list = []
    return_list.append(ergebnis.beta)
    return_list.append(ergebnis.sd_beta)
    
    if print_resultate == True:
        print('Ergebnisse des ODR-Fits:\n')
        ergebnis.pprint()
        
    if output_chi_test != False:
        chi_quadrat = ergebnis.sum_square
        anzahl_messwerte = np.shape(messpunkte)[1]
        anzahl_parameter = len(ergebnis.beta)
        chi_test_list = [chi_quadrat, anzahl_messwerte, anzahl_parameter]
        if output_chi_test == True:
            return_list.append(chi_test_list)
        elif output_chi_test == 'print':
            print('\n')
            chi_quadrat_odr(*chi_test_list)
    
    return return_list


        
        
def _chi_quadrat_print(chi_quadrat, anzahl_messwerte, anzahl_parameter):
    '''
    Berechnet χ^2_reduziert und die Fitwahrscheinlichkeit und printet sie als schönes Ergebnis.
    '''
    
    freiheitsgrade         = anzahl_messwerte - anzahl_parameter
    chi_quadrat_reduziert  = chi_quadrat / freiheitsgrade 
    fit_wahrscheinlichkeit = (1 - chi2.cdf(chi_quadrat, freiheitsgrade)) * 100
    
    print('Ergebnisse des χ^2-Tests:\n')
    print(f"χ^2_reduziert         = {chi_quadrat_reduziert:.2f}") 
    print(f"Fitwahrscheinlichkeit = {fit_wahrscheinlichkeit:.1f}%")
        

        
        
def chi_quadrat_test(fit_werte, werte, werte_fehler, anzahl_parameter): 
    '''
    Printet den χ^2_reduziert-Wert und die Fitwahrscheinlichkeit.
    
    
    Argumente
    ---------
    fit_werte: np.array (1D, number_like)
        die Werte, die die Fitfunktion ausgibt, also  fit_werte = fit_func(x_werte, *parameter)
    
    werte: np.array (1D, number_like)
        y-Werte der Messdaten
    
    werte_fehler: np.array (1D, number_like)
        y-Fehler der Messdaten
    
    anzahl_parameter : int (> 0)
        Anzahl Parameter der Fitfunktion
        
        
    Beispiel
    --------
    >>> x_werte = np.array([-8, -5.5, -1.2, 1, 1.4, 3.2, 4.5])
    >>> y_werte = np.array([40, 20.8, 3.1, 0.5, 1.5, 3, 6])
    >>> y_fehler = np.array([0.5, 0.73, 0.42, 0.23, 0.23, 0.41, 0.44])
    >>> fitparameter = [0.46721214, -1.01681483, 1.45102103]
    >>> pap.chi_quadrat_test(pap.quadfunc(x_werte, *fitparameter), y_werte, y_fehler, 3)
      Ergebnisse des χ^2-Tests:

      χ^2_reduziert         = 2.79
      Fitwahrscheinlichkeit = 2.5%
    '''
    
    
    chi_quadrat = np.sum(((fit_werte - werte) / werte_fehler)**2)
    
    _chi_quadrat_print(chi_quadrat, len(werte), anzahl_parameter)
    
    
    
 
def chi_quadrat_odr(chi_quadrat, anzahl_messwerte, anzahl_parameter):
    '''
    Printet den χ^2_reduziert-Wert und die Fitwahrscheinlichkeit für einen ODR-Fit (siehe pap.odr_fit()).
    Die drei Input-Argumente kann man sich von der pap.odr_fit-Funktion mithilfe der Angabe
    output_chi_test = True  als drittes Output-Argument geben lassen.
    
    
    Argumente
    ---------
    chi_quadrat : float (> 0)
    
    anzahl_messwerte : int (> 0)

    anzahl_parameter : int (> 0)
    
    
    Beispiel
    --------
    >>> parameter, parameter_fehler, chi_test_liste = pap.odr_fit(... Argumente ..., output_chi_liste = True)
    ... Geprintetes Ergebnis vom ODR-Fit ...
    >>> pap.chi_quadrat_ord(*chi_test_liste)
    Ergebnisse des χ^2-Tests:
    
    χ^2_reduziert         = 0.82
    Fitwahrscheinlichkeit = 44.0%
    '''
    
    
    _chi_quadrat_print(chi_quadrat, anzahl_messwerte, anzahl_parameter)
    
    
    

    
    
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

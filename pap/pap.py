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

def _rundung_einzel(wert, präzision):
    '''
    Die Rundung mit einem Array von Nachkommastellen  (präzisionen)  funktioniert deshalb, da in rekursiven
    for-Loops die Arrays in einzelne Elemente aufgebrochen werden, welche dann gerundet werden.
    
    
    Argumente (sollten schon durch  _rundung()  passend gemacht worden sein.)
    ---------
    werte : np.ndarray (number_like), number_like
    
    präzisionen : np.ndarray (int), int
    
    
    Output
    ------
    wert_gerundet : np.ndarray (number_like), number_like
        Mit Pythons  round()  auf nächste gerade Ziffer gerundet (symmetrisches Runden).
        Form und Elemente sonst gleich wie  werte.
    '''
    
    
    
    anzahl_dimensionen = np.ndim(wert)   # Entsprechend viele Rekursionen werden stattfinden.
    
    # Eigentliche Rundung
    if anzahl_dimensionen == 0:
        wert_gerundet = round(wert, präzision)
    
    # Aufrufen von  _rundung_einzel()  um in einem for-Loop die Elemente von werte abzuarbeiten.
    elif anzahl_dimensionen > 0:
        wert_form = np.shape(wert)
        wert_gerundet = np.zeros(wert_form)
        for i in range(wert_form[0]):
            wert_gerundet[i] = _rundung_einzel(wert[i], präzision[i])
            
    return wert_gerundet   # Die gesammelten gerundeten Werte werden als Ergebnis zur vorigen Funktion
                           # zurückgeschickt.
    
    
    

def _rundung(werte, präzisionen):
    '''
    Rundet  werte  auf ihre jeweilige Anzahl Nachkommastellen  (präzisionen).
    Im Gegensatz zu  np.round()  kann diese Funktion  werte  mit ganzen Arrays von Nachkommastellen runden.
    Für Details zum Rundungsprozess siehe  _rundung_einzel().
    
    
    Argumente
    ---------
    werte : np.ndarray (number_like), number_like
        Kann beliebige Form haben und auch Einzelwert sein.
    
    präzisionen : np.ndarray (int), int
        Muss gleiche Form wie  werte  haben oder int sein.
    
    
    Output
    ------
    "wert_gerundet" : np.ndarray (number_like), number_like
        Mit Pythons  round()  auf nächste gerade Ziffer gerundet (symmetrisches Runden).
        Form und Elemente sonst gleich wie  werte.
    '''
    
    
    
    # Überprüfung und Anpassung der Argumente
    präzisionen = arr(präzisionen)  # Falls Einzelwert
    if präzisionen.dtype != int:
        print('präzisionen darf nur Integers enthalten!')
        print('Die Anzahl Stellen, auf die gerundet wird, kann nur ganzzahlig sein.')
    
    if np.shape(werte) != np.shape(präzisionen):
        if np.ndim(präzisionen) == 0:   # Falls  präzisionen  Einzelwert, dann wird
                                        # daraus ein Array derselben Form wie  werte  gemacht.
            präzisionen = np.full(np.shape(werte), präzisionen)
        else:
            print('werte und präzisionen müssen die gleiche np.shape haben!')
            print('np.shape(werte) =', np.shape(werte))
            print('np.shape(präzisionen) =', np.shape(präzisionen))
    
    
    # Eigentlicher Rundungsprozess
    return _rundung_einzel(werte, präzisionen)




def _größenordnung(zahlen, art = int):
    if art == int:
        art = 'int64'
    elif art == float:
        art = 'float64'
    einsen = np.ones(np.shape(zahlen))   # 1 hat Größenordnung 0 (welches auch 0 hier haben soll).
    zahlen_kompatibel = np.where(zahlen == 0, einsen, zahlen)
    return arr(np.floor(np.log10(np.abs(zahlen_kompatibel))), dtype = art)




def _erste_ziffer(zahlen, art = float):
    größenordnungen = _größenordnung(zahlen, art = float)
    ziffern = np.abs(zahlen / 10**größenordnungen)
    if art == float:
        return ziffern
    if art == int:
        return np.int_(ziffern)
    
    
    

def _nachkommastelle(zahlen, sig_stellen = 1, sig_grenze = 1.0):
    
    über_der_grenze = _erste_ziffer(zahlen) >= sig_grenze
    sig_stellen_normal = np.full(np.shape(zahlen), sig_stellen)
    signifikante_stellen = np.where(über_der_grenze, sig_stellen_normal, sig_stellen_normal + 1)
    größenordnungen = _größenordnung(zahlen, art = float)
    
    nachkommastellen = -größenordnungen + signifikante_stellen - 1
    
    
    return nachkommastellen




def _negativ_wird_null(array):
    '''
    "Rampenfunktion": Die Werte von array, die negativ sind, werden durch 0 ersetzt.
    
    
    Argument
    --------
    array : np.ndarray (number_like)
    '''
    
    
    nullen = np.full(np.shape(array), 0)
    return np.where(array > 0, array, nullen)


    
    
def _istbool(wert, bool_wert:bool):
    '''
    Überprüft ob wert wirklich bool_wert (True oder False) ist und nicht nur 1 oder 0.
    '''
    
    return (wert == bool_wert and isinstance(wert, bool))



def _listen_transponieren(listen_matrix):
    transponierte_matrix = []
    for i in range(len(listen_matrix[0])):
        zeile = []
        for j in range(len(listen_matrix)):
            zeile.append(listen_matrix[j][i])
        transponierte_matrix.append(zeile)
    return transponierte_matrix




def _füllen(string, index = 0,  menge = 1, füllzeichen = ' '):
    if index == 'rechts':
        index = len(string)
    elif index == 'links':
        index = 0
    string_neu = string[:index] + füllzeichen * menge + string[index:]
    return string_neu




def _entfernen(string, index, länge = 1):
    
    return string[:index] + string[(index + länge):]




def _zentrieren_rechts(string, länge_gewünscht, füllzeichen = ' '):
    länge_string = len(string)
    if länge_gewünscht <= länge_string:
        return string
    else:
        füll_länge        = länge_gewünscht - länge_string
        füll_länge_links  = int(np.ceil(füll_länge / 2))
        füll_länge_rechts = int(np.floor(füll_länge / 2))
        string_zentriert  = füllzeichen * füll_länge_links + string + füllzeichen * füll_länge_rechts
        return string_zentriert
    
    
    

def _zahlen_ausrichtung(zahlen_liste):
    
    länge_abs = len(zahlen_liste)
    test_zahl    = [any(x in string for x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) 
                    for string in zahlen_liste]
    nicht_zahlen = [(i, zahlen_liste.pop(i))  for i in reversed(range(länge_abs))  if not test_zahl[i]][::-1]
        # Pflückt alle nicht-Zahlen von hinten nach vorne aus der zahlen_liste um deren richtige Indices zu 
        # bewahren.
    
    if len(zahlen_liste) != 0:
        länge_abs = len(zahlen_liste)
        anzahl = 9   #% (minus, vor_komma, komma, nach_komma, e, e-, nach_e, text, ende)

        test_minus   = ['-' in string[0] for string in zahlen_liste]
        test_komma   = ['.' in string for string in zahlen_liste]
        test_e       = ['e' in string for string in zahlen_liste]
        test_e_minus = ['e-' in string for string in zahlen_liste]
        test_text    = [' ' in string for string in zahlen_liste]
        längen_strings = [len(string) for string in zahlen_liste]
        indices = np.int_(np.zeros((länge_abs, anzahl)))


        for i in range(länge_abs):
            indices[i][-1] = längen_strings[i]
            if test_text[i]:
                indices[i][7] = zahlen_liste[i].find(' ')
            else:
                indices[i][7] = indices[i][-1]
            if test_e[i]:
                indices[i][4] = zahlen_liste[i].find('e')
                if test_e_minus[i]:
                    indices[i][5] = zahlen_liste[i].find('e-') + 1
                    indices[i][6] = indices[i][5] + 1
                else: 
                    indices[i][5:7] = [indices[i][4] + 1] * 2
            else:
                indices[i][4:7] = [indices[i][7]] * 3
            if test_komma[i]:
                indices[i][2] = zahlen_liste[i].find('.')
                indices[i][3] = indices[i][2] + 1
            else:
                indices[i][2:4] = [indices[i][4]] * 2
            if test_minus[i]:
                indices[i][1] = 1
            else:
                indices[i][1] = 0

        längen = (indices.T[1:] - indices.T[:-1]).T
        längen_max = np.max(längen, axis = 0)
        längen_diff = längen_max[np.newaxis:] - längen

        längen_auswahl = [7, 6, 5, 4, 3, 2, 1, 0]
        indices_auswahl = [7, 5, 5, 4, 4, 2, 0, 0]   #% auf jeden Fall kommentieren.
        for i in range(länge_abs):
            for j in range(len(längen_auswahl)):
                zahlen_liste[i] = _füllen(zahlen_liste[i], menge = längen_diff[i][längen_auswahl[j]], 
                                          index = indices[i][indices_auswahl[j]])
    
        test_leerzeichen = [' ' in string[0] for string in zahlen_liste]
        test_e_leer      = ['e ' in string if 'e' in string else True for string in zahlen_liste]
        if all(test_leerzeichen):
            for i in range(länge_abs):
                zahlen_liste[i] = zahlen_liste[i][1:]
        if all(test_e_leer) and any(test_e):
            index_e_string = test_e.index(True)
            index_nach_e   = zahlen_liste[index_e_string].index('e') + 1
            zahlen_liste = [_entfernen(string, index_nach_e) for string in zahlen_liste]
        
        länge_gesamt = len(zahlen_liste[0])
    else:
        länge_gesamt = max([len(string) for i, string in nicht_zahlen])
    for tupel in nicht_zahlen:
        zahlen_liste.insert(tupel[0], _zentrieren_rechts(tupel[1], länge_gesamt))
    
    return zahlen_liste




def _plus_minus(string_liste):
    plus_minus = []
    for i in range(len(string_liste)):
        if string_liste[i] == '':
            plus_minus.append('')
        elif all([zeichen == ' ' for zeichen in string_liste[i]]):
            plus_minus.append('   ')
        else:
            plus_minus.append(' ± ')
    return plus_minus
    

    
    
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
        präzision = _negativ_wird_null(präzision)   # Keine negativen Werte für format(prec=) erlaubt.
        if rel_fehler != 0:
            if größenordnung > -5:   # Sehr kleine Werte sehen besser mit e aus.
                rel_fehler_string = '   ({:.{prec}f} %)'.format(rel_fehler, prec = präzision)
            else:
                rel_fehler_string = '   ({:.1f}e{} %)'.format(rel_fehler * 10**(-größenordnung),
                                                              größenordnung, prec = präzision)
        else:
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
    nachkommastellen = _negativ_wird_null(nachkommastellen)   # Keine negativen Werte für 
                                                              # format(prec=) erlaubt.
    
    
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

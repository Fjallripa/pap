# Docstring des pap-Paketes
'''
Dieses Python-Paket soll repetitive Aufgaben der Physikexperiment-Auswertungen im Studium schneller, 
einfacher und schöner lösen als das manuell möglich wäre.  

Aktuell lassen sich die Features in 5 Bereiche aufteilen:  
* Fehlerrechnung
* Einfache Statistik
* Resultat-Darstellung und -Vergleich
* Fits und Chi^2-Tests
* Grundlegende Fitfunktionen

Installationshinweise: Siehe how-to-make-import-pap-work.md im Ordner dieses Paketes.



Übersicht der Bereiche
----------------------
Fehlerrechnung:
    * pap.summen_fehler()  und  pap.produkt_fehler()
        vereinfachen einem die gauß'sche Fehlerfortpflanzung.
        Zur Berechnung muss man nur die benötigten Werte und Fehler einsetzen.
        

Einfache Statistik:
    * pap.std() 
        berechnet den Experimentellen Fehler des Einzelwertes
        np.std() tut dies nämlich nicht, Näheres dazu im pap.std()-Docstring
    
    * pap.mittel()  und  pap.mittel_fehler()
        entsprechen jeweils np.mean() und dem Experimentellen Fehler des Mittelwertes
    
    * pap.fwhm()
        wandelt σ in FWHM bzw. Halbwertsbreite um


Resultat-Darstellung und Vergleich:
    * pap.resultat()
        printet ein schön formatiertes Ergebnis mit 
        Titel, definierter Präzision, evt. +/- Fehler, Einheit und evt. relativen Fehler.
        
        Beispiel:
        >>> pap.resultat('Arbeit', np.array([3.3520e6, 0.4684e6]), 'MJ', faktor = 1e-6)
          Arbeit: 3.4 +/- 0.5 MJ
          
    * pap.vergleichstabelle()
        printet einen wissenschaftlichen Vergleich von fehlerbehafteten experimentellen und 
        theoretischen Werten in Tabellenform. 
         - Absolute, relative und sigma-Abweichung werden berechnet.
         - Die Werte sind nach Größenordnung ausgerichtet und wissenschaftlich gerundet.
         - Darstellung der Vergleiche als Blöcke oder als Liste möglich.
         - Robust gegen Extremfälle und fehlende Werte.
        
        Beispiel:
        >>> titel  = 'Literaturvergleich Fallbeschleunigung'
        >>> werte  = np.array([[3.446, 0.00204], [0.105, 0.00045], [3.69, 0], [5e-3, 0]])
        >>> größen = ['Boden', 'Orbit']
        >>> vergleichstabelle(werte, titel, einheit = 'm/s^2', größen = größen, 
                              beschreibung = 'knapp')
          Literaturvergleich Fallbeschleunigung

           [m/s^2]       Boden             Orbit     
          --------   --------------   ---------------
          Wert exp    3.45  ± 0.10    0.0020 ± 0.0004
               the    3.690 ± 0.005   0.0    ± 0.0   
          Abw. abs   -0.24  ± 0.11    0.0020 ± 0.0004
               rel       -6.6 %              -       
               sig        2.3 σ            4.5 σ      

        
Fits und Chi^2-Tests:
    * pap.odr_fit()
        fittet Funktionen ähnlich wie SciPys curve_fit() nur mit Berücksichtigung des x-Fehlers, 
        was wichtig wird, wenn dieser der dominante Fehler ist. 
        Diese Funktion benutzt direkt SciPys odr-Paket, ist aber wesentlich einfacher 
        zu bedienen.
    
    * pap.chi_quadrat_test()  und  pap.chi_quadrat_odr()
        führen einen χ^2-Test zu Bestimmung der Güte des Fits durch.
        Erstere nimmt die Ergebnisse von SciPys curve_fit() auf, während zweitere die von 
        pap.odr_fit() benutzt und damit auch den x-Fehler berücksichtigt.
        
        Beispiel: (für Orignal-Werte, siehe den pap.chi_quadrat_test()-Docstring)
        >>> pap.chi_quadrat_test(pap.func.quad(x_werte, *fitparameter), y_werte, y_fehler, 3)
          Ergebnisse des χ^2-Tests:

          χ^2_reduziert         = 2.79
          Fitwahrscheinlichkeit = 2.5%
          
        
Grundlegende Fitfunktionen:
    (mehr Infos im Docstring von pap.func)
    * pap.func.konst()  - Konstante Funktion
    * pap.func.prop()   - Proportionale Funktion
    * pap.func.lin()    - Lineare Funktion
    * pap.func.quad()   - Quadratische Funktion
    * pap.func.poly()   - allgemeines Polynom
    * pap.func.exp()    - Exponentialfunktion
    * pap.func.gauss()  - Gaußverteilung
'''






# Alle benötigten Pakete

import numpy as np
from numpy import array as arr
from scipy.stats import chi2
from scipy import odr

from pap import func   # Ermöglicht es, direkt pap.func-Funktionen zu nutzen wenn nur `import pap` ausgeführt wurde.

  




# Konstanten

ZIFFERN = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')






# Fehlerrechnung

def summen_fehler(fehler_array):
    '''
    Quadratische Addition der Fehler einer Summe
    
    Die Form dieser Summe soll sein  wert1 + wert2 + ... + wertn.
    fehler_array soll eine Form haben wie  [fehler_wert1, ..., fehler_wertn].
    '''
    
    return np.linalg.norm(fehler_array, axis = 0)




def produkt_fehler(produkt, rel_fehler_array):
    '''
    Quadratische Addition der relativen Fehler eines Produktes (optional inkl. Potenzen)
    
    Die Form dieses Produktes soll sein  wert1**n1 * wert2**n2 * ... * wertn**nn.
    fehler_array soll eine Form haben wie  [relativer_fehler_wert1, ..., relativer_fehler_wertn]
    mit  relativer_fehler_wert1 = n1 * fehler_wert1 / wert1,  wobei  n1  dessen Potenz ist.
    
    Wenn produkt = 1 gewählt wird, erhält man den relativen Fehler.
    '''
    
    relativer_fehler = np.linalg.norm(rel_fehler_array, axis = 0)
    return np.abs(produkt) * relativer_fehler






# Statistik

def std(*args, **kwargs):
    '''
    Experimenteller Fehler des Einzelwertes
    
    Die Funktion ist identisch zu np.std() inkl. aller Argumente, 
    außer dass ddof = 1 gesetzt wird wenn nicht spezifisch angegeben.
    Wenn σ die Varianz einer Werteverteilung X mit N Werten ist, dann wird also im Normalfall berechnet
    std = sqrt(σ(X) / (N - 1)).
    '''
    
    if not ('ddof' in kwargs):
        kwargs['ddof'] = 1
    return np.std(*args, **kwargs)




def mittel(*args, **kwargs):
    '''
    Mittelwert
    
    Die Funktion ist identisch zu np.mean() inkl. aller Argumente
    und dient nur besseren Lesbarkeit inmitten von anderen pap-Funktionen.
    '''
    
    return np.mean(*args, **kwargs)




def mittel_fehler(*args, **kwargs):
    '''
    Experimenteller Fehler des Mittelwertes
    
    Die Funktion berechnet std(X) / sqrt(N) von einer Werteverteilung X mit N Werten.
    Dabei ist std() = pap.std() also der Experimentelle Fehler des Einzelwertes.
    Somit lassen sich genau die gleichen Argumente wie in np.std() einsetzen.
    '''
    
    
    werte = args[0]
    shape = np.shape(werte)
    if shape == (0,):   # Verhindert Fehlermeldung falls werte == []
        return np.nan
    
    if 'axis' in kwargs and kwargs['axis'] != None:   
        # Zweite Bedingung im if-Satz nötig, wenn man explizit axis = None angibt.
        achsen        = kwargs['axis']
        shape_rest    = (shape[achsen]  if type(achsen) == int  
                         else arr([shape[i] for i in achsen]))
        anzahl_zahlen = np.prod(shape_rest)
    else:
        anzahl_zahlen = np.product(shape)
    
    
    fehler_des_mittelwertes = std(*args, **kwargs) / np.sqrt(anzahl_zahlen)
    return fehler_des_mittelwertes




def fwhm(sigma):
    '''
    Halbwertsbreite (Full Width Half Mean):
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
    '''
    Bestimmt elementweise die Größenordnungen eines Arrays von Zahlen und gibt sie als int- oder float-Array 
    zurück. 
    0 bekommt die Größenordnung 0.
    
    
    Argumente
    ---------
    zahlen : np.ndarray (number_like)
        
    art : type, optional
        Darf nur sein:
        int   - größenordnungen-Array wird aus np.int64-Zahlen bestehen, zB. 0.048 -> -2
        
        float - größenordnungen-Array wird aus np.float64-Zahlen bestehen. zB. 0.048 -> -2.0
        
        
    Output
    ------
    größenordnungen : np.ndarray  (np.int64 oder np.float64)
        np.shape(größenordnungen) = np.shape(zahlen)
    '''
    
    
    
    if art == int:
        art = 'int64'
    elif art == float:
        art = 'float64'
    
    # Nullen werden kompatibel gemacht.
    einsen            = np.ones(np.shape(zahlen))   # 1 hat Größenordnung 0 (welches auch 0 hier haben soll).
    zahlen_kompatibel = np.where(zahlen == 0, einsen, zahlen)
    
    return arr(np.floor(np.log10(np.abs(zahlen_kompatibel))), dtype = art)




def _erste_ziffer(zahlen, art = float):
    '''
    Bestimmt elementweise die erste Ziffer eines Arrays von Zahlen wenn art = int, aber
    wenn art = float, wird die Zahl nur auf Größenordnung null gebracht.
    
    
    Argumente
    ---------
    zahlen : np.ndarray (number_like)
    
    art : type, optional
        Darf nur sein:
        int   - ziffern-Array wird aus np.int64-Zahlen bestehen, zB. 239.78 -> 2
        
        float - ziffern-Array wird aus np.float64-Zahlen bestehen, zB. 239.78 -> 2.3978 
        
    
    Output
    ------
    ziffern : np.ndarray  (np.int64 oder np.float64)
        np.shape(ziffern) = np.shape(zahlen)
    '''
    
    
    
    größenordnungen = _größenordnung(zahlen, art = float)
    ziffern         = np.abs(zahlen / 10**größenordnungen)
    
    if art == float:
        return ziffern
    if art == int:
        return np.int_(ziffern)
    
    
    

def _nachkommastelle(zahlen, sig_stellen = 1, sig_grenze = 1.0):
    '''
    Berechnet elementweise die Anzahl der Nachkommastellen, auf die eine Zahl gerundet werden soll, 
    abhängig davon wie viele signifikante Stellen zugelassen werden und davon wo die Signifikanz-Grenze liegt.
    Mehr Details unter "Berechnung".
    
    
    Argumente
    ---------
    zahlen : np.ndarray (number_like)
    
    sig_stellen : int, optional
        Nur Zahlen >= 1 sinnvoll
    
    sig_grenze : int, float, optional
        Nur Zahlen >= 1 und < 10 sinnvoll
    
    
    Output
    ------
    nachkommastellen : np.ndarray (np.float64)
        np.shape(nachkommastellen) = np.shape(zahlen)
    
    
    Berechnung
    ----------
    Rundet man eine Zahl wissenschaftlich, dann will man sie auf eine bestimmte Anzahl signifikanter Stellen 
    runden, zB. bei Fehlerwerten auf oft nur eine: 1.389342 -> 1.
    Stur auf eine signifikante Stelle zu runden wird aber bei Zahlen mit kleinen ersten Ziffern problematisch
    wie in oberem Beispiel. Der gerundete Wert könnte zwischen 0.5 und 1.5 liegen, wodurch man einen unnötig 
    großen Darstellungsfehler introduziert.
    Um dieses Problem zu beheben, wurde eine Signifikanzgrenze eingeführt. Ist die erste Ziffer des zu 
    rundenden Wertes kleiner als diese Grenze, wird der Wert mit einer signifikanten Stelle mehr gerundet.
    
    Beispiel 1: Sei die Signifikanzgrenze sig_grenze = 4 (Darstellungsfehler max. 1/8)
                und die normale Anzahl signifikanter Stellen sig_stellen = 1.
    0.002458 -> 0.0025 (nachkommastelle =  4)
    828.003  -> 800    (nachkommastelle = -2)
    4.001    -> 4      (nachkommastelle =  0)
    3.999    -> 4.0    (nachkommastelle =  1)
    3.949    -> 3.9    (nachkommastelle =  1)
    1.034    -> 1.0    (nachkommastelle =  1)
    0.928    -> 0.9    (nachkommastelle =  1)
    0.434    -> 0.4    (nachkommastelle =  1)
    0.394    -> 0.39   (nachkommastelle =  2)
    
    Beispiel 2: Will man bei oberen Beispielen vermeiden, dass sowohl 4 als auch 4.0 auftauchen,
    kann man sig_grenze = 3.95 wählen. Dann ergibt sich
    4.000 -> 4
    3.999 -> 4
    3.950 -> 4
    3.949 -> 3.9
    '''
    
    
    über_der_grenze      = _erste_ziffer(zahlen) >= sig_grenze
    sig_stellen_normal   = np.full(np.shape(zahlen), sig_stellen)
    signifikante_stellen = np.where(über_der_grenze, sig_stellen_normal, sig_stellen_normal + 1)
    größenordnungen      = _größenordnung(zahlen, art = float)
    
    nachkommastellen     = -größenordnungen + signifikante_stellen - 1
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
    '''
    Transponiert eine Liste, die eine Form wie ein 2D np.ndarray hat.
    
    
    Argumente
    ---------
    listen_matrix : list
        Muss aus einer Liste von N Listen, welche alle M Elemente haben, bestehen.
        Also "shape"(listen_matrix) = (N, M).
    
    
    Output
    ------
    tranxponierte_matrix : list
        "shape"(transponierte_maxtrix) = (M, N)
    '''
    
    
    
    transponierte_matrix = []
    for i in range(len(listen_matrix[0])):
        zeile = []
        for j in range(len(listen_matrix)):
            zeile.append(listen_matrix[j][i])
        transponierte_matrix.append(zeile)
    
    return transponierte_matrix




def _füllen(string, index = 0,  menge = 1, füllzeichen = ' '):
    '''
    fügt eine bestimmte Menge an Füllzeichen an eine bestimmte Position eines Strings.
    Ähnlich zu Pythons .format()-Methode, wo der String eine festgelegte Breite haben soll und mit entsprechend
    vielen Füllzeichen aufgefüllt wird. Hier kann man stattdessen die Anzahl der Füllzeichen festlegen und auch
    die genaue Einsetz-Position.
    
    
    Argumente
    ---------
    string : str
    
    index : int, str, optional
        Position im string, wo die füllzeichen eingefügt werden sollen
        Wenn type(index) == str, dann darf index nur sein:
        index = 'links'    (= 0) -> füllzeichen ganz links einfügen
        
        index = 'rechts'   (= len(string)) -> füllzeichen ganz rechts einfügen
    
    menge : int, optional
        Anzahl gewünschter füllzeichen
    
    füllzeichen : str, optional
    
    
    Output
    ------
    string_neu : str
    '''
    
    
    if index == 'rechts':
        index = len(string)
    elif index == 'links':
        index = 0
        
    string_neu = string[:index] + füllzeichen * menge + string[index:]
    return string_neu




def _entfernen(string, index, länge = 1):
    '''
    entfernt eine bestimmte Anzahl (länge) Zeichen von einem String ab einem bestimmten Index.
    
    
    Argumente
    ---------
    string : str
    
    index : int, optional
        Nur index >= 0 sinnvoll.

    länge : int, optional
        Nur länge >= 0 sinnvoll.
        
    
    Output
    ------
    string_output : str
    '''
    
    
    return string[:index] + string[(index + länge):]




def _zentrieren_rechts(string, länge_gewünscht, füllzeichen = ' '):
    '''
    arbeitet so wie '{:^{width}'.format(string, width = länge_gewünscht), mit dem Unterschied dass .format bei 
    einer ungeraden Anzahl Füllzeichen, den string ein bisschen nach links anordnet:    'Hi' -> ' Hi  '
    Diese Funktion ordnet in einem solchen Fall den string ein bisschen nach rechts an: 'Hi' -> '  Hi '
    Ist die Anzahl Füllzeichen gerade, benehmen sich beide Funktionen gleich:           'Hi' -> '  Hi  '
    
    Argumente
    ---------
    string : str
    
    länge_gewunscht : int
    
    füllzeichen : str, optional
    
    
    Output
    ------
    string_zentriert : str
    '''
    
    
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
    '''
    wandelt eine Liste unterschiedlich langer Zahlenstrings in eine Lister gleichlanger Zahlenstrings um,
    die nach Komma ('.'), Größenordnung ('e') und Einheit (zB. ' %') ausgerichtet sind, siehe "Beispiel".
    
    
    Argumente
    ---------
    zahlen_liste : list  (str)
        Unterstützte Arten von Strings sind:
        * int- und float-Strings (auch mit 'e')
        * solche Strings mit einem Leerzeichen und Einheit hinten dran (zB. '1.4e-3 %')
        * einzelne Zeichen (zB. '-')
        * leere Strings
        
    
    Output
    ------
    zahlen_liste : list  (str)
        
    
    Beispiel
    --------
    >>> pap._zahlenausrichtung(['23.3',
    ...                         '2.940e12',
    ...                         '-94',
    ...                         '2030 %'
    ...                         '-6.19e-3'
    ...                         '-',
    ...                         ''])
    ['   23.3       ',
     '    2.940e12  ',
     '  -94         ',
     '-2030        %',
     '   -6.19 e-3  ',
     '      -       ',
     '              ']
    '''
    
    
    # Vorbearbeitung der Liste
    anzahl_strings    = len(zahlen_liste)
    if anzahl_strings == 0:
        return zahlen_liste
    
    ''' Nur Zahlenstrings können ausgerichtet werden, deshalb werden alle anderen
    herausgeplückt.'''
    test_zahl    = [any(x in string for x in ZIFFERN) 
                    for string in zahlen_liste]
    nicht_zahlen = [(i, zahlen_liste.pop(i))  for i in reversed(range(anzahl_strings))  
                    if not test_zahl[i]] [::-1]
    ''' Pflückt alle nicht-Zahlen von hinten nach vorne aus der zahlen_liste um deren richtige Indices zu 
    bewahren.'''
    
    
    # Ausrichten der Zahlenstrings
    if len(zahlen_liste) != 0:

        '''Die Zahlenstrings werden in 9 Bereiche unterteilt:
        minus, vor_komma, komma, nach_komma, e, e-, nach_e, text und ende.
        String-Bsp: '-23.383e-10 %' '''
        anzahl_strings       = len(zahlen_liste)
        anzahl_bereiche = 9 
        indices         = np.int_(np.zeros((anzahl_strings, anzahl_bereiche)))
        längen_strings  = [len(string) for string in zahlen_liste]
        

        '''Nach allen diesen Zeichen unten werden die Strings ausgerichtet. Insbesondere sollen '.' und 'e' 
        alle vertikal übereinander sfein.'''
        test_minus   = ['-'  in string[0] for string in zahlen_liste]
        test_komma   = ['.'  in string    for string in zahlen_liste]
        test_e       = ['e'  in string    for string in zahlen_liste]
        test_e_minus = ['e-' in string    for string in zahlen_liste]
        test_text    = [' '  in string    for string in zahlen_liste]
        
        
        '''Hier werden die Anfangs-Indices aller 9 Bereiche bestimmt. Ist ein Bereich nicht vorhanden, bekommt 
        er den Index des nachfolgenden Bereiches. Deshalb werden die Indices vom hintersten Bereich vorwärts
        bestimmt.'''
        for i in range(anzahl_strings):
            indices[i][-1] = längen_strings[i]   # ende
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

        
        '''Aus allen Indices werden die Längen der einzelnen Bereiche bestimmt und daraus die Menge an
        Füllung, die benötigt wird. Diese wird schließlich bei allen Strings an der richtigen Stelle#
        eingefügt.'''
        längen      = (indices.T[1:] - indices.T[:-1]).T   
            # Längen der Bereiche, sortiert nach Bereich, np.shape(längen) = (anzahl_bereiche, anzahl_strings)
        längen_max  = np.max(längen, axis = 0)   # Maximum-Länge jedes Bereiches
        längen_diff = längen_max[np.newaxis:] - längen     
            # Anzahl benötigte Leerzeichen um jeden Bereich bis zur Max-Länge aufzufüllen.

        ## Einfügen der Füllungen
        längen_auswahl  = [7, 6, 5, 4, 3, 2, 1, 0]
        indices_auswahl = [7, 5, 5, 4, 4, 2, 0, 0]   
        '''Dies ist wie folgt zu lesen: Bereich text (7) wird als erstes aufgefüllt. Bereiche e- (5) und 
        nach-e (6) bleiben zusammen und es wird der Platz 5 zwischen dem 'e' und dem '-' aufgefüllt. 
        Auch der Platz 4 zwischen Bereichen e (4) und nach-komma (3) wird gefüllt. Das gleiche gilt für
        Platz 0 vor Bereichen minus (0), vor-komma (1) und komma (2). Fehlt im Zahlenstring irgendeiner
        dieser Bereiche wird sein Platz ebenso gefüllt.'''
        for i in range(anzahl_strings):
            for j in range(len(längen_auswahl)):
                zahlen_liste[i] = _füllen(zahlen_liste[i], menge = längen_diff[i][längen_auswahl[j]], 
                                          index = indices[i][indices_auswahl[j]])
    
        
        # Nachbearbeitung bei Sonderfällen
        '''Wenn Minuszeichen vorhanden sind, wird überall ein Leerzeichen an Füllung deswegen eingebracht.
        Da die Minuszeichen aber bei ihren Zahlen bleiben, kann es passieren, dass eine ganze Spalte an 
        Leerzeichen existiert (all(...)). Dieser wird hier entfernt, da überflüssig.'''
        test_leerzeichen = [' ' in string[0] for string in zahlen_liste]
        test_e_leer      = ['e ' in string if 'e' in string else True for string in zahlen_liste]
        if all(test_leerzeichen):
            for i in range(anzahl_strings):
                zahlen_liste[i] = zahlen_liste[i][1:]
        if all(test_e_leer) and any(test_e):
            index_e_string = test_e.index(True)
            index_nach_e   = zahlen_liste[index_e_string].index('e') + 1
            zahlen_liste   = [_entfernen(string, index_nach_e) for string in zahlen_liste]
        
        
        länge_gesamt = len(zahlen_liste[0])
    else:   # Falls keine Zahlenstrings in zahlen_liste vorhanden
        länge_gesamt = max([len(string) for i, string in nicht_zahlen])
    
    
    # Zentrierte nicht-Zahlenstrings werden wieder in die Liste eingefügt.
    for index, string in nicht_zahlen:
        zahlen_liste.insert(index, _zentrieren_rechts(string, länge_gesamt))
            
            
    return zahlen_liste



def _plus_minus(string_liste):
    '''
    entscheidet, welche Strings in einer Liste von Strings mit einem Plus-Minus-Zeichen versehen werden 
    sollen und welche nicht. Diese Funktion ergibt nur als direkte Hilfsfunktion von pap.vergleichstabelle()
    Sinn.
    
    
    Argumente
    ---------
    string_liste : list  (str) 
    
    
    Output
    ------
    plus_minus : list  (str)
    '''
    
    
    plus_minus = []
    for string in string_liste:
        if string == '':   # Falls string leer ist.
            plus_minus.append('')
        elif all([zeichen == ' ' for zeichen in string]):   # Falls string nur aus Leerzeichen besteht.
            plus_minus.append('   ')
        else:
            plus_minus.append(' ± ')   # Falls string aus mehr besteht.
    
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


        
        
def vergleichstabelle(werte, titel = '', einheit = '', größen = '', faktor = 1, ausrichtung = 'blöcke', 
                      beschreibung = 'standard'):
    '''
    Printet einen wissenschaftlichen Vergleich von fehlerbehafteten experimentellen und theoretischen Werten in 
    Tabellenform. 
    Berechnet und angezeigt werden zusätzlich absolute und relative sowie sigma-Abweichungen.
    Die Werte sind zur besseren Vergleichbarkeit in ±-Darstellung, nach Komma und Exponent ausgerichten als auch 
    gerundet entsprechend der Größe ihrer Fehler (siehe "Berechnung und Rundung").
    
    Die Vergleiche können sowohl nebeneinander als 'blöcke' dargestellt werden als auch untereinander als 'liste'.
    Einheit sowie Überschriften der einzelnen Vergleiche (größen) können auch angegeben werden.
    Randfälle sowie "div-by-0"-Probleme und fehlende Werte (None) werden automatisch hantiert.
    Ein Überblick der Darstellungsoptionen ist in "Beispiele" zu finden.
    


    Argumente
    ---------
    werte : np.ndarray (1D/2D, mit number_like oder None Elementen)
        Darf folgende Formen haben:
        * shape = (4, 0), np.array([ex_wert, ex_fehler, theo_wert, theo_fehler ])
        * shape = (4, N), np.array([ex_liste, ex_fehler_liste, theo_liste, theo_fehler_liste]) mit  Listenlänge N, 
                          N = Anzahl der Wertvergleiche, die gemacht werden sollen.
        
        Art der Werte:
        Die Elemene dürfen reellwertige Zahlen sein (int, bool oder numpy-Äquivalente) oder None sein.
        Ein Fehler-Wert, der None ist, wird als 0 interpretiert. Ein ex-/theo_wert der None ist, wird als fehlende Zahl 
        interpretiert und es wird kein Vergleich durchgeführt, siehe "Beispiele".
        
    titel : str, optional
        Tabellentitel, unbearbeitet
    
    einheit : str, optional
        Wird in der oberen linken Zelle als Einheit der verglichen Werte gekennzeichnet sein.
    
    größen : str, array_like (1D, mit str Elementen), optional
        Überschriften für jeden Vergleich. Werden je nach Ausrichtung in der Titelzeile bzw. -spalte des 
        jeweiligen Vergleichs angezeigt.
        Darf folgende Formen haben:
        * str                   - einzelne Überschrift
        * Liste bis Länge N     - bis zu eine Überschrift für jeden Vergleich. Bei weniger Überschriften 
                                  bekommen die letzten Vergleiche keine Überschrift.
        * Liste von Länge N + 1 - nur möglich, wenn einheit nicht angegeben. Erster String der Liste 
                                  ersetzt einheit und die Kennzeichnung 'Einheit' bzw. '[...]'. Die 
                                  restlichen Strings sind die jeweiligen Vergleichsüberschriften.
    
    faktor : number_like, optional
        wird multipliziert mit allen Werten. Falls die angegebene Einheit (oder Größenordnung) nicht die ist, in der 
        gerechnet wurde.
    
    ausrichtung : str, optional
        Darf nur sein:
        'blöcke'  - Vergleiche nebeneinander als "Blöcke".
        
        'liste'   - Vergleiche übereinander als Liste von Zeilen.
    
    beschreibung : str, optional
        meint die Überschriften wie "Wert experimentell", "Abweichung absolut" etc.
        Darf nur sein:
        'standard' - Überschriften in voller Länge, zB. "Abweichung sigma"
        
        'knapp'    - Überschriften abgekürzt, zB. "Abw. sig"
        
        
    
    Beispiele
    ---------
    * Gewöhnlicher Vergleich:
    >>> titel = 'Literaturvergleich Fallbeschleunigung'
    >>> werte = arr([9.634, 0.274, 9.810, 5e-4])
    >>> vergleichstabelle(werte, titel, einheit = 'm/s^2')
      Literaturvergleich Fallbeschleunigung
  
             Einheit    m/s^2                         
      ------------------------   --------------
      Wert       experimentell    3.45  ± 0.10 
                 theoretisch      3.690 ± 0.005
      Abweichung absolut         -0.24  ± 0.11 
                 relativ             -6.6 %    
                 sigma                2.3 σ    
  
    
    * Knappe Beschreibung
      + "div-by-0"
    >>> werte  = np.array([[3.446, 0.00204], [0.105, 0.00045], [3.69, 0], [5e-3, 0]])
    >>> größen = ['Boden', 'Orbit']
    >>> vergleichstabelle(werte, titel, einheit = 'm/s^2', größen = größen, beschreibung = 'knapp')
      Literaturvergleich Fallbeschleunigung
      
       [m/s^2]       Boden             Orbit     
      --------   --------------   ---------------
      Wert exp    3.45  ± 0.10    0.0020 ± 0.0004
           the    3.690 ± 0.005   0.0    ± 0.0   
      Abw. abs   -0.24  ± 0.11    0.0020 ± 0.0004
           rel       -6.6 %              -       
           sig        2.3 σ            4.5 σ      

    
    * Listenansicht
      + stark variierende Größenordnungen
      + fehlende Werte
    >>> titel  = 'Erneute Messungen der Strahlenexposition'
    >>> werte  = np.array([[0.039, 5.392,  7372.038, 0.299, 4703822.612, 345.384], 
                           [0.018, 0.385,   274.340, 0.070,   53891.349,  18.239], 
                           [0.031, 5.408, 10381.949, 0.285, 8239403.217,    None], 
                           [0.012, 0.094,    93.911, 0.033,    3495.384,   None]])
    >>> größen = ['Ort A', 'Ort B', 'Ort C', 'Ort D', 'Ort E', 'Ort F (neu)']
    >>> vergleichstabelle(werte, titel, einheit = 'µS/h', ausrichtung = 'liste', größen = größen)
      Erneute Messungen der Strahlenexposition
  
        Einheit   |                       Wert                       |                  Abweichung                  
         µS/h     |     experimentell      |       theoretisch       |         absolut         | relativ  |  sigma  
      --------------------------------------------------------------------------------------------------------------
      Ort A       |    0.039   ±     0.018 |     0.031    ±    0.012 |     0.008   ±     0.022 |  26    % |  0.37  σ
      Ort B       |    5.39    ±     0.38  |     5.41     ±    0.09  |    -0.0     ±     0.4   |  -0.30 % |  0.040 σ
      Ort C       | 7370       ±   270     | 10380        ±   90     | -3010       ±   290     | -29    % | 10     σ
      Ort D       |    0.30    ±     0.07  |     0.285    ±    0.033 |     0.01    ±     0.08  |   4.9  % |  0.18  σ
      Ort E       |    4.70 e6 ± 50000     |     8.2394e6 ± 3500     |    -3.54 e6 ± 50000     | -43    % | 65     σ
      Ort F (neu) |  345       ±    18     |                         |                         |          |         
      
    
    * Listenansicht knapp
      + größen[0] ersetzt einheit
    >>> titel  = 'Vergleich der Viskositäten nach Stokes bzw. Hagen-Poiseuille'
    >>> werte  = arr([[1.2515, 1.3855, 1.4089], [0.0239, 0.0156, 0.0227], 
                      [1.4000, 1.4000, 1.6480], [0.0010, 0.0010, 0.0005]])
    >>> größen = ['Adiabatenkoeffizient', 'Clément-Desormes Luft', 'Rüchhardt        Luft', 'Rüchhardt        Argon']
    >>> vergleichstabelle(werte, titel, größen = größen, ausrichtung = 'liste', beschreibung = 'knapp')
      Vergleich der Viskositäten nach Stokes bzw. Hagen-Poiseuille
  
                             |              Wert               |                Abw.               
       Adiabatenkoeffizient  |      exp      |       the       |      abs       |   rel   |   sig  
      ---------------------------------------------------------------------------------------------
      Clément-Desormes Luft  | 1.252 ± 0.024 | 1.4000 ± 0.0010 | -0.148 ± 0.024 | -11   % |  6.2  σ
      Rüchhardt        Luft  | 1.386 ± 0.016 | 1.4000 ± 0.0010 | -0.014 ± 0.016 |  -1.0 % |  0.93 σ
      Rüchhardt        Argon | 1.409 ± 0.023 | 1.6480 ± 0.0005 | -0.239 ± 0.023 | -15   % | 11    σ



    Berechnung und Rundung
    ----------------------
    Die Vergleichswerte werden wie folgt berechnet:
    * abweichung_abs        = wert_ex - wert_theo
    * abweichung_abs_fehler = np.sqrt(wert_ex_fehler**2 + wert_theo_fehler**2)
    * abweichung_rel        = abweichung_abs / wert_theo
    * abweichung_sig        = abweichung_abs / abweichung_abs_fehler
    * Bei einem "div-by-0"-Fall wird der entsprechende Vergleichswert mit '-' ersetzt.
    
    Art der Rundung: symmetrisches Runden
    * gerundet wird mit Pythons round()
    * Im Gegensatz zum Schulrunden wird bei 5 nicht immer aufgerundet sondern zur nächsten geraden Zahl.
    * Bsp.: 10.5 -> 10,  11.5 -> 12,    2.5 -> 2,  3.5 -> 4
    * Beim Runden von vielen Zahlen reduziert dies den systematischen Fehler, der durchs Runden entsteht.
    
    Gerundet wird nach der Größe des Fehlers:
    * Dieser wird auf eine signifikante Stelle gerundet, wenn die erste Ziffer größer als 3 ist.
      - Wenn die erste Ziffer kleiner ist, wird auf zwei signifikante Stellen gerundet.
      - Ist der Fehler 0, dann wird auf eine Nachkommastelle gerundet.
    * Die Absolutzahl wird auf ebenso viele Nachkommastellen wie ihr Fehler gerundet
      - Also, '123.46 ± 0.04' aber '123.456 ± 0.039'
    * relative und sigma Abweichung werden immer auf zwei signifikante Stellen gerundet.
      - Wenn eine 0 ist, sieht das so aus: '0.00 %'
    * Rundung ohne Komma ist auch möglich: '1624.2 ± 59.9' -> '1600 ± 60'

    Ausrichtung der Zahlen erfolgt nach Komma und Exponent:
    * Zahlen ab der Größenordnung 10^5 bzw. 10^-5 werden in Exponententenschreibweise dargestellt, zB. '1.38e-23'
      - Deren Kommas werden um Platz zu sparen genau wie die anderen Kommas ausgerichtet.
    * Minuszeichen bleiben an ihren Zahlen haften.
    Beispiel:
    '   -3.28   e18'
    '49200         '
    '  -58.07023   '
    '    0.0034    '
    '    2.933  e-9'
    '''



    # Überprüfen der Argumente
    werte_typ = type(werte)
    if werte_typ != np.ndarray:
        print(f'Eingabefehler: type(werte) = {werte_typ}')
        print('werte muss ein numpy Array sein.\n')
        return
    werte_shape = np.shape(werte)
    if (not len(werte_shape) in [1, 2]) or werte_shape[0] != 4:
            print(f'Eingabefehler: shape(werte) = {werte_shape}')
            print('werte muss die shape  (4, n) mit n = 0, 1, 2, ...  haben.\n')
            return
    
    titel_typ = type(titel) 
    if titel_typ != str:
        print(f'Eingabefehler: type(titel) = {titel_typ}')
        print('titel muss ein String sein.\n')
        return
    
    einheit_typ = type(einheit)
    if einheit_typ  != str:
        print(f'Eingabefehler: type(einheit) = {einheit_typ}')
        print('einheit muss ein String sein.\n')
        return
    
    # größen siehe: "# Vorbereitung Größenliste"
    
    ausrichtung_optionen = ['blöcke', 'liste']
    if not ausrichtung in ausrichtung_optionen:
        print(f'Eingabefehler: ausrichtung = {ausrichtung}')
        print(f'ausrichtung kann nur folgende Strings sein: {ausrichtung_optionen}\n')
        return
    
    beschreibung_optionen = ['standard', 'knapp']
    if not beschreibung in beschreibung_optionen:
        print(f'Eingabefehler: beschreibung = {beschreibung}')
        print(f'beschreibung kann nur folgende Strings sein: {beschreibung_optionen}\n')
        return
    
    
    
    # Vorbearbeitung der Argumente
    if np.shape(werte) == (4,):   
        werte = arr(werte, ndmin = 2).T   # Jeder Wert muss aus Formatierungsgründen eine eigene Liste werden
    
    
    ## Auslese von None-Elementen im Werte-Array
    ### Ersetzung von None-Werten durch Nullen um berechenbar zu bleiben
    test_kein_wert = werte == None   # Bool-Array, wo None-Elemente in werte mit True markiert sind.
    none_stellen   = np.where(test_kein_wert)   # entsprechende Indices
    nullen         = np.zeros(np.shape(werte))
    werte          = arr(np.where(test_kein_wert, nullen, werte), dtype = np.float64)
    
    ### Speichern der Positionen von None-Werten in jew. ex und theo um später dort den Vergleich löschen
    ex_none   = []
    theo_none = []
    for i in range(len(none_stellen[0])):
        if none_stellen[0][i] == 0:
            ex_none.append(none_stellen[1][i])
        if none_stellen[0][i] == 2:
            theo_none.append(none_stellen[1][i])
    alle_none = ex_none + theo_none

    
    ## Wichtige Konstanten
    anzahl_vergleiche = np.shape(werte)[1]
    anzahl_zahlen = 8    # Anzahl Zahlen, die in einem Vergleich vorkommen
    anzahl_vergleichswerte = 5  # Anzahl (fehlerbehafteter) Werte, die in einem Vergleich vorkommen
    
    
    ## Vorbereitung der zu verrechnenden Werte
    werte = werte * faktor   # Umrechnung auf gewünschte Größenordnung bzw. Einheit
    werte[1::2] = np.abs(werte[1::2])      # Keine negativen Fehlerwerte
    ex, ex_fehler, theo, theo_fehler = werte
    

    ## Vorberarbeitung der Größen(-liste)
    größe0 = None   # Wird String im Falle, dass erster Wert von Größen als einheit interpretiert wird.
    if not type(größen) in [str, list]:
        größen = list(größen)
    if len(größen) == 0: # Falls größen leer
        if einheit == '':
            überschriften = []   # Überschriften-Zeile muss nicht geprintet werden
        else:
            fehlende_größen = [''] * anzahl_vergleiche
            überschriften = [*fehlende_größen]
    elif type(größen) == str:
        fehlende_größen = [''] * (anzahl_vergleiche - 1)
        überschriften = [größen, *fehlende_größen]
    elif len(größen) < anzahl_vergleiche:
        fehlende_größen = [''] * (anzahl_vergleiche - len(größen))
        überschriften = [*größen, *fehlende_größen]
    elif len(größen) == anzahl_vergleiche:
        überschriften = größen
    elif len(größen) - 1 == anzahl_vergleiche and einheit == '':
        größe0 = größen.pop(0)
        überschriften = größen
    else:
        if anzahl_vergleiche == 1:
            print((f'Eingabefehler: len(größen) = {len(größen)}, aber es findet nur {anzahl_vergleiche} Vergleich ' 
                    'statt.'))
        else:
            print((f'Eingabefehler: len(größen) = {len(größen)}, aber es finden nur {anzahl_vergleiche} Vergleiche '
                    'statt.'))
        print('Es darf höchstens so viele Größen wie Vergleiche geben.')
        print('(Ausnahme: einheit = \'\' und len(größen) = anzahl_vergleiche + 1,')
        print(' dann wird der erste Wert als einheit interpretiert)\n')
        return
        

        
    # Berechnung und Rundung
    ## Ausrechnen der Abweichungen
    abweichung_abs        = ex - theo
    abweichung_abs_fehler = summen_fehler(arr([theo_fehler, ex_fehler]))
    abweichung_rel        = arr([abweichung_abs[i] / theo[i] * 100  if theo[i] != 0  else 0 
                                 for i in range(anzahl_vergleiche)])   
                                 # [%], div-by-0-crash wird hier verhindert und später mit '-' ersetzt.
    abweichung_sig        = arr([np.abs(abweichung_abs[i] / abweichung_abs_fehler[i])  
                                 if abweichung_abs_fehler[i] != 0  else 0  for i in range(anzahl_vergleiche)])
                                 # hier ebenso
    
    
    ## Bestimmung der Nachkommastellen
    werte_absolut = arr([ex, theo, abweichung_abs])
    werte_fehler  = arr([ex_fehler, theo_fehler, abweichung_abs_fehler])
    werte_relativ = arr([abweichung_rel, abweichung_sig])
    
    ### Berechnung der Anzahl der Nachkommastellen des gerundeten Wertes
    nachkommastellen_fehler  = _nachkommastelle(werte_fehler, sig_grenze = 3.95) 
    '''Cutoff, ab dem nur noch eine signifikante Stelle angezeigt wird, soll eigentlich 4.0 sein, 
    aber aufgerundete Werte sollen auch als '4', nicht '4.0' dargestellet werden.'''
    nachkommastellen_absolut = nachkommastellen_fehler   
                               # Die Rundung der Absolutwerte orientiert sich an der Größe ihrer Fehlerwerte.
    nachkommastellen_relativ = _nachkommastelle(werte_relativ, sig_stellen = 2, sig_grenze = 1.0)  
                               # Hier immer 2 signifikante Stellen.
    
    ### Bildung eines nachkommastellen-Arrays mit shape = (anzahl_zahlen, anzahl_vergleiche)
    nachkommastellen = []
    for i in range(3):
        nachkommastellen.append(nachkommastellen_absolut[i])
        nachkommastellen.append(nachkommastellen_fehler[i])
    nachkommastellen.extend(nachkommastellen_relativ)
    nachkommastellen = np.array(nachkommastellen, dtype = int)
    
    
    ## Rundung aller Werte
    alle_werte          = arr([ex, ex_fehler, theo, theo_fehler, abweichung_abs, abweichung_abs_fehler,
                               abweichung_rel, abweichung_sig])   # shape = (anzahl_zahlen, anzahl_vergleiche)
    alle_werte_gerundet = _rundung(alle_werte, nachkommastellen)   # zahlen-Array
    größenordnungen     = _größenordnung(alle_werte_gerundet)    # int-Array
    
    
    ## Darstellung der einzelnen Werte 
    '''Umwandlung der Zahlen zu String unter berücksichtigung von Rundung und Größenordnung'''
    alle_werte_strings = []
    for i in range(anzahl_zahlen):
        zahlen_strings = []
        for j in range(anzahl_vergleiche):
            if np.abs(größenordnungen[i][j]) < 5:   # Darstellung direkt als gerundete Zahl
                nachkommastelle = _negativ_wird_null(nachkommastellen[i][j])
                wert_string     = '{:.{prec}f}'.format(alle_werte_gerundet[i][j], prec = nachkommastelle)
            else:   # Sehr große oder kleine Werte werden, entsprechend gerundet, in Exponentdarstelung dargestellt.
                größenordnung = größenordnungen[i][j]
                wert_gestutzt = alle_werte_gerundet[i][j] * 10**(-float(größenordnung))
                präzision     = nachkommastellen[i][j] + größenordnung
                wert_string   = '{:.{prec}f}e{}'.format(wert_gestutzt, größenordnung, prec = präzision)
            zahlen_strings.append(wert_string)
        alle_werte_strings.append(zahlen_strings)
    
    ## Löschen des Vergleichs, falls ex- oder theo-Werte None waren, da Vergleich dann sinnlos.
    alle_werte_strings = arr(alle_werte_strings).T  # shape = (anzahl_vergleiche, anzahl_zahlen)
    for i in range(anzahl_vergleiche):
        if i in ex_none:
            alle_werte_strings[i][0:2] = ['', '']
        if i in theo_none:
            alle_werte_strings[i][2:4] = ['', '']
        if i in alle_none:   # alle_none = ex_none or theo_none
            alle_werte_strings[i][4:8] = ['', '', '', '']   
                                         # Fehlt irgendein Wert, werden alle Abweichungs-Werte gelöscht.


                
    # Formatierung der Werte zu schönen, gut lesbaren Vergleichen
    if ausrichtung == 'blöcke':
        alle_vergleiche = []
        '''Wird alle Vergleichswerte als fertig ausgerichtete Strings enthalten, welche einheitliche Länge haben.'''
        for i in range(anzahl_vergleiche):
            strings_einzelwerte = alle_werte_strings[i]

            # Anpassen der Absolutzahlen aneinander
            strings_absolut = list(strings_einzelwerte[[0, 2, 4]])
            strings_absolut = _zahlen_ausrichtung(strings_absolut)

            # Anpassen der Fehlerzahlen aneinander
            strings_fehler = list(strings_einzelwerte[[1, 3, 5]])
            strings_fehler = _zahlen_ausrichtung(strings_fehler)

            # Zusammenstellen des Vergleichs
            plus_minus = _plus_minus(strings_absolut)
            strings_plusminus = [strings_absolut[j] + plus_minus[j] + strings_fehler[j]
                                 for j in range(len(strings_absolut))]
            
            # Darstellen der relativen und sigma-Abweichungen
            string_rel, string_sig = [strings_einzelwerte[6] + ' %', strings_einzelwerte[7] + ' σ']
            
            # Anpassung der Relativwerte bei bestimmten Randfällen
            if string_rel[0] == '-':   # Falls die Zahl negativ ist, soll die sigma-Zahl ein extra ' ' vorne bekommen.
                string_sig = _füllen(string_sig, index = 0)
            if theo[i] == 0:   # Statt div-by-0 oder unsinnigem Wert wird die rel. Abweichung einfach als '-' angegeben.
                string_rel = '-'
            if abweichung_abs_fehler[i] == 0:   # Gleiches gilt für die sigma-Abweichung
                string_sig = '-'
            if i in alle_none:   # Falls ex oder theo fehlt, werden die unsinnigen Abweichungszahlen gelöscht.
                string_rel = ''
                string_sig = ''
            
            # Mittige Ausrichtung aller Strings zu einem Block von gleichmäßiger Breite
            strings_vergleich = [*strings_plusminus, string_rel, string_sig]
            breite_block = max([len(string) for string in strings_vergleich])
            strings_vergleich = [_zentrieren_rechts(string, breite_block) for string in strings_vergleich] 
            
            alle_vergleiche.append(strings_vergleich)
            
    elif ausrichtung == 'liste':
        alle_werte_strings = alle_werte_strings.T   # shape = (anzahl_zahlen, anzahl_vergleiche)
        
        
        # Anpassen und Zusammenfügen von Vergleichszahlen zu Absolutwerten
        zahlen_absolut = [_zahlen_ausrichtung(list(zahlen)) for zahlen in alle_werte_strings[:6]]
        '''Alle Elemente der 8 Vergleichszahlen (Listen von Strings) werden aneinander ausgerichtet, da sie in der
        Tabelle als vertikale Liste dargestellt werden.'''
        plus_minus = [_plus_minus(zahlen_absolut[i]) for i in range(0, len(zahlen_absolut), 2)]   # range = [0, 2, 4]
        strings_absolut = [[zahlen_absolut[i][j] + plus_minus[i//2][j] + zahlen_absolut[i + 1][j] 
                            for j in range(anzahl_vergleiche)] for i in range(0, len(zahlen_absolut), 2)]
        
        
        # Anpassung der Relativwerte bei bestimmten Randfällen
        '''Analog zu wie Randfälle im 'blöcke'-Abschnitt behandelt werden.'''
        strings_rel = [alle_werte_strings[6][i]  + ' %'  if theo[i] != 0  else '-' for i in range(anzahl_vergleiche)]
        strings_sig = [alle_werte_strings[7][i] + ' σ'  if abweichung_abs_fehler[i] != 0  else '-'  
                       for i in range(anzahl_vergleiche)]
        strings_rel = ['' if i in alle_none else strings_rel[i] for i in range(anzahl_vergleiche)]
        strings_sig = ['' if i in alle_none else strings_sig[i] for i in range(anzahl_vergleiche)]
        strings_rel = _zahlen_ausrichtung(strings_rel)
        strings_sig = _zahlen_ausrichtung(strings_sig)
        
        alle_vergleiche = [*strings_absolut, strings_rel, strings_sig]   # "shape" = (anzahl_zahlen, anzahl_vergleiche)
        
    
    
    # Erstellen der fertigen Tabellenstrings
    titel_strings = [titel, '']  if titel != ''  else  []   # Hinzufügen des Titels der Tabelle falls vorhanden
    
    
    if ausrichtung == 'blöcke':
        separator = '   '   # Was die Blöcke (Spalten) der Tabelle trennt.
        
        # Angleichen der Länge der Größenstrings (Blocküberschriften) mit der Breite der dazugehörigen Vergleichsblöcke
        if überschriften != []:
            breite_blöcke   = [max(len(alle_vergleiche[i][0]), len(überschriften[i])) for i in range(anzahl_vergleiche)]
            überschriften   = ['{:^{width}}'.format(überschriften[i], width = breite_blöcke[i]) 
                               for i in range(anzahl_vergleiche)]   
                              # Überschriften werden links-zentriert auf die Blöcke.
            alle_vergleiche = [['{:^{width}}'.format(vergleichswert, width = breite_blöcke[i]) 
                                for vergleichswert in alle_vergleiche[i]] for i in range(anzahl_vergleiche)] 
                              # Ebenso die Blöcke, falls diese schmaler als die Überschriften sind.
            
        # Erstellen vom "Einheiten und Beschreibungen"-Block (Vorspalte)
        if beschreibung == 'standard':
            beschreibung_liste = ['Wert       experimentell', '           theoretisch  ', 'Abweichung absolut      ', 
                                  '           relativ      ', '           sigma        ']
            if einheit != '':
                einheit_string = f'Einheit    {einheit}'
                überschuss     = len(einheit) - len('experimentell')
                stelle         = 'rechts'   # Angabe, dass einheit_string später links ausgerichtet werden soll, 
                                            # 'rechts' werden Leerzeichen eingefügt.
                
        elif beschreibung == 'knapp':
            beschreibung_liste = ['Wert exp', '     the', 'Abw. abs', '     rel', '     sig']
            if einheit != '':
                einheit_string = f'[{einheit}]'
                überschuss     = len(einheit_string) - len(beschreibung_liste[0])
                stelle         = 'links'   # links vom einheit_string werden später Leerzeichen eingefügt.
            
        ## Ausrichtung der Vorspalte
        if größe0 != None:  # Randfall: erster größen-String ersetzt einheit.
            einheit_string = größe0
            überschuss     = len(einheit_string) - len(beschreibung_liste[0])
            stelle         = 'rechts'
            
        if einheit == '' and größe0 == None:   # Fall: keine einheit angegeben
            einheit_string = ' ' * len(beschreibung_liste[0])
        elif überschuss < 0:   # = falls einheit_string schmaler als Beschreibungsstrings
            einheit_string = _füllen(einheit_string, stelle, menge = -überschuss)
        elif überschuss > 0:   # = falls einheit_string breiter als Beschreibungsstrings
            beschreibung_liste = [_füllen(string, index = stelle, menge = überschuss) for string in beschreibung_liste]

        
        # Erstellen und Sammeln aller Überschriften-Strings
        if überschriften != []:
            überschriften.insert(0, einheit_string)
            überschriften_string = separator.join(überschriften)   
            titel_strings.append(überschriften_string)
            
        ## Erstellen der Linie, die Überschriften und Vergleiche trennt
        alle_vergleiche = _listen_transponieren(alle_vergleiche)   # "shape" = (anzahl_vergleiche, anzahl_zahlen) 
        blöcke_längen   = [len(vergleich) for vergleich in alle_vergleiche[0]]
        blöcke_längen.insert(0, len(einheit_string))
        oberlinie       = separator.join(['-' * länge for länge in blöcke_längen])   
            # Die gestrichelte Oberlinie ist durch separator-Strings unterbrochen, d.h. jeder Block hat seine Linie.
        titel_strings.append(oberlinie)
        
        # Erstellen aller Vergleich-Strings (alles unter der Oberlinie)
        vergleich_strings = []
        for i in range(anzahl_vergleichswerte):
            vergleich_string = separator.join([beschreibung_liste[i], *alle_vergleiche[i]])
            vergleich_strings.append(vergleich_string)
    
    
    if ausrichtung == 'liste':
        separator = ' | '   # Was die Spalten der Tabelle voneinander trennt.
        
        if beschreibung == 'standard':
            beschreibung_liste = [['Wert', 'Abweichung'], 
                                  ['experimentell', 'theoretisch', 'absolut', 'relativ', 'sigma']]
            
        elif beschreibung == 'knapp':
            beschreibung_liste = [['Wert', 'Abw.'], ['exp', 'the', 'abs', 'rel', 'sig']]
            if einheit != '':
                einheit = f'[{einheit}]'
        
        # Angleichen der Breite der Beschreibungen mit denen der Vergleichswertspalten
        for i in range(anzahl_vergleichswerte):
            differenz = len(beschreibung_liste[1][i]) - len(alle_vergleiche[i][0])
            if differenz < 0:   # = vergleich ist breiter als beschreibung -> Beschreibungen werden "links-zentriert".
                beschreibung_liste[1][i] = '{:^{width}}'.format(beschreibung_liste[1][i], 
                                                                width = len(alle_vergleiche[i][0]))
            elif differenz > 0:    # = vergleich ist schmaler als beschreibung -> Vergleichsstrings werden rechtsbündig 
                                   #   ausgerichtet.
                alle_vergleiche[i] = [_füllen(string, 'links', menge = differenz) for string in alle_vergleiche[i]]
       
        ## 'Wert' wird zentriert auf die ex- und theo-Spalten. 
        beschreibung_liste[0][0] = '{:^{width}}'.format(beschreibung_liste[0][0],   
                                                        width = len(separator.join(beschreibung_liste[1][:2])))
        ## 'Abweichung' bzw. 'Abw.' wird zentriert auf die abs-, rel- und sig-Spalten
        beschreibung_liste[0][1] = '{:^{width}}'.format(beschreibung_liste[0][1], 
                                                        width = len(separator.join(beschreibung_liste[1][2:])))
        
        ## Vorbereiten und Ausrichten der Vorspalte
        if überschriften != []:  # Wenn falsch, bedeutet auch, dass einheit == '' ist.
            if einheit == '' or beschreibung == 'knapp':
                überschriften.insert(0, '')   # Leere erste Zelle
            elif beschreibung == 'standard':   # Wenn einheit vorhanden und "Platz für ausführlichere Beschreibung"
                überschriften.insert(0, 'Einheit')
            if größe0 == None:
                überschriften.insert(1, einheit)   # einsetzen vom Einheit-String
            else:
                überschriften.insert(1, größe0)   # einsetzen der ersten Überschrift statt Einheit
            
            # Bestimmung und Vereinheitlichung der Breite der Vorspalte
            überschrift_längen = [len(string) for string in überschriften]
            überschriften_breite = max(überschrift_längen)
            for i in range(2):   # Bearbeitung der ersten zwei Kopfzeilen 
                einheit_string = '{:^{width}}'.format(überschriften.pop(0), width = überschriften_breite)
                beschreibung_liste[i].insert(0, einheit_string)
            überschriften = ['{:<{width}}'.format(string, width = überschriften_breite) for string in überschriften]
                # Die einzelnen Überschriften (größen) werden linksbündig ausgerichtet
            
        
        # Erstellen und Sammeln aller Überschriften-Strings
        for i in range(2):  # Erstellen und einfügen der beiden Kopfzeilen-Strings
            beschreibung_string = separator.join(beschreibung_liste[i])
            titel_strings.append(beschreibung_string)
        oberlinie = '-' * len(beschreibung_string)
        titel_strings.append(oberlinie)
        
        # Erstellen aller Vergleich-Strings (alles unter der Oberlinie)
        alle_vergleiche   = _listen_transponieren(alle_vergleiche)   # "shape" = (anzahl_vergleiche, anzahl_zahlen)
        if überschriften != []:   # Einfügen der Vorspalte falls vorhanden
            vergleich_liste = [[überschriften[i], *alle_vergleiche[i]] for i in range(anzahl_vergleiche)]
        else:
            vergleich_liste = alle_vergleiche
        vergleich_strings = [separator.join(vergleich) for vergleich in vergleich_liste]
    
    
    
    # Printen der Tabelle
    alle_strings = [*titel_strings, *vergleich_strings]
    for zeile in alle_strings:
        print(zeile)  
    print('')   # Separieren von nachfolgenden Prints.
        


        
        
        
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
        funktion(x, *parameter)  also bspw. pap.func.quad(x, a, b, c)
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
    >>> parameter, parameter_fehler = pap.odr_fit(pap.func.prop, messpunkte, messfehler, 
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
    >>> output = pap.odr_fit(pap.func.poly, messpunkte, messfehler, parameter_schätz, 
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
        sind, dies sieht man besser mit einem Plot.
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
    fit_werte : np.array (1D, number_like)
        die Werte, die die Fitfunktion ausgibt, also  fit_werte = fit_func(x_werte, *parameter)
    
    werte : np.array (1D, number_like)
        y-Werte der Messdaten
    
    werte_fehler : np.array (1D, number_like)
        y-Fehler der Messdaten
    
    anzahl_parameter : int (> 0)
        Anzahl Parameter der Fitfunktion
        
        
    Beispiel
    --------
    >>> x_werte = np.array([-8, -5.5, -1.2, 1, 1.4, 3.2, 4.5])
    >>> y_werte = np.array([40, 20.8, 3.1, 0.5, 1.5, 3, 6])
    >>> y_fehler = np.array([0.5, 0.73, 0.42, 0.23, 0.23, 0.41, 0.44])
    >>> fitparameter = [0.46721214, -1.01681483, 1.45102103]
    >>> pap.chi_quadrat_test(pap.func.quad(x_werte, *fitparameter), y_werte, y_fehler, 3)
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
    >>> pap.chi_quadrat_odr(*chi_test_liste)
      Ergebnisse des χ^2-Tests:
      
      χ^2_reduziert         = 0.82
      Fitwahrscheinlichkeit = 44.0%
    '''
    
    
    _chi_quadrat_print(chi_quadrat, anzahl_messwerte, anzahl_parameter)
   

# Projekt `vergleichstabelle()`
## Ziel
Erstellen einer Funktion, die einen automatisierten Vergleich von theoretischen mit experimentellen Werten durchführen soll und diesen dann möglichst schön und leserlich und aussagekräftig in einer geprinteten Tabelle darstellt.

## Features und Aussehen
Die Funktion ist nun fürs erste fertig entwickelt (Stand 2020-10-27). Eine Übersicht über was diese Funktion macht und wie die Vergleichstabellen aussehen bietet der aktuelle Docstring von pap.vergleichstabelle(); siehe vor allem "Beispiele":


    vergleichstabelle(werte, titel = '', einheit = '', größen = '', faktor = 1, ausrichtung = 'blöcke', 
                      beschreibung = 'standard'):
    '''
    Printet einen wissenschaftlichen Vergleich von fehlerbehafteten experimentellen und theoretischen Werten in 
    Tabellenform. 
    Berechnet und angezeigt werden zusätzlich absolute und relative sowie sigma-Abweichungen.
    Die Werte sind zur besseren Vergleichbarkeit in ±-Darstellung, nach Komma und Exponent ausgerichten als auch 
    gerundet entsprechend der Größe ihrer Fehler (siehe "Berechnung und Rundung")
    
    Die Vergleiche können sowohl nebeneinander als 'blöcke' dargestellt werden als auch untereinander als 'liste'.
    Einheit sowie Überschriften der einzeln Vergleiche (größen) können auch angegeben werden.
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
        Ein Fehler-Wert, der None ist, wird als 0 interpretiert. Ein ex-/theo-Wert der None ist, wird als fehlende Zahl 
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
                                  bekommen die letzten Vergleiche keine Überschrift
        * Liste von Länge N + 1 - nur möglich, wenn einheit nicht angegeben. Erster String der Liste 
                                  ersetzt einheit und die Kennzeichnung 'Einheit' bzw. '[...]'. Die 
                                  restlichen Strings sind die jeweiligen Vergleichsüberschriften.
    
    faktor : number_like, optional
        wird multipliziert mit allen Werten. Falls die angegebene Einheit (oder Größenordnung), nicht die ist in der 
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
    * Beim Runden von vielen Zahlen reduziert dies den statistischen Fehler, der durchs Runden entsteht.
    
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

# pap-Paket

**Übersicht:**
* Was wird in diesem Projekt gemacht?
* Übersicht der Features und Funktionen
* [Installieren des Pakets](https://github.com/Fjallripa/pap#installieren-des-pakets)



## Was wird in diesem Projekt gemacht?
Hier wird ein Python-Paket `pap` entwickelt, das repetitive Aufgaben der Physikexperiment-Auswertungen im Studium schneller, einfacher und schöner löst als es manuell möglich wäre.
Im Zuge der Entwicklung wird das Paket um neue Funktionen ergänzt und alte Funktionen flexibler/kraftvoller gemacht.  
Ideen, Feedback und Beiträge sind höchst willkommen.



## Übersicht der Features und Funktionen  

Aktuell lassen sich die Features in 5 Bereiche aufteilen:  
* Fehlerrechnung
* Einfache Statistik
* Resultat-Darstellung und -Vergleich
* Fits und Chi^2-Tests
* Grundlegende Fitfunktionen


### Übersicht der Bereiche
#### Fehlerrechnung:
* [`pap.summen_fehler()`](https://github.com/Fjallripa/pap/wiki/summen_fehler()) und [`pap.produkt_fehler()`](https://github.com/Fjallripa/pap/wiki/produkt_fehler())
    vereinfachen einem die gauß'sche Fehlerfortpflanzung.  
    Zur Berechnung muss man nur die benötigten Werte und Fehler einsetzen.
        

#### Einfache Statistik:
* [`pap.std()`](https://github.com/Fjallripa/pap/wiki/std())
    berechnet den Experimentellen Fehler des Einzelwertes.  
    `np.std()` tut dies nämlich nicht, näheres dazu auf der `pap.std()`-Seite
* [`pap.mittel()`](https://github.com/Fjallripa/pap/wiki/mittel())  und  [`pap.mittel_fehler()`](https://github.com/Fjallripa/pap/wiki/mittel_fehler())
    entsprechen jeweils `np.mean()` und dem Experimentellen Fehler des Mittelwertes
* [`pap.fwhm()`](https://github.com/Fjallripa/pap/wiki/fwhm())
    wandelt σ in FWHM bzw. Halbwertsbreite um


#### Resultat-Darstellung und Vergleich:
* [`pap.resultat()`](https://github.com/Fjallripa/pap/wiki/resultat())
    printet ein schön formatiertes Ergebnis mit 
    Titel, definierter Präzision, evt. +/- Fehler, Einheit und evt. relativen Fehler.
    
    Beispiel:
    ```python
    >>> pap.resultat('Arbeit', np.array([3.3520e6, 0.4684e6]), 'MJ', faktor = 1e-6)
    ```
    ```
    Arbeit: 3.4 +/- 0.5 MJ
    ```
    
* [`pap.vergleichstabelle()`](https://github.com/Fjallripa/pap/wiki/vergleichstabelle())
    printet einen wissenschaftlichen Vergleich von fehlerbehafteten experimentellen und 
    theoretischen Werten in Tabellenform. 
     - Absolute, relative und sigma-Abweichung werden berechnet.
     - Die Werte sind nach Größenordnung ausgerichtet und wissenschaftlich gerundet.
     - Darstellung der Vergleiche als Blöcke oder als Liste möglich.
     - Robust gegen Extremfälle und fehlende Werte.
    
    Beispiel:
    ```python
    >>> titel  = 'Literaturvergleich Fallbeschleunigung'
    >>> werte  = np.array([[3.446, 0.00204], [0.105, 0.00045], [3.69, 0], [5e-3, 0]])
    >>> größen = ['Boden', 'Orbit']
    >>> vergleichstabelle(werte, titel, einheit = 'm/s^2', größen = größen, 
                          beschreibung = 'knapp')
    ```
    ```
    Literaturvergleich Fallbeschleunigung

     [m/s^2]       Boden             Orbit     
    --------   --------------   ---------------
    Wert exp    3.45  ± 0.10    0.0020 ± 0.0004
         the    3.690 ± 0.005   0.0    ± 0.0   
    Abw. abs   -0.24  ± 0.11    0.0020 ± 0.0004
         rel       -6.6 %              -       
         sig        2.3 σ            4.5 σ      
    ```


#### Fits und Chi^2-Tests:
* [`pap.odr_fit()`](https://github.com/Fjallripa/pap/wiki/odr_fit())
    fittet Funktionen ähnlich wie SciPys `curve_fit()` nur mit Berücksichtigung des x-Fehlers, 
    was wichtig wird, wenn dieser der dominante Fehler ist. 
    Diese Funktion benutzt direkt SciPys `odr`-Paket, ist aber wesentlich einfacher 
    zu bedienen.

* [`pap.chi_quadrat_test()`](https://github.com/Fjallripa/pap/wiki/chi_quadrat_test()) und  [`pap.chi_quadrat_odr()`](https://github.com/Fjallripa/pap/wiki/chi_quadrat_odr())
    führen einen χ^2-Test zu Bestimmung der Güte des Fits durch.
    Erstere nimmt die Ergebnisse von SciPys `curve_fit()` auf, während zweitere die von 
    `pap.odr_fit()` benutzt und damit auch den x-Fehler berücksichtigt.

    Beispiel: (für Orignal-Werte, siehe die `pap.chi_quadrat_test()`-Seite)
    ```python
    >>> pap.chi_quadrat_test(pap.func.quad(x_werte, *fitparameter), y_werte, y_fehler, 3)
    ```
    ```
    Ergebnisse des χ^2-Tests:

    χ^2_reduziert         = 2.79
    Fitwahrscheinlichkeit = 2.5%
    ```
 

#### Grundlegende Fitfunktionen:
(mehr Infos in der [Modulübersicht](https://github.com/Fjallripa/pap/wiki/Modul-pap.func) von `pap.func`)
* [`pap.func.konst()`](https://github.com/Fjallripa/pap/wiki/func.konst())   - Konstante Funktion
* [`pap.func.prop() `](https://github.com/Fjallripa/pap/wiki/func.prop())   - Proportionale Funktion
* [`pap.func.lin()  `](https://github.com/Fjallripa/pap/wiki/func.lin()) ` `- Lineare Funktion
* [`pap.func.quad() `](https://github.com/Fjallripa/pap/wiki/func.quad())   - Quadratische Funktion
* [`pap.func.poly() `](https://github.com/Fjallripa/pap/wiki/func.poly())   - allgemeines Polynom
* [`pap.func.exp()  `](https://github.com/Fjallripa/pap/wiki/func.exp()) ` `- Exponentialfunktion
* [`pap.func.gauss()`](https://github.com/Fjallripa/pap/wiki/func.gauss())   - Gaußverteilung



## [Installieren des Pakets](https://github.com/Fjallripa/pap/wiki/Installationsanleitung)
Dieses Paket ist noch kein allgemeinzugängliches Python-Paket, deshalb muss es manuell von GitHub (https://github.com/Fjallripa/pap) heruntergeladen werden (nur der Ordner `pap` ist notwendig).  

Wenn du es direkt benutzen willst, kannst du es in den gleichen Ordner wie dein Jupyter-Notebook bzw. Python-Skript speichern.  
Wenn du aber nicht für jede neue Datei den `pap`-Ordner dorthin kopieren willst, damit `import pap` klappt, dann gibt es für Jupyter-Notebook-Benutzer eine detaillierte Anleitung unter [Installationsanleitung](https://github.com/Fjallripa/pap/wiki/Installationsanleitung). Skript-Benutzer (`.py`) können ihren Dateipfad für `pap` PYTHONPATH hinzufügen (wie, kann leicht gegoogelt werden).

Danach sollte `pap` problemlos zu benutzen sein:
```python
import pap

# Infos zum Paket/Modul. Gibt eine Übersicht der Funktionen. Auch alle deren Docstrings sind aufgelistet.
help(pap)
help(pap.func)

# Aufrufen der pap-Funktionen
pap.blabla(...)
pap.func.blablubb(...)
```

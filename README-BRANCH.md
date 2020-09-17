# Fits und Chi-Tests
Hier werden mehrere Funktionen entwickelt, die zum Einen ermöglichen sollen Messdaten mit signifikanten x-Fehlern an Funktionen zu fitten (`odr_fit()`) und zum Anderen einen χ^2-Test zum Beurteilen der Güte dieses Fits ausführen sollen (`chi_quadrat_odr()`). Zusätzlich wird noch die alte Funktion des normalen χ^2-Tests (`chi_quadrat_test()`) angepasst, da beide Funktionen nun viel Code teilen. `_chi_quadrat_print()` wird von beiden Funktionen aufgerufen.

## `odr_fit`
fittet 1D-Funktionen an Messdaten mit Fehlern in der x-Achse. Sie bedient sich direkt dem scipy.odr Paket und vereinfacht nur die Bedienung auf Kosten von Optionen.
Auf Wunsch können Fit-Resultate angezeigt und weitergegeben werden. Das Gleiche gilt auch für einen χ^2-Test.

## `chi_quadrat_odr`
Wenn nicht schon von `odr_fit` aufgerufen, dann lässt sich mit dessen Daten der Test separat ausführen. Hierbei wird nur `_chi_quadrat_print` aufgerufen.

## `chi_quadrat_test`
Aus Fitfunktion und Messwerten (ohne x-Fehler) wird χ^2 berechnet und mithilfe von `_chi_quadrat_print die Resultate angezeigt.

## `_chi_quadrat_print`
Nimmt den χ^2-Wert auf und berechnet den reduzierten χ^2-Wert sowie die Fitwahrscheinlichkeit und präsentiert diese.

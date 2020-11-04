## Rundung

### Rundung nach DIN1333 anpassen
* Wie wichtig/vorteilhaft wäre die Umstellung?
* vA. bei vergleichstabelle()
    * Auch bei anderen?
* Signifikanz-Niveau von "4.0" auf "3.0" ändern.
    * Wie sind genau die Regeln?
    
### Nachkommastellen-Berechnung verbessern
* `_nachkommastellen()` bzw. `_erste_ziffer()` verbessern, sodass "4.0"-Randfall nicht mehr vorkommt (siehe Tests von vergleichstabelle()).
* Idee: Zahlen zu Strings umwandeln und erstes Zeichen angucken.
* Übrigens: Unter `## Darstellung der einzelnen Werte` bei vergleichstabelle() kann `wert_gestutzt` in ähnlich angepasster Weise berechnet werden.


## Verbesserungen von `resultat()`
* Automatisches wissenschaftliches Runden wie bei vergleichstabelle()
    * Wie sollen fehlerlose Fälle behandelt werden?


## Verbesserungen von `vergleichstabelle()`
* Abwählbare Abweichungen
* ex- und theo-Werte umbenennen können (siehe Tests)
* Theo-Wert-Rundung anpassen (siehe Tests)
    * `'auto'`  - normal
    * `'exakt'` - so genau wie Eingangswert
    * `'exp'`   - wie ex-Wert gerundet
    * `int`     - Präzision (Anzahl signifikante Stellen)  angeben
    * Motivation: Ist der theo-Wert eine exakte Konstante mit 0 Fehler, dann wird er nach aktuellen Regeln auf nur eine Nachkommastelle gerundet.
* Optional? (Motivation zweifelhaft)
    * `einheit` auch als Liste möglich
        * `einheit` dann Teil von den  Überschriften-Strings: `'Größe [E]'`
    * `faktor` auch als Liste möglich

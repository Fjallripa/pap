# Installationsanleitung

Dieses Paket ist noch kein allgemeinzugängliches Python-Paket, deshalb muss es manuell von GitHub (https://github.com/Fjallripa/pap) heruntergeladen werden (nur der Unterordner `pap` ist notwendig).  



## Sofort benutzen
Wenn du es direkt benutzen willst, kannst du den `pap`-Unterordner in den gleichen Ordner wie dein Jupyter-Notebook bzw. Python-Skript speichern.  

#### Nachteil:  
Schreibt man ein eigenes Paket mit Python-Funktionen wie hier `pap`, dann muss man es normalerweise im gleichen Ordner wie das Jupyter-Notebook haben, damit `import pap` klappt.  



## Benutzen mit `pap`-Ordner an nur einem Ort
Will man aber nicht neben jedem Notebook Kopien des Pakets rumfliegen haben, sondern nur an einer Stelle (zB. im Ordner `/HOME/Ordner-über-dem-pap-Ordner`), dann kann man ins Notebook folgenden Code schreiben (mit gewünschtem Dateipfad): 
```
import sys
sys.path.append('HOME/Ordner-über-dem-pap-Ordner')
``` 
Er sorgt dafür, dass Jupyter auch im gewünschten Dateipfad nach Python-Paketen sucht. 

#### Nachteil:
Der Code muss bei jedem Notebook dabei sein, wo man das Modul importieren will und der Dateipfad kann bei jedem Rechner anders aussehen. Nervig wenn man sowohl auf dem jupyter.kip-Server als auch auf seinem eigenen Rechner das Notebook benutzt.



## Beste Lösung
## für `.py`-Skripte

Schreibt man Python-Skripte, kann man den gewünschten Dateipfad zu "`PYTHONPATH`" hinzufügen, das ist dem Jupyter-Notebook aber egal.
Wie das geht, wird auf dieser [Blog-Seite](https://izziswift.com/permanently-add-a-directory-to-pythonpath/) beschrieben, für Linux/Mac sowie für Windows.


## für Jupyter-Notebooks
Der hier präsentierte Weg sorgt dafür, dass Jupyter auch standardmäßig im gewünschten Dateipfad nach Paketen guckt.


### Vorgehensweise
1. 
Erstelle eine `own_pythonpath.py` Textdatei (Name egal) mit folgendem Code drin:  
```
import sys
sys.path.append('HOME/Ordner-über-dem-pap-Ordner')
```  
Ändere den Dateipfad im Code zu welchem Ordner auch immer du das Paket gespeichert hast und beachte, dass Windows für Dateipfade `\` statt `/`benutzt. Setze für `HOME` den entsprechenden Dateipfad deines Betriebssystems ein (siehe "Home-Verzeichnis" unten).

2. 
Bewege die Datei in den Ordner `HOME/.ipython/profile_default/startup`. Möglicherweise musst du dafür dein Dateienprogramm dazu bringen versteckte Ordner und Dateien anzuzeigen (einfach nachgoogeln wie). 
Falls du dies im jupyter.kip-Server tun willst, bewege die Datei mit "Move" und kopiere die Adresse `/.ipython/profile_default/startup` in die Zeile vom "Move"-Fenster.

3. Jetzt Jupyter-Notebook neustarten und `import pap` ausführen.


### Erklärung
In Schritt 1 wird ein Mini-Programm erstellt, das dafür sorgt, dass Python-Pakete (hier unser pap) in Jupyter-Notebooks auch von einem selbst gewählten Ordner aus importiert werden können.  
In Schritt 2 wird dieses Programm in einen Ordner bewegt, wo Jupyter .py-Dateien immer zuerst ausführt wenn ein Notebook gestartet wird. Dadurch funktionert unser Programm erst.


### Home-Verzeichnis
Ersetze Wörter in Großbuchstaben ersetzen mit eigenen.  
Das `/` (bzw. `C:\`) am Anfang muss dabei sein.

| Betriebssystem     | Dateipfad               |
| ------------------ | ----------------------- |
| Windows            | `C:\Users\USERNAME`     |
| Linux              | `/home/USERNAME`        |
| Mac                | `/Users/USERNAME`       |
| jupyter.kip-Server | `/home/ad/UNI-ID/linux` |

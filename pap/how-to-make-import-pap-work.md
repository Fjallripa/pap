# pap-Paket ohne Probleme in Jupyter-Notebook importieren


## Motivation
Schreibt man ein eigenes Paket mit Python-Funktionen wie hier `pap`, dann muss man es normalerweise im gleichen Ordner wie das Jupyter-Notebook haben, damit `import pap` klappt.  
Will man aber nicht neben jedem Notebook Kopien des Pakets rumfliegen haben, sondern nur an einer Stelle (zB. im Ordner `/HOME/experiment-code`), dann kann man ins Notebook folgenden Code schreiben (mit gewünschtem Dateipfad): `import sys; sys.path.append('HOME/experiment-code')`. Er sorgt dafür, dass Jupyter auch im gewünschten Dateipfad nach Python-Paketen sucht. Das Problem ist, dass der Code bei jedem Notebook dabei sein muss, wo man das Modul importieren will und der Dateipfad bei jedem Rechner anders aussehen kann. Nervig wenn man sowohl auf dem jupyter.kip-Server als auch auf seinem eigenen Rechner das Notebook benutzt.  
Schreibt man Python in der Kommandozeile, kann man den gewünschten Dateipfad zu "PYTHONPATH" hinzufügen, das ist dem Jupyter-Notebook aber egal.  

Der hier präsentierte Weg sorgt dafür, dass Jupyter auch standardmäßig im gewünschten Dateipfad nach Paketen guckt.


## Vorgehensweise
1. Erstelle eine `own_pythonpath.py` Textdatei (Name egal) mit folgendem Code drin:  
`import sys`  
` `  
`sys.path.append('HOME/experiment-code')`  
Ändere den Dateipfad im Code zu welchem Ordner auch immer du das Paket gespeichert hast und beachte, dass Windows für Dateipfade `\` statt `/`benutzt. Setze für `HOME` den entsprechenden Dateipfad deines Betriebssystems ein (siehe "Home-Verzeichnis" unten).
2. Bewege die Date in den Ordner `HOME/.ipython/profile_default/startup`. Möglicherweise musst du dafür dein Dateienprogramm dazu bringen versteckte Ordner und Dateien anzuzeigen (einfach nachgoogeln wie).


## Erklärung
In Schritt 1 wird ein Mini-Programm erstellt, das dafür sorgt, dass Python-Pakete (hier unser pap) in Jupyter-Notebooks auch von einem selbst gewählten Ordner aus importiert werden können.  
In Schritt 2 wird dieses Programm in einen Ordner bewegt, wo Jupyter .py-Dateien immer zuerst ausführt wenn ein Notebook gestartet wird. Dadurch funktionert unser Programm erst.


## Home-Verzeichnis
Ersetze Wörter in Großbuchstaben ersetzen mit eigenen.  
Das `/` (bzw. `C:\`) am Anfang muss dabei sein.

| Betriebssystem     | Dateipfad               |
| ------------------ | ----------------------- |
| Windows            | `C:\Users\USERNAME`     |
| Linux              | `/home/USERNAME`        |
| Mac                | `/Users/USERNAME`       |
| jupyter.kip-Server | `/home/ad/UNI-ID/linux` |
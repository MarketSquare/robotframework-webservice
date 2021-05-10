# Robot Task Webservice

Ein Webservice zum Starten von Robot Framework Tasks über einen Webservice.


## Idee

Der Webservice soll ermöglichen, Robot Framework Tasks zu starten, indem
man per Browser die URL des Services aufruft und als Teil der Route den Namen
des Tasks und ggf. die Variablen für den Task angeben kann.

Beispiel:

    http://localhost:5003/run/MeinNuetzlicherTask

Beispiel mit Variablen:

    http://localhost:5003/run/MeinNuetzlicherTask?MeineVariable=42&NochEineVariable=Mustermann

Als Antwort bekommt man den Status angezeigt und die Log-Datei.


## Entwicklungsstatus

Status: Noch in der Prototypphase


### Webservice starten

Beispiel, um den Service auf Port 5003 zu starten:

    
    uvicorn app.main:app --port 5003

Geht auch mit anderen WSGI-Webservern, z.B. Waitress:

    waitress-serve --port 5003 app.main:app


### Demo-Tasks

Aktuell sind ein paar Demo-Tasks hinterlegt, die aufgerufen werden können.
Die Robot-Dateien dazu liegen im Unterordner ``tasks``.
Hier können auch weitere Robot-Dateien mit Tasks abgelegt werden, um
sie dann über den Webservice zu starten.


### Task-Name in der URL

In der URL sind keine Leerzeichen erlaubt, aber Robot Framework unterstützt
auch CamelCase- und snake_case-Schreibweise. D.h. ein Task namens "Noch ein Task"
wird von Robot auch gefunden, wenn man den Namen als "NochEinTask" oder
"noch_ein_task" angibt.


### Variablen

Variablen können mit der URL-Parameter-Schreibweise übergeben werden.

Beispiel:

    http://localhost:5003/TaskMitMehrerenVariablen?vorname=Max&nachname=Mustermann


### Robot Log.html, output.xml und report.hmtl

Im Moment werden diese drei Dateien von jedem Robot-Task im Verzeichnis /robotlog angelegt.
Jeder Task legt im /robotlog sein eigenes Verzeichniss mit den drei Datein an. Diese werden 
bei jedem neuen lauf des Task überschrieben.
Sie können per Browser abgerufen werden über die Route ``\robotlog\``.

Beispiele:

    http://localhost:5003/robotlog/log.html
    http://localhost:5003/robotlog/output.xml
    http://localhost:5003/robotlog/report.html

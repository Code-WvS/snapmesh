Snapmesh
========

Deutsch
-------
Einfacher Python-Server, der Daten empfängt, speichert und sendet. Snap!-Blöcke inbegriffen.
Snapmesh ist abhängig von Python2 und dem Modul snapext. `snapmesh_plain.py` ist ein Python2-Server ohne die snapext-Abhängigkeit (jedoch nicht auf dem neuesten Stand).
Zur Ausführung werden Rootrechte benötigt, alternativ kann der Port (Standard 80) geändert werden.
Unter Windows sollte zudem die snapext durch `snapext.py` ersetzt werden.

Folgende Befehle sind via HTTP verfügbar:
  * `/`: Testen des Onlinestatus
  * `/check?key=foo` gibt zurück, ob `foo` gespeichert ist
  * `/get?key=foo` gibt den als `foo` gespeicherten Wert
  * `/put?key=foo&value=bar` speichert `bar` in `foo`
  * `/list` listet alle vorhandenen Keys
  * `/bye` beendet den Server

English
-------

Dead-simple python server that receives, stores and sends data. Snap! blocks included.
Snapmesh depends on Python2 and the python module snapext. `snapmesh_plain.py` ist a Python2 server without the snapext dependency (not up to date, though).
To run you need root or you could also change the port (default 80).
On Windows replace snapext by `snapext.py`.

There are the following commands available through HTTP:
  * `/`: test if online
  * `/check?key=foo` tests wheather `foo` is saved
  * `/get?key=foo` returns the value saved for `foo`
  * `/put?key=foo&value=bar` saves `bar` to `foo`
  * `/list` lists all keys
  * `/bye` shuts the server down

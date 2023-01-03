#electricitymeter
Graphic Electricity Meter Viewer with Raspberry Pico W

##Task of the software
Graphical representation of energy consumption by evaluating the flashing pulses on a modern electronic electricity meter. The evaluation at a Ferraris meter is not possible. 
Functionality
The flashing pulses are detected at the electricity meter via a photoresistor and processed with a Raspberry Pico W. The photoresistor is simply taped to the meter. The photoresistor is simply taped in front of the flashing LED of the meter. If necessary, the area of the photoresistor should be darkened with a cover (cardboard). It is possible to connect the photoresistor to the pico with a maximum 1m long two-wire cable. 
Display
When calling the IP address of the Raspberry Pico W, a small web page is displayed. On this there are 4 links to evaluations of the energy consumption of the last 2 hours, the last day, the last 31 days and the last 2 years. In each of the graphs the average of the evaluation period is also shown.
Special functions
After every full hour a backup file is created. In the "backup.py" all information is contained. It can be edited manually with an editor. When the software is started, the contents of the "backup.py" are loaded automatically. The software obtains the time by calling the NTP function. Links can be used to set the system time to summer and winter time. There is also the possibility to create an immediate backup without waiting for the next hour change. A special backup "sbackup.py" can also be created. The backup file "sbackup.py" is not created or read automatically. It is only used for a manual service case, when the normal "backup.py" cannot be used anymore.
##Application
1. load Raspberry Pico W with the current Micropython firmware UF2 file ( https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2 )
2. download APP Thonny ( https://thonny.org )
3. edit lines 13-15 of "main.py" (enter your own WLAN access data and number of pulses per 1 KWh from your electricity meter)
4. connect Raspberry Pico W with the photoresistor diode ( pin 17 and pin18 )
5. fix the photoresistor in front of the flashing LED of the electricity meter (adhesive tape)
6. transfer the file main.py to the Raspberry Pico W using Thonny
7. Open the Raspberry Pico W in any browser via the IP address.
##here you can read more
https://icplan.de/seite41/

##Aufgabe der Software
Graphische Darstellung des Energieverbrauchs durch Auswertung der Blinkimpulse an einem modernen elektronischen Stromzähler. Die Auswertung an einem Ferrariszähler ist nicht möglich. 
Funktionsweise
Die Blinkimpulse werden am Stromzähler über einen Fotowiderstand erfasst und mit einem Raspberry Pico W verarbeitet. Der Fotowiderstand wird einfach mit Klebeband vor die blinkende LED des Zählers geklebt. Wenn nötig, ist der Bereich des Fotowiderstands mit einer Abdeckung (Pappe) abzudunkeln. Es ist möglich, den Fotowiderstand mit einem maximal 1m langen zweiadrigen Kabel mit dem Pico zu verbinden. 
Darstellung
Beim Aufrufen der IP Adresse des Raspberry Pico W wird eine kleine Webseite angezeigt. Auf dieser finden sich 4 Links zu Auswertungen des Energieverbrauchs der letzten 2 Stunden, des letzten Tages, der letzten 31 Tage und der vergangenen 2 Jahre. In jedem der Graphen wird auch der Durchschnitt des Auswertezeitraums angezeigt.
Sonderfunktionen
Nach jeder vollen Stunde wird eine Backupdatei erstellt. In der „backup.py“ sind alle Informationen enthalten. Sie kann mit einem Editor von Hand bearbeitet werden. Beim Start der Software wird automatisch der Inhalt der „backup.py“ geladen. Die Uhrzeit bezieht die Software durch den Aufruf der NTP Funktion. Über Links kann die Systemzeit auf Sommer und Winterzeit gestellt werden. Es gibt auch die Möglichkeit ein Sofortbackup zu erstellen, ohne erst auf den nächsten Stundenwechsel zu warten. Ein Sonderbackup „sbackup.py“ kann ebenso erstellt werden. Die Backupdatei  „sbackup.py“ wird nicht automatisch erzeugt oder eingelesen. Sie dient nur für einen manuellen Servicefall, wenn die normale „backup.py“ nicht mehr verwendet werden kann.
Anwendung
1. Raspberry Pico W mit der aktuellen Micropython Firmware bespielen UF2 File ( https://micropython.org/download/rp2-pico-w/rp2-pico-w-latest.uf2 )
2. Download APP Thonny ( https://thonny.org )
3. Editieren der Zeilen 13-15 der „main.py“ (eigene WLAN Zugangsdaten und Anzahl der Impulse pro 1 KWh von Deinem Stromzähler eintragen)
4. Raspberry Pico W mit der Fotowiderstanddiode verbinden ( Pin 17 und Pin18 )
5. Fotowiderstand vor der blinkenden LED des Stromzählers befestigen (Klebeband)
6. Mit Thonny die Datei main.py zum Raspberry Pico W übertragen
7. über die IP Adresse den Raspberry Pico W in einem beliebigen Browser öffnen
##hier kannst Du weiterlesen
https://icplan.de/seite41/

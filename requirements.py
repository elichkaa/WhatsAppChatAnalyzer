# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# wa_analyser.py
# In diesen Endprojekt erstellt ihr eurer erstes größeres Programm, welches ihr 
# später auch für Bewerbungen und anderem vorzeigen könnt!
# 
# Im ersten Teil implementiert ihr Funktionen um Infographiken zu bestimmten 
# Fragen zu erstellen. 
# Im zweiten Teil werdet ihr das Programm dann durch eine textuelle Schnittstelle
# für Nutzer der Kommandozeile bereitstellen.
#
# Teil 1:
# Folge zunächst diesen Schritten:
#   1. Exportiere deinen ChatsApp Chat (ohne Medien)! 
#   2. Nimm die .txt Datei und bewege Sie in den Ordner in dem auch dieses Script 
#      liegt.
# 
# Bevor wir den Chat einlesen können müssen wir zunächst verstehen, was in der
# Datei enthalten ist. Dazu solltet Ihr euch diese genau angucken und das Muster
# erkennen.
# Hier ein paar zusätzliche Anmerkungen:
#   0. Die Zeichen sind nicht nur ASCII, also müssen wir daran denken die Datei
#      in utf-8 zu lesen.
#   1. Nicht jede neue Zeile ist auch eine neue Nachricht, denn eine Nachricht
#      kann auch ein neue Zeile Symbol beinhalten und sich somit über mehrere 
#      Zeilen erstrecken.
#   2. In Zeilen die eine weggelassene Media-Nachricht repräsentieren steht vor 
#      dem Datum und der Uhrzeit, sowie zu beginn der Nachricht selber der 
#      unsichtbare Unicode Code Point U+200E.
#      Zum Beispiel:
#           [U+200E][13.04.17, 11:37:25] Max Mustermann: [U+200E]Bild weggelassen
#      In Python könnt Ihr dieses Zeichen mit 
#           special_char = u"\u200e"
#      darstellen. In Visual Studio Code könnt ihr mit der Kommandoeingabe und 
#      ">highlighting of invisible characters" euch diese auch hervorgehoben 
#      anzeigen lassen.
#   3. Diese besonderen Zeichen wird auch bei Kontrollnachrichten wie zum Beispiel
#           [26.12.15, 20:42:10] [U+200E]Max Mustermann hat die Gruppe erstellt.
#           [26.12.15, 20:42:10] [U+200E]Max Mustermann hat dich hinzugefügt.
#      verwendet. Diese Nachrichten wollen wir von unserer Analyse auschließen.
#   4. Nicht eingespeicherte Personen werden mit der Telefonnummer angegeben. Diese
#      Telefonnummer werden mit besonderen utf-8 Code Punkten vor und nach der Nummer,
#      sowie mit in der Nummer angegeben. Vor und nach der Nummer stehen die
#      utf-8 Code Points U+202A und U+202C. "Leerzeichen" in der Nummer sind U+00A0.
#      In eurer Analyse stellen wir es euch frei ob ihr den Sender von
#           [15.04.17, 16:04:12] [U+202A]+49[U+00A0]1234[U+00A0]9876543[U+202C]: Sehr interessant.
#      als "+49 1234 9876543" oder als "[U+202A]+49[U+00A0]1234[U+00A0]9876543[U+202C]" erfasst.
#      Wir haben uns für die leichtere, zweite Variante entschieden, da die restlichen
#      Zeichen so oder so nicht sichtbar sind.
#
# Nun schreibe ein Python Programm welches diese Datei einliest und darauf basierend 
# Infographiken zu folgenden Fragen erstellt.
#  1. Was sind die 100 häufigsten Wörter?
#       -> Ausgabe in die Datei 100_most_common_words.txt
#               |Rang Anzahl Wort
#               |1.   345    ich
#               |2.   220    der
#               |...
#  2. Welches ist das 200., 300., 400. und 500. meistverwendete Wort?
#       -> Ausgabe in die Datei special_words.txt.
#  3. Wie viele Nachrichten hat jede Person geschrieben? 
#       -> Bar Chart
#  4. Wie hoch liegt der prozentuale Anteil an geschriebenen Nachrichten pro Person?
#       -> Pie Chart
#  5. Wie viele Nachrichten wurden pro Tag über die gesamte Existenz des Chats 
#     gesendet?
#       -> Line Chart mit Datum auf der x-Achse.
# Für Fortgeschrittene:
#  6. Wie viele Nachrichten wurden pro Stunde gesendet(, d. h. wann war die Gruppe am aktivsten)?
#       -> Bar / Line Chart
#  7. In welcher Stunde vom Tag war jede Person am aktivsten?
#       -> Für jede Person einen Scatter Plot (Line Chart) auf einem Diagramm.
#
# Um diese Graphen zu erzeugen musst du mehrere Funktionen schreiben, am Ende
# soll das Program durch den Aufruf der Funktion main alle Inforgrafiken generieren.
#
#   |def main(chat_filepath: string):
#   |    # ...
#   |
#   |main("wa_chat_with_my_bff.txt")
#
# Die Ausgabe eures Programms soll in Dateien gespeichert werden, für Plotly figures
# geht dies mit der Methode fig.write_image(filename: str). Die möglichen 
# Dateiformate sind .pdf, .png und .jpeg.
# Plotly braucht zum speichern von Diagrammen in Dateien die Python Bibliothek
# Kaleido. Diese könnte ihr durch folgenden Befehl installieren:
#       Windows: |pip install -U kaleido
#   MacOs/Linux: |pip3 install -U kaleido 
#
# Implementations Tipps:
#   1. Erstellt euch eine Klasse die die relevanten Informationen einer Textnachricht
#      speichert. Eure Analysen arbeiten dann mit der Liste von Instanzen dieser Klasse.
#   2. Das Datum und die Uhrzeit lassen sich durch Pythons datetime Klasse im Modul
#      datetime darstellen. Besonders wichtig für uns sind die Methoden 
#           datetime.strptime(text: str, format: str): datetime
#           dt_instance.strftime(format): str
#      Wie und welche Formate man spezifizieren kann ist einer eurer Teilaufgaben, 
#      hier eine gute Hilfestellung wenn ihr soweit seit:
#           https://www.programiz.com/python-programming/datetime/strptime
#   3. Wir definieren Wörter als alle durch Leerzeichen getrennten Zeichenketten. Dabei
#      ist die Kapitalisierung egal ("HaLLO" == "hallo"). Die Sonderzeichen 
#           ".,:;!?"
#      haben wir vor der Verarbeitung der Texte entfernt, damit Wörter richtig 
#      gezählt werden. Zum Beispiel:
#           "Ende"
#           "Ende."
#           "ende"
#           "Ende,"
#           => 4 Mal das Wort "ende"
#   4. Nehmt die Dokumentation von Plotly zu Hand und googelt Teilschritte wenn
#      ihr nicht wisst wie es geht! So machen wir es auch :D.
#          Bar Chart - https://plotly.com/python/bar-charts/
#          Pie Chart - https://plotly.com/python/pie-charts/
#          Line Chart - https://plotly.com/python/line-charts/
#
# Viel Spaß und viel Erfolg. Bei Fragen (welche absolut verständlich sind, denn
# das hier ist alles andere als eine triviale Aufgabe), stehen wir euch gerne zur
# Seite!
#
# ######################## Erst Teil 1 implementieren! #########################
#
# Teil 2:
# Im zweiten Teil eueres Endprojectes soll ihr eurer Programm in eine CLI umwandeln.
# Eure CLI soll nachher das folgende Aufrufmuster haben:
#       Windows: |python wa_analyser.py <filepath_to_chat> <output_directory>
#   MacOs/Linux: |python3 wa_analyser.py <filepath_to_chat> <output_directory>
# Achtung:
#   Windows Pfade enthalten "\", welche vom Terminal als Escape-Character interpretiert werden.
#   Damit diese als normale Zeichen interpretiert werden müssen wir unser gesamtes 
#   Argument in doppelte Anführungszeichen (") setzen.
#
# Alle erstellten Graphik-Dateien sollen im output_directory liegen. Übergibt der 
# Nutzer keinen output_directory, legt die Dateien im aktuellen Verzeichnis in einem
# neuen Ordner .\analysis-{chat file name} ab.
# Denkt daran das der Nutzer euch ggf. falsche Eingaben gibt. Klärt den Nutzer dann
# über den Fehler auf und sagt ihm wie man euer Programm richtig nutzt.
#
# Seit kreativ! Euer Programm soll die beschriebenen Fähigkeiten mindestens haben,
# weitere Fähigkeiten, also weitere Inforgraphiken, mehr Optionen der CLI, hübschere
# Farben bei den Graphiken usw. wird sehr gerne gesehen und macht dein Projekt besonders! 
# 
# Am wichtigsten: Habt Spaß, euer Projekt wird nicht bewertet. Wir wollen das ihr
# die Herausforderung angeht, dabei lernt und etwas für eure Zukunft mitnehmt. 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

.. index:: Ampel

*****
Ampel
*****

Um eine visuelle Anzeige für Rennstart und -stopp zur Verfügung zu stellen,
entschieden wir uns dafür, eine Ampel im „Formel-1-Stil“ zu bauen. Diese Ampel
besteht aus 8 großen LEDs, welche an einem rechteckigen Holzbrett
angebracht sind. Sie befindet sich direkt an der Zeitmessbrücke und ist
somit besonders gut bei Start- und Zieleinfahrt von den Fahrern einsehbar.

Die Startreihenfolge ist an jene der Formel-1 angelehnt und verläuft wie
folgt:

 * 1. Reihe rot
 * 2. Reihe rot
 * 3. Reihe rot
 * Reihe 1,2 und 3 aus, 4. Reihe grün

Die LEDs werden dabei vom UE9 angesteuert, wobei die Leistungsverstärkung
mittels Transistoren gewährleistet wird. Sie werden mit 12V Spannung
betrieben.

.. figure:: /images/sketches/traffic_lights_circuit.png

   Schaltbild

Probleme
--------

Unerwarteterweise bereitete uns die Ampel mit am meisten Schwierigkeiten, da
es wiederholt Probleme mit der Verstärkerschaltung gab und die richtige
Reihenfolge für das Aufleuchten der LEDs lange von Problemen verfolgt war.
Dieses Problem konnten wir  mit viel Geduld lösen, sodass die LEDs
letztendlich in richtiger Reihenfolge aufleuchten.

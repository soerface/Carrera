**************
Autopilot / KI
**************

Als zusätzliche Herausforderung haben wir dem Arduino beigebracht, die Strecke
möglichst schnell zu fahren. Um die aktuelle Autoposition festzustellen,
verwendet der Arduino die Daten der :doc:`Lichtschranken </hardware/sensors>`.
Zu jeder Lichtschranke ordnet der Arduino drei Arrays zu: Das erste Array
enthält die Geschwindigkeit, mit der das Auto fahren soll, sobald es die
Lichtschranke passiert. Das zweite Array enthält einen Delay, also eine
Zeitverzögerung (in Millisekunden). Nach Ablauf der dort angegebenen Zeit
beschleunigt das Auto auf den Wert, welcher im dritten Array gespeichert ist.

Dieser Ansatz wurde gewählt, da es so mit relativ wenig Lichtschranken möglich
ist, ein gutes Fahrverhalten zu realisieren.

Die Geschwindigkeit wird mittels :doc:`PWM-Signal </hardware/arduino>`
gesteuert.

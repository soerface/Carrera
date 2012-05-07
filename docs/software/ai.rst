.. index:: KI, Arduino, PWM

**************
Autopilot / KI
**************

Als zusätzliche Herausforderung haben wir dem Arduino beigebracht, die Strecke
möglichst schnell zu fahren. Um die aktuelle Autoposition festzustellen,
verwendet der Arduino die Daten der :doc:`Lichtschranken </hardware/sensors>`.
Zu jeder Lichtschranke ordnet der Arduino drei Arrays zu: Das erste Array
enthält die Geschwindigkeit, mit der das Auto fahren soll, sobald es die
Lichtschranke passiert. Das zweite Array beinhaltet einen Delay, also eine
Zeitverzögerung (in Millisekunden). Nach Ablauf der dort angegebenen Zeit
beschleunigt das Auto auf den Wert, welcher im dritten Array gespeichert ist.
Dieser Ansatz wurde gewählt, da es so mit relativ wenig Lichtschranken möglich
ist, ein gutes Fahrverhalten zu realisieren.

Der Arduino bietet zwar keinen analogen Ausgang, die Geschwindigkeit kann
jedoch mittels :ref:`PWM-Signal <pwm>` gesteuert werden.

Das Programm ist in Form eines :download:`Arduino Sketches </../ai/ai.pde>`
erhältlich.

Probleme
--------

Aktuell ist die :doc:`Streckenfreigabe </hardware/power_release>` nur für die
manuell gesteuerten Fahrzeuge umgesetzt, der Arduino lässt sich nicht stoppen.
Grundsätzlich gibt es zwei Möglichkeiten, dieses Problem zu lösen. Zum einen
elektrotechnisch, indem abhängig vom Signal des UE9 der Arduino physikalisch
von der Strecke getrennt wird. Dies würde keine Änderungen der Software
erfordern. Der andere Ansatz ist, ein einziges Kabel direkt zwischen Arduino
und UE9 zu verlegen. Über dieses Kabel ist zwar keine physikalische Trennung
möglich, wie sie bei den menschlichen Spielern angewandt wird, es kann jedoch
eine "Bitte" in Form eines Signals (HIGH oder LOW) an den Arduino gesendet
werden. Die Software des Arduinos müsste nun lediglich durch eine einfache
Abfrage erweitert werden, welche abhängig von diesem Signal fährt oder stehen
bleibt.

Ein größeres und für uns derzeit unlösbares Problem stellt die „Lernfähigkeit“
des Arduinos da. Aktuell müssen die Werte für die einzelnen Lichtschranken
per Hand ausprobiert und eingegeben werden. Eine zunächst scheinbar
naheliegende Lösung stellte sich nach den manuellen Tests als ungenügend
heraus:

Man könnte doch einfach die gesamte Strecke zunächst langsam abfahren, und nach
jeder Runde ein wenig beschleunigen. Fällt der Wagen nach einer bestimmten
Lichtschranke aus der Bahn, kann an dieser Stelle nicht weiter beschleunigt
werden. Dies wird solange durchgeführt, bis für jede Lichtschranke die
Maximalgeschwindigkeit gefunden wurde.

Dies ist jedoch aus einigen Gründen nur schwerlich umsetzbar:
   * Bei den manuellen Tests wurde auch die Position der Lichtschranken
     optimiert, da erkannt wurde, dass sie zu nah oder zu weit entfernt von
     den Kurven stehen. Diese Optimierung wäre auf diese Weise nicht möglich
   * Da der Wagen mit einer gewissen Geschwindigkeit ankommt, ist diese auch
     für die folgende Kurve von Bedeutung, nicht nur die Geschwindigkeit, die
     der Wagen annehmen soll. Der Wagen kann nicht sofort auf die gewünschte
     Geschwindigkeit gebracht werden. Somit ist die Frage „fliegt er raus oder
     nicht?“ auch massiv von der vorherigen Lichtschranke abhängig. Doch ist
     es nun sinnvoller, bei der aktuellen Lichtschranke stärker vom Gas zu
     gehen, oder bei der vorherigen? Das ist wiederum vom Aufbau der Strecke
     abhängig - wurden zuvor viele Kurven verwendet, war es eine lange Gerade,
     gab es Steigungen oder Gefälle?

All dies kann nicht mithilfe der Lichtschranken erfasst werden, sondern
erfordert manuelle Analysen und Tests oder mehr Daten.

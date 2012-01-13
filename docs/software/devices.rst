.. index:: UE9

***********************
Devices / UE9 Interface
***********************

LabJack bietet nicht nur Linuxtreiber für ihr UE9 an, sondern ebenfalls eine
`Schnittstelle zu Python <http://labjack.com/support/labjackpython>`_. Damit
ist es möglich, das gesamte Gerät vergleichsweise einfach zu nutzen.

Um die Nutzung für unsere Zwecke weiter zu vereinfachen, sind wir noch einen
Schritt weiter gegangen: Mittels Vererbung haben wir die von LabJack
bereitgestellte ``UE9`` Klasse um Methoden erweitert, welche speziell auf
unsere Zwecke abgestimmt sind. Dazu gehören etwa Methoden, welche die
:doc:`Ampelsequenz </hardware/traffic_lights>` abspielen oder die
:doc:`Lichtschranken </hardware/sensors>` an der Startlinie abfragen. Auf
diese Weise kann das eigentliche Messprogramm frei von kryptischen Portabfragen
bleiben und stattdessen Methoden mit aussagekräftigen Namen verwenden, welche
das Programm lesbarer machen.

Weiterhin hat diese Abstraktion den zusätzlichen Vorteil, dass das
Messprogramm auch mit anderen Geräten verwendet werden kann: Es kann selbst
unverändert bleiben, lediglich die Abstraktionsschicht muss für andere Geräte
neu geschrieben werden. Neben dem Interface für das UE9 wurde daher auch ein
virtuelles Messgerät geschrieben. Das virtuelle Gerät ist sehr
nützlich, wenn man die Software testen möchte, jedoch keinen UE9 zur
Verfügung hat. Das virtuelle Gerät löst dabei zufällig unterschiedliche
Aktionen aus, wie etwa das Passieren des Ziels, und zeigt Informationen an,
die es erhält, etwa das ein- oder ausschalten der
:doc:`Stromfreigabe </hardware/power_release>`.

Standardmäßig versucht das Programm zunächst, eine Verbindung zu einem realen
UE9 aufzubauen, wenn das fehlschlägt, wird auf das virtuelle zurückgegriffen.
Geplant ist außerdem ein Einstellungsdialog, welcher die Möglichkeit bieten
soll, während des Betriebes zwischen verschiedenen Geräten zu wechseln.

Im Folgenden sind die von LabJack bereitgestellten Methoden nicht aufgeführt.

.. autoclass:: devices.UE9
   :members:

.. autoclass:: devices.Virtual
   :members:

Die Dokumentation der Pinbelegung befindet sich im
:doc:`Hardware Teil </hardware/ue9>`.

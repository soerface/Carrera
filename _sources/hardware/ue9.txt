.. index:: UE9

***
UE9
***

Das UE9 ist ein universell einsetzbares Mess-Labor, welches die Schnittstelle
zur :doc:`Software </software/devices>` darstellt und so ermöglicht, Daten
auszulesen und verschiedene Vorgänge zu steuern. Wir verwendeten es zunächst
nur für die Zeitnahme durch die Start/Ziel-Lichtschranken, später kamen
die Steuerung der Relais für die :doc:`Streckenfreischaltung
</hardware/power_release>` und die :doc:`Ampel-Schaltung
</hardware/traffic_lights>` hinzu.

Gesteuert werden die einzelnen Elemente durch Low bzw. High Pegel, welche
verstärkt werden, um das dazugehörige Bauelement anzusteuern. Außerdem wird
erfasst, ob gerade eine Lichtschranke aktiviert ist, also ein Auto die
Start- / Ziellinie überquert.

Auf der Website von Meilhaus ist ein `Datenblatt des UE9
<http://www.meilhaus.de/index.php?id=26&L=0&user_produkte[PR]=85&cHash=2feb1f687f>`
erhältlich.

Schnittstellen
==============

.. image:: /images/sketches/UE9_Ports.png

Ampel:

   * Rot 1: FIO0
   * Rot 2: FIO1
   * Rot 3: FIO2
   * Grün: FIO3

:doc:`Streckenfreigabe </hardware/power_release>`:

   * Strecke 1: EIO4
   * Strecke 2: EIO5
   * Strecke 3: EIO6
   * Strecke 4: EIO7

Sensoren:

   * 1: EIO0
   * 2: EIO1
   * 3: EIO2
   * 4: EIO3

Probleme
========

Das UE9 selbst bereitete uns wenig Probleme, da es fehlerfrei und genau
arbeitete, jedoch mussten klare Absprachen mit dem Programmierer getroffen
werden, damit auch alles so funktioniert wie es soll. Meistens ging es um
die richtige Pinbelegung.

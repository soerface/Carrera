.. index:: Spielmodi

*********
Spielmodi
*********

Die Basisklasse aller Spielmodi ist „BaseMode”, jeder Spielmodus erbt von dieser
Klasse. Diese Klasse kümmert sich um alle grundlegenden Funktionalitäten,
die für jede Spielmodus von Bedeutung sind: Messung der Zeit, Zählung der
Runden, Aktualisierungen der Oberfläche ermöglichen, die Ampelsequenz
einleiten.

Was diese Klasse nicht übernimmt, ist die Entscheidung, wann ein Rennen
beendet ist, da dies von jedem Spielmodus abhängig ist. Dazu stehen drei
Methoden zur Verfügung, die von den Unterklassen überschrieben werden können:
``configure`` ermöglicht es, weitere Argumente zu verarbeiten, etwa die maximale
Anzahl von Runden oder ein Zeitlimit. ``on_player_passed_line`` wird aufgerufen,
wenn ein Spieler die Ziellinie durchquert; das entsprechende Spielerobjekt
wird als erstes Argument übergeben. Mithilfe von ``check_conditions`` können
weitere Überprüfungen durchgeführt werden, z.B. auf das erreichen des
Zeitlimits getestet werden, da diese Methode in jedem Schleifendurchgang
aufgerufen wird.

.. autoclass:: modes.BaseMode
   :members:
   :inherited-members:

Knock Out
=========

In einem „Knock Out“ Rennen fliegt in jeder Runde der langsamste Spieler raus.
Dadurch sind maximal drei Runden möglich, bei diesen stehen die Spieler aber
unter hohem Druck und Nervenkitzel.

.. autoclass:: modes.KnockOut
   :members:

Match
=====

Bei einem Match fahren 2-4 Spieler eine bestimmte Anzahl an Runden. Nach dem
Absolvieren aller Runden wird der Strom auf der entsprechenden Spur
abgeschaltet.

.. autoclass:: modes.Match
   :members:

Time Attack
===========

Im Modus „Time Attack“ wird eine bestimmte Zeit vorgegeben. Nach Ablauf der
Zeit wird auf allen Spuren der Strom abgeschaltet. Sieger ist, wer die meisten
Runden geschafft hat.

.. autoclass:: modes.TimeAttack
   :members:

Training
========

Im „Training” Modus kann auf jeder Spur separat trainiert werden. Dafür
wird eine maximale Anzahl von Runden angegeben, die auf jeder Strecke
absolviert werden können. Bei Erreichen des Limits wird der Strom von der
Strecke genommen, bis er wieder über den „Admin” Tab im Hauptfenster wieder
freigeschaltet wird. Nach der Freischaltung können auf dieser Spur wieder
soviele Runden gefahren werden, wie das Limit vorgibt.

.. autoclass:: modes.Training
   :members:

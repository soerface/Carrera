*********
Spielmodi
*********

Basisklasse aller Spielmodi:

.. autoclass:: modes.Mode
   :members:
   :inherited-members:

Match
=====

Bei einem Match fahren 2-4 Spieler eine bestimmte Anzahl an Runden. Nach dem
absolvieren aller Runden wird der Strom auf der entsprechenden Spur
abgeschaltet.

.. autoclass:: modes.Match
   :members:

Time Attack
===========

Im Modus "Time Attack" wird eine bestimmte Zeit vorgegeben. Nach Ablauf der
Zeit wird auf allen Spuren der Strom abgeschaltet. Sieger ist, wer die meisten
Runden geschafft hat.

.. autoclass:: modes.TimeAttack
   :members:

Knock Out
=========

In einem "Knock Out" Rennen fliegt in jeder Runde der langsamste Spieler raus.
Dadurch sind maximal drei Runden möglich, bei diesen stehen die Spieler aber
unter hohem Druck und Nervenkitzel.

.. autoclass:: modes.KnockOut
   :members:

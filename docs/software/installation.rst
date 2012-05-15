************
Installation
************

Gesamte Paketliste zum kopieren:

.. code-block:: bash

   apt-get install git python-pip build_essential libusb-1.0-0-dev

Neben einer funktionierenden Pythoninstallation (empfohlen: 2.7) sollte
zunächst das Versionskontrollsystem git installiert werden, um den
Quellcode dieser Software und den Code der UE9 Treiber komfortabel
beziehen zu können.

Um die Kommunikation mit dem UE9 zu ermöglichen, sind die Treiber und
Pythonmodule von LabJack erforderlich, eine ausführliche Anleitung gibt es
auf der
`Website von LabJack <http://labjack.com/support/linux-and-mac-os-x-drivers>`_,
die wichtigsten Schritte zur Installation sind allerdings ebenfalls hier
beschrieben.

Der Quellcode Software kann direkt von unserem Repository bezogen werden:

.. code-block:: bash

  git clone https://github.com/swege/Carrera

Die restlichen benötigten Pythonmodule sind in der mitgelieferten
requirements.txt aufgelistet. Mithilfe von pip können sie leicht installiert
werden:

.. code-block:: bash

  pip install -r requirements.txt

Es ist empfehlenswert, dies in einem virtualenv zu tun, um sie nicht
systemweit zu installieren - dies ist aber nicht erforderlich.
Gestartet wird die Messsoftware mit

.. code-block:: bash

   python measurement.py

Die für das eigenständige Fahren konzipierte Software besteht aus einem
einzigen Arduinosketch, zu finden in der Datei ``ai/ai.pde``, und kann mithilfe
der `Arduino IDE <http://arduino.cc/hu/Main/Software>`_ kompiliert und auf den
Arduino geladen werden.

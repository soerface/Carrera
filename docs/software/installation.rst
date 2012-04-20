************
Installation
************

Neben einer funktionierenden Pythoninstallation (empfohlen: 2.7) sollte
zunächst das Versionskontrollsystem git installiert werden, um den
Quellcode dieser Software und den Code der UE9 Treiber komfortabel
beziehen zu können.

.. code-block:: bash

  apt-get install git

Um die Kommunikation mit dem UE9 zu ermöglichen, sind die Treiber und
Pythonmodule von LabJack erforderlich, diese können mithilfe der von LabJack
angebotenen
`Anleitung <http://labjack.com/support/linux-and-mac-os-x-drivers>`_.

Zur grafischen Darstellung wird matplotlib und das zugehörige Pythonmodul
benötigt:

.. code-block:: bash

  apt-get install python-matplotlib

Der Quellcode Software kann direkt von unserem Repository bezogen werden:

.. code-block:: bash

  git clone https://github.com/swege/Carrera

Die restlichen benötigten Pythonmodule sind in der mitgelieferten
requirements.txt aufgelistet. Nachdem pip installiert wurde:

.. code-block:: bash

  apt-get install pip

Können sie leicht per

.. code-block:: bash

  pip install -r requirements.txt

heruntergeladen und installiert werden. Es ist empfehlenswert, dies in einem
virtualenv zu tun, um sie nicht systemweit zu installieren - dies ist aber
nicht erforderlich. Gestartet wird die Messsoftware mit

.. code-block:: bash

   python gui.py

Die für das eigenständige Fahren konzipierte Software besteht aus einem
einzigen Arduinosketch, zu finden in der Datei ``ai/ai.pde``, und kann mithilfe
der `Arduino IDE <http://arduino.cc/hu/Main/Software>`_ auf den Arduino
übertragen werden.

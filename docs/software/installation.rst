************
Installation
************

Linux
=====

(getestet unter Ubuntu 12.04)

Gesamte Paketliste zum kopieren:

.. code-block:: bash

   apt-get install git python-pip build_essential libusb-1.0-0-dev python-virtualenv

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

.. code-block:: bash

   git clone https://github.com/labjack/exodriver
   cd exodriver/liblabjackusb/
   make
   sudo make install
   cd ..
   sudo cp 10-labjack.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules
   cd

Der Quellcode Software kann direkt von unserem Repository bezogen werden,
die Erstellung eines eigenen Verzeichnisses könnte für den nächsten Schritt
von Nutzen sein:

.. code-block:: bash

   mkdir carrera
   cd carrera/
   git clone https://github.com/swege/Carrera.git
   cd Carrera/

Es ist empfehlenswert, die restlichen benötigten Pythonmodule in einem
virtualenv zu installieren, um sie nicht systemweit zu haben und eventuell
Konflikte mit anderen Programmen hervorzurufen.

Die restlichen benötigten Pythonmodule sind in der mitgelieferten
requirements.txt aufgelistet. Mithilfe von pip können sie leicht installiert
werden:

.. code-block:: bash

   # virtualenv erstellen
   virtualenv --system-site-packages ../venv
   # virtualenv aktivieren (jedes mal nötig)
   . ../venv/bin/activate
   # Module installieren
   pip install -r requirements.txt

Gestartet wird die Messsoftware mit

.. code-block:: bash

   python measurement.py

Windows
=======

(getestet unter Windows XP)

Python 2.7
----------

`Herunterladen <http://www.python.org/ftp/python/2.7/python-2.7.msi>`_ und Installer
starten. Manuelle Einstellungen im Installationsassistenten sollten nicht
nötig sein.

Umgebungvariable anpassen: *Start › Systemsteuerung (klassische Ansicht) ›
System › Reiter "Erweitert" › Umgebungsvariablen*

Variable ``Path`` bearbeiten und den Pfad für Python und dazugehörige Scripte
anfügen:

::

   ;C:\Python27;C:\Python27\Scripts

**Nichts entfernen**, nur *anhängen*, sonst wird das System unbrauchbar!

pip
---

``pip`` wird benötigt, um später weitere Pythonmodule einfach zu installieren.
Zunächst `setuptools
<http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe>`_
herunterladen und installieren.

Eine neue Eingabeaufforderung starten (die oben genannten Änderungen an der
``Path`` Variable müssen bereits erfolgt und bestätigt worden sein) und pip
installieren:

::

   easy_install pip

Versionskontrollsystem Git
--------------------------

`Herunterladen <http://git-scm.com/download/win>`_ und installieren. Während
der Installation beim Schritt *Adjusting your PATH environment* die Option
*Run Git from the Windows Command Prompt* wählen. Macht das gleiche wie wir
vorhin manuell gemacht haben, nur für Git statt Python. Restliche Einstellungen
können unberührt bleiben.

GTK
---

Für die grafische Oberfläche wird GTK2 verwendet. Dieses kann mitsamt der
für uns erforderlichen Python bindings als `all-in-one bundle
<http://ftp.gnome.org/pub/GNOME/binaries/win32/pygtk/2.24/pygtk-all-in-one-2.24.0.win32-py2.7.msi>`_
bezogen werden.

LabJack UE9
-----------

Für die Einrichtung des UE9 ist die `Installationsanleitung von LabJack
<http://labjack.com/ue9>`_ zu befolgen.

Quellcode herunterladen
-----------------------

Zum herunterladen der Software kommt Git zum Einsatz. Öffne das Verzeichnis,
in welches die Software kopiert werden soll. *Rechtsklick › Git Bash* öffnet
eine Eingabeaufforderung, hier folgende Befehle ausführen, um den Quellcode
herunterzuladen und die restlichen Pythonmodule zu installieren.

::

   git clone https://github.com/swege/soapboxderby.git
   git clone https://github.com/swege/Carrera.git
   cd soapboxderby
   pip install -r requirements.txt

Gestartet wird die Messsoftware mit

.. code-block:: bash

   python measurement.py

Arduino
=======

Die für das eigenständige Fahren konzipierte Software besteht aus einem
einzigen Arduinosketch, zu finden in der Datei ``ai/ai.pde``, und kann mithilfe
der `Arduino IDE <http://arduino.cc/hu/Main/Software>`_ kompiliert und auf den
Arduino geladen werden.

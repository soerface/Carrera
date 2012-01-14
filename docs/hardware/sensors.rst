.. index:: Lichtschranken

**************
Lichtschranken
**************

Die Lichtschranken verwendeten wir zunächst für die
:doc:`Zeitmessung </software/measuring>` der einzelnen Runden bzw. Rennen.
Hierfür verwendeten wir ein Gestell an dem für jede der vier Bahnen eine
Lichtschranke befestigt war. Dieses Gestell war bereits vorhanden, sodass wir
nur noch die Software anpassen mussten. Um die Daten der Lichtschranken am
Computer auslesen zu können, verwendeten wir ein UE9, auf das später noch
genauer eingegangen wird.

Zu den anfänglich vier Lichtschranken kamen im Laufe der Zeit acht weitere
hinzu. Diese stellten wir vor jeder wichtigen Kurve entlang der Stecke auf,
um ein computergesteuertes Fahrzeug mit der nötigen Spannung zu versorgen,
sodass es die Runde optimal fahren kann.

Die Lichtschranken bestehen aus einer Platine und einem Reflexsensor; fährt
ein Auto unter diesem Sensor hindurch, sorgt die Schaltung dafür, dass mittels
eines Pull-Down Widerstandes der High-Pin des Arduinos auf Masse gezogen
wird. Dabei machen wir uns die Eigenschaften des Arduinos zu Nutzen, da es
bereits die Möglichkeit eines :index:`Pull-Down` Widerstandes besitzt müssen wir
lediglich die Lichtschranke durch ein Kabel mit dem entsprechndem Port verbinden.

Als Hilfe diente uns ein `Tutorial von arduino.cc
<http://arduino.cc/it/Tutorial/Button>`_, in welchem am Beispiel eines
einfachen Buttons die Schaltung und dazu nötige Software erläutert wurde.

.. figure:: /images/sketches/sensor_circuit.png
   :width: 75%

   Schaltbild einer Reflexlichtschranke mit Anschluss an das Arduino


.. figure:: /images/sketches/pull-down.png

   Prinzip eines Pull-Down

Probleme
========

Gegen Ende des Projekts, nachdem wir uns lange mit dem selbständigen Fahren
beschäftigt haben, schlossen wir die Zeitmessung, die bereits lange
abgeschlossen war. und mussten uns einem neuem Problem stellen ein
reproduzierbarer Fehler welcher dafür sorgte, dass einige Lichtschranken bei
Aktivierung andere beeinflusst. Dieser Fehler kam Zustande, weil wir ein
Verlängerungskabel verwendeten, welches den Ansprüchen nicht genügte,
sodass wir es noch austauschen mussten. Das Kabel welches durch
Quetschverbindugen an den Streckern befestigt war muss an diesen
Quetschverbindungen nich perfekt isoliert haben, sodass es ständig zu
Fehlsignalen kam.

.. figure:: /images/photos/sensor_1.jpg

.. figure:: /images/photos/sensor_2.jpg

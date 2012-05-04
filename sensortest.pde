void setup() {
    int j;
    for (int i=0; i<11; i++) {
        j = i + 22;
        pinMode(j, INPUT);
        digitalWrite(j, HIGH);
    }
    Serial.begin(9600);
}

void loop() {
    bool v;
    int j;
    char incoming;
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    Serial.println("");
    for (int i=0; i<11; i++) {
        j = i + 22;
        v = digitalRead(j);
        Serial.println("-");
        Serial.println(j, DEC);
        Serial.println(v, DEC);
    }
    Serial.println("-------");
    while (true) {
        while (Serial.available()) {
            incoming = Serial.read();
        }
        if (incoming == '1') {
            break;
        }
    }
}

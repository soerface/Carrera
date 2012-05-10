void setup() { int j;
    for (int i=0; i<12; i++) {
        j = i + 22;
        // Workarounds for broken arduino
        if (j == 24) {
            j = 53;
        }
        if (j == 33) {
            j = 43;
        }

        pinMode(j, INPUT);
        digitalWrite(j, HIGH);
    }
    Serial.begin(9600);
}

void loop() {
    bool v;
    int j;
    char incoming;
    Serial.println('-');
    for (int i=0; i<12; i++) {
        j = i + 22;
        // Workarounds for broken arduino
        if (j == 24) {
            j = 53;
        }
        if (j == 33) {
            j = 43;
        }

        v = digitalRead(j);
        if (!v) {
            Serial.println(j, DEC);
        }
    }
    delay(20);
    /*
    while (true) {
        while (Serial.available()) {
            incoming = Serial.read();
        }
        if (incoming == '1') {
            break;
        }
    }
    */
}

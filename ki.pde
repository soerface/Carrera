int car_pin = 11;
int value = 0;
int last_value = 0;

void setup() {
    for (int i=0; i<14; i++) {
        if (i == car_pin) {
            pinMode(i, OUTPUT);
        }
        else if (i == 13) {
            continue;
        }
        else {
            pinMode(i, INPUT);
            // connect pull up resistor
            digitalWrite(i, HIGH);
        }
    }
}

int VALUES[14] = {60, 70, 80, 90, 100, 80, 90, 100, 50, 60, 70, 80, 90, 100};

void loop() {
    bool sensor;
    for(int i=0; i<14; i++) {
        if (i == car_pin) {
            continue;
        }
        sensor = digitalRead(i);
        if (sensor == LOW) {
            value = VALUES[i];
        }
    }
    analogWrite(car_pin, value);
}

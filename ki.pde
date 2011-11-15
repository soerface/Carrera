int car_pin = 11;
int value = 0;
int last_value = 0;

void setup() {
    int sensors[14];
    for (int i=0; i<14; i++) {
        if (i == car_pin) {
            pinMode(i, OUTPUT);
        }
        else {
            pinMode(i, INPUT);
        }
    }
}

int VALUES[14] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 0, 120, 130, 140};

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

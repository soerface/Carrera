int car_pin = 11;
int last_sensor = 0;
int value = 0;
unsigned long time = 0;

int VALUES1[10] = {    0,     0,    0,    0,    0,    0,    0,    0,    0,    0};
int DELAY[10] =   { 1000,  1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};
int VALUES2[10] = {   94,    94,   94,   94,   94,   94,   94,   94,   94,   94};


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

void loop() {
    bool sensor;
    for(int i=0; i<10; i++) {
        if (i == car_pin) {
            continue;
        }
        sensor = digitalRead(i);
        if (sensor == LOW) {
            value = VALUES1[i];
            time = millis();
            last_sensor = i;
        }
        if (millis() - time > DELAY[last_sensor]) {
            value = VALUES2[last_sensor];
        }
    }
    analogWrite(car_pin, value);
}

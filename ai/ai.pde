/*
    This program is used to control the speed of the car for the individual
    track sections. Currently the values / the speed is hardcoded and they
    need to be adjusted manually for each track.
*/
int car_pin = 11;
unsigned long time = 0;

// the speed of the car when it enters the light barrier
// Sensor number:     0    1    2    3    4    5    6   7
int VALUES1[8] = {220, 254, 154, 205, 165, 205, 154, 175};
// time in ms to keep that speed
int DELAY[8] =   { 400, 400,  50, 50,   4, 200, 150,  50};
// new speed for the car when the time from above is over
int VALUES2[8] = {55, 95, 130, 135, 135, 105, 115, 25};

int START_VALUE = 180;


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
    int last_sensor = -1;
    int value = START_VALUE;
    int last_value = -1;
    bool sensor;
    int j;
    analogWrite(car_pin, 255);
    // check the start signal of the UE9
    while (digitalRead(12)) {
        // only update the pwm signal if the value actually changed, should take
        // some load off the arduino
        if (last_value != value) {
            // break
            if (value == 0) {
                analogWrite(car_pin, 255 - value);
                delay(1);
                //analogWrite(10, 255);
            } else {
                analogWrite(10, 0);
                delay(1);
                analogWrite(car_pin, 255 - value);
            }
            last_value = value;
        }
        for(int i=0; i<8; i++) {
            if (i == car_pin) {
                continue;
            }
            // Workaround for a defective light barrier / port
            if (i == 5) {
                j = 8;
            }
            else {
                j = i;
            }
            sensor = digitalRead(j);
            if (sensor == LOW) {
                value = VALUES1[i];
                time = millis();
                last_sensor = i;
            }
            if (last_sensor != -1 && millis() - time > DELAY[last_sensor]) {
                value = VALUES2[last_sensor];
            }
        }
    }
}

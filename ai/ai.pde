/*
    This program is used to control the speed of the car for the individual
    track sections. Currently the values / the speed is hardcoded and they
    need to be adjusted manually for each track.
*/
int car_pin = 11;
unsigned long time = 0;

// the speed of the car when it enters the light barrier
// Sensor number:   0    1    2    3    4    5    6    7    8    9   10
int VALUES1[11] = {  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0};
// time in ms to keep that speed
int DELAY[11] =   {999, 999, 999, 999, 999, 999, 999, 999, 999, 999, 999};
// new speed for the car when the time from above is over
int VALUES2[11] = {150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150};

int START_VALUE = 130;


void setup() {
    int j;
    for (int i=0; i<11; i++) {
        j = i + 22;
        if (i == car_pin) {
            pinMode(i, OUTPUT);
        }
        else {
            pinMode(j, INPUT);
            // connect pull up resistor
            digitalWrite(j, HIGH);
        }
    }
}

void loop() {
    int last_sensor = -1;
    int value = START_VALUE;
    int last_value = -1;
    bool sensor;
    int j;
    // check the start signal of the UE9
    //while (digitalRead(12)) {
    while (true) {
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
        for(int i=0; i<11; i++) {
            if (i == car_pin) {
                continue;
            }
            j = i + 22;
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

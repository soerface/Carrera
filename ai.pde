/*
    This program is used to control the speed of the car for the individual
    track sections. Currently the values / the speed is hardcoded and they
    need to be adjusted manually for each track.
*/
int car_pin = 11;
int last_sensor = 0;
int value = 0;
int last_value = -1;
unsigned long time = 0;
bool started = false;

// the speed of the car when it enters the light barrier
// Sensor number:     0    1    2    3    4    5    6   7
int VALUES1[8] = {   35,   1, 101,  50,  90,  50, 101,  80};
// time in ms to keep that speed
int DELAY[8] =   {  150, 450,  75,  30,  10,  50, 500,  75};
// new speed for the car when the time from above is over
int VALUES2[8] = {  200, 160, 125, 120, 120, 150, 140, 230};


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
    int j;
    if (started == false) {
        last_value = value = 0;
        analogWrite(car_pin, value);
        started = true;
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
            value = 255 - VALUES1[i];
            time = millis();
            last_sensor = i;
        }
        if (millis() - time > DELAY[last_sensor]) {
            value = 255 - VALUES2[last_sensor];
        }
    }
    // only update the pwm signal if the value actually changed, should take
    // some load off the arduino
    if (last_value != value) {
        analogWrite(car_pin, value);
        // break
        if (value == 0) {
            analogWrite(10, 255);
        } else {
            analogWrite(10, 0);
        }
        last_value = value;
    }
}

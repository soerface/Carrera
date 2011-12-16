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

// the speed of the car when it enters the light barrier
int VALUES1[10] = {    0,     0,    0,    0,    0,    0,    0,    0,    0,    0};
// time in ms to keep that speed
int DELAY[10] =   {  500,   500,  500,  500,  500,  500,  500,  500,  500,  500};
// new speed for the car when the time from above is over
int VALUES2[10] = {   97,    97,   97,   97,   97,   97,   97,   97,   97,   97};


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
        // TODO: Workaround for a defective light barrier / port
        if (i == 5) {
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
    // only update the pwm signal if the value actually changed, should take
    // some load off the arduino
    if (last_value != value) {
        analogWrite(car_pin, value);
        last_value = value;
    }
}

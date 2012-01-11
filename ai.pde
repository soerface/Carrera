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
int VALUES1[8] = {   40,     7,  101,  50,  90,  60,  101,  150};
// time in ms to keep that speed
int DELAY[8] =   {  150,   200,  100,  30,  10,  25,  500,  150};
// new speed for the car when the time from above is over
int VALUES2[8] = {  220,   170,  140, 120,  120, 155,  101,  245};


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

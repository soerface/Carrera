/*
    This program is used to control the speed of the car for the individual
    track sections. Currently the values / the speed is hardcoded and they
    need to be adjusted manually for each track.
*/
int break_pin = 10;
int car_pin = 11;
int power_release_pin = 12;
unsigned long time = 0;

// the speed of the car when it enters the light barrier
// Sensor number:     0     1     2     3     4     5     6     7     8     9    10    11
int VALUES1[12] = {   -1,   -1,   50,  130,  200,  130,  180,  130,  100,  180,  180,  255};
// time in ms to keep that speed
int DELAY[12] =   { 5000, 5000,  180,  300,    5,  200,   40,   50,   10,  999,  999,  500};
// new speed for the car when the time from above is over
int VALUES2[12] = {  180,  130,  140,  140,  140,  160,  220,  200,  230,  220,  200,  255};

int START_VALUE = 180;


void setup() {
    int j;
    for (int i=0; i<12; i++) {
        j = i + 22;
        if (j == 24) {
            j = 53;
        }
        pinMode(j, INPUT);
        // connect pull up resistor
        digitalWrite(j, HIGH);
    }
    pinMode(11, OUTPUT);
    digitalWrite(11, HIGH);
    pinMode(power_release_pin, INPUT);
    pinMode(break_pin, OUTPUT);
}

void loop() {
    int last_sensor = -1;
    int value = START_VALUE;
    bool sensor;
    bool power;
    int j;
    int i = 0;
    while (true) {
        // check the start signal of the UE9
        if (!digitalRead(power_release_pin)) {
            // drive to the start and stop
            power = false;
        }
        else {
            power = true;
        }
        // break
        if (value == -1) {
            analogWrite(car_pin, 255);
            digitalWrite(break_pin, HIGH);
        } else {
            digitalWrite(break_pin, LOW);
            analogWrite(car_pin, 255 - value);
        }
        for(int i=0; i<12; i++) {
            j = i + 22;
            if (j == 24) {
                j = 53;
            }
            sensor = digitalRead(j);
            if (sensor == LOW) {
                value = VALUES1[i];
                if (!power) {
                    if (i == 9) {
                        value = 100;
                    }
                    else if (i == 10) {
                        value = -1;
                    }
                    else if (i == 11) {
                        value = -1;
                    }
                }
                time = millis();
                last_sensor = i;
            }
            if (last_sensor != -1 && millis() - time > DELAY[last_sensor]) {
                if (power or (!power and last_sensor != 9 and last_sensor != 10 and last_sensor != 11)) {
                    value = VALUES2[last_sensor];
                }
            }
        }
    }
}

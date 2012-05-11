/*
    This program is used to control the speed of the car for the individual
    track sections. Currently the values / the speed is hardcoded and they
    need to be adjusted manually for each track.
*/
int break_pin = 10;
int car_pin = 11;
int power_release_pin = 12;
int num_sensors = 12;
unsigned long time = 0;

// the speed of the car when it enters the light barrier
// Sensor number:     0     1     2     3     4     5     6     7     8     9    10    11
int VALUES1[12] = {  255,   40,  110,   10,  120,   80,  120,   60,  100,  170,   80,   90};
// Values for last round
int LAST_VAL[12] ={   -1,   -2,   -2,   -2,   -2,   -2,   -2,   -2,   -2,  120,   80,   70};


// time in ms to keep that speed
int DELAY[12] =   {   50,  350,   20,   50,  200,  150,  150,  150,  150,  150,  150,  150};
// new speed for the car when the time from above is over
int VALUES2[12] = {  200,   80,   50,  150,    0,   80,   80,   80,   80,   80,   80,   80};

int START_VALUE = 80;


void setup() {
    int j;
    for (int i=0; i<num_sensors; i++) {
        j = i + 22;
        // Workaround for broken arduino
        if (j == 24) {
            j = 53;
        }
        if (j == 33) {
            j = 43;
        }
        pinMode(j, INPUT);
        // connect pull up resistor
        digitalWrite(j, HIGH);
    }
    pinMode(car_pin, OUTPUT);
    digitalWrite(car_pin, HIGH);
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
            analogWrite(car_pin, 0);
            digitalWrite(break_pin, HIGH);
        } else {
            digitalWrite(break_pin, LOW);
            analogWrite(car_pin, value);
        }
        for(int i=0; i<num_sensors; i++) {
            j = i + 22;
            // Workaround for broken arduino
            if (j == 24) {
                j = 53;
            }
            if (j == 33) {
                j = 43;
            }
            sensor = digitalRead(j);
            if (sensor == LOW) {
                value = VALUES1[i];
                if (!power) {
                    value = LAST_VAL[i];
                    if (value == -2) {
                        value = VALUES1[i];
                    }
                }
                time = millis();
                last_sensor = i;
            }
            if (last_sensor != -1 && millis() - time > DELAY[last_sensor]) {
                if (power or (!power and last_sensor != 9 and last_sensor != 10 and last_sensor != 11)) {
                    // original VALUES2, VALUES1 to not use "time delta"
                    value = VALUES1[last_sensor];
                }
            }
        }
    }
}

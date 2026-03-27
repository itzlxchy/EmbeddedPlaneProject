#include "config.h"
#include "motor.h"
#include "serial_cmd.h"

Motor left_motor, right_motor;

void setup() {
    serial_init(115200);
    motor_init(&left_motor,  LEFT_PWM,  MOTOR_BIAS);
    motor_init(&right_motor, RIGHT_PWM, 0.0f);
}

void loop() {
    serial_update(&left_motor, &right_motor);
}
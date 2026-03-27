#include "config.h"
#include "motor.h"

Motor left_motor, right_motor;

void setup() {
    motor_init(&left_motor,  LEFT_PWM,  MOTOR_BIAS);
    motor_init(&right_motor, RIGHT_PWM, 0.0f);
}

void loop() {
    motor_set_power(&left_motor, &right_motor, 80);
}
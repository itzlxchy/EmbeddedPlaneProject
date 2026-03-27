#include "motor.h"

static int clamp(int val, int min, int max) {
    if (val < min) return min;
    if (val > max) return max;
    return val;
}

// Write a power level to one motor (forward direction)
static void write_motor(Motor *m, int power) {
    m->power = (uint8_t)clamp(power, 0, 100);
    analogWrite(m->pwm_pin, (m->power * 255) / 100);
}

void motor_init(Motor *m, uint8_t pwm_pin, float bias) {
    m->pwm_pin = pwm_pin;
    m->power   = 0;
    m->bias    = bias;

    pinMode(m->pwm_pin, OUTPUT);

    motor_stop(m);
}

void motor_set_power(Motor *left, Motor *right, uint8_t power) {
    // bias shifts power around the average — positive favours right, negative favours left
    int adjust = (int)(left->bias * power);

    write_motor(left,  power - adjust);
    write_motor(right, power + adjust);
}

void motor_apply_bias(Motor *left, Motor *right) {
    // Re-applies the bias split based on current power — for small in-flight corrections
    int adjust = (int)(left->bias * ((left->power + right->power) / 2.0f));

    write_motor(left,  (int)left->power  - adjust);
    write_motor(right, (int)right->power + adjust);
}

void motor_stop(Motor *m) {
    m->power = 0;
    // IN1 and IN2 both HIGH = active brake on the L298N
    analogWrite(m->pwm_pin, 0);
}

void motor_stop_all(Motor *left, Motor *right) {
    motor_stop(left);
    motor_stop(right);
}
#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

// Holds everything needed to run one motor on an L298N
typedef struct {
    uint8_t pwm_pin;
    uint8_t power;    // current power level, 0-100
    float   bias;     // trim correction, -1.0 to +1.0 (store on left motor)
} Motor;

// Set up pins and zero the motor — call once per motor in setup()
void motor_init(Motor *m, uint8_t pwm_pin, float bias);

// Set both motors from a single 0-100 value — bias shifts the split around that average
// e.g. power=80, bias=0.1 → left gets 72, right gets 88
void motor_set_power(Motor *left, Motor *right, uint8_t power);

// Fine-tune an already-running pair using the bias stored on the left motor
// Useful for small in-flight corrections on top of set_power
void motor_apply_bias(Motor *left, Motor *right);

// Stop a single motor
void motor_stop(Motor *m);

// Stop both motors at once
void motor_stop_all(Motor *left, Motor *right);

#endif
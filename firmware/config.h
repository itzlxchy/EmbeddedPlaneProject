#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// Motor pins
#define LEFT_PWM    6
#define LEFT_IN1    7
#define LEFT_IN2    8

#define RIGHT_PWM   9
#define RIGHT_IN1   10
#define RIGHT_IN2   11

// Positive = right gets more power, negative = left gets more
#define MOTOR_BIAS  0.1f

#endif
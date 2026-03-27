#ifndef CONFIG_H
#define CONFIG_H
//#define DEBUG_SERIAL
#include <Arduino.h>

// Motor pins
#define LEFT_PWM    12
#define RIGHT_PWM   13

// Positive = right gets more power, negative = left gets more
#define MOTOR_BIAS  0.0f

#endif
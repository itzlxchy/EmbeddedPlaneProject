#ifndef SERIAL_CMD_H
#define SERIAL_CMD_H

#include "motor.h"

// Add DEBUG_SERIAL to config.h to enable debug output
// #define DEBUG_SERIAL

#ifdef DEBUG_SERIAL
    #define DEBUG(msg)        Serial.println(msg)
    #define DEBUG_VAL(k, v)   Serial.print(k); Serial.println(v)
#else
    #define DEBUG(msg)
    #define DEBUG_VAL(k, v)
#endif

// Call once in setup()
void serial_init(int baud);

// Call every loop() — reads incoming commands and acts on them
void serial_update(Motor *left, Motor *right);

#endif
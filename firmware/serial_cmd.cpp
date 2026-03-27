
// Serial command reference:
//   MOTOR_SPEED:0-100   — set both motors (bias shifts the split)
//   MOTOR_BIAS:-1.0-1.0 — update trim, positive favours right motor
//   MOTOR_STOP          — kill both motors immediately
//   STATUS              — print current speed and bias values

#include "serial_cmd.h"

void serial_init(int baud) {
    Serial.begin(baud);
    DEBUG("Serial ready");
}

// Parse and handle one complete command string e.g. "MOTOR_SPEED:50"
static void handle_command(const char *cmd, Motor *left, Motor *right) {

    if (strncmp(cmd, "MOTOR_SPEED:", 12) == 0) {
        int speed = atoi(cmd + 12);
        motor_set_power(left, right, speed);
        DEBUG_VAL("Speed set: ", speed);

    } else if (strncmp(cmd, "MOTOR_BIAS:", 11) == 0) {
        float bias = atof(cmd + 11);
        left->bias = bias;
        motor_apply_bias(left, right);
        DEBUG_VAL("Bias set: ", bias);

    } else if (strcmp(cmd, "MOTOR_STOP") == 0) {
        motor_stop_all(left, right);
        DEBUG("Motors stopped");

    } else if (strcmp(cmd, "STATUS") == 0) {
        Serial.print("Speed L: ");  Serial.println(left->power);
        Serial.print("Speed R: ");  Serial.println(right->power);
        Serial.print("Bias:    ");  Serial.println(left->bias);

    } else if (isdigit(cmd[0]) || (cmd[0] == '-' && isdigit(cmd[1]))) {
        int speed = atoi(cmd);
        motor_set_power(left, right, speed);
        DEBUG_VAL("Speed set: ", speed);
    } else {
        Serial.print("Unknown command: ");
        Serial.println(cmd);
    }
}

void serial_update(Motor *left, Motor *right) {
    static char buf[32];
    static uint8_t pos = 0;

    // Read one character at a time, build up a command until newline
    while (Serial.available()) {
        char c = Serial.read();

        if (c == '\n' || c == '\r') {
            if (pos > 0) {
                buf[pos] = '\0';
                handle_command(buf, left, right);
                pos = 0;
            }
        } else if (pos < sizeof(buf) - 1) {
            buf[pos++] = c;
        }
    }
}
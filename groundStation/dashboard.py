import tkinter as tk
import pygame

# --- Constants ---
POLL_RATE_MS = 50

AXIS_LEFT_X  = 0
AXIS_LEFT_Y  = 1
AXIS_RIGHT_X = 2
AXIS_L2      = 4
AXIS_R2      = 5

BUTTON_CIRCLE = 1


# --- Utility ---
def clamp(val, min_val, max_val):
    if val < min_val:
        return min_val
    if val > max_val:
        return max_val
    return val


# --- Input Reading ---
def read_roll(js):
    return clamp(js.get_axis(AXIS_LEFT_X), -1.0, 1.0)


def read_pitch(js):
    return clamp(-js.get_axis(AXIS_LEFT_Y), -1.0, 1.0)


def read_rudder(js):
    return clamp(js.get_axis(AXIS_RIGHT_X), -1.0, 1.0)


def normalise_trigger(val):
    # handles both [-1,1] and [0,1] ranges
    if val < 0:
        return (val + 1.0) / 2.0
    return val


def read_throttle(js):
    l2_raw = js.get_axis(AXIS_L2)
    r2_raw = js.get_axis(AXIS_R2)

    # convert from [-1,1] → [0,1]
    l2 = (l2_raw + 1.0) / 2.0
    r2 = (r2_raw + 1.0) / 2.0

    l2_pressed = l2 > 0.1
    r2_pressed = r2 > 0.1

    if l2_pressed and r2_pressed:
        return 1.0
    if l2_pressed or r2_pressed:
        return 0.5
    return 0.0


def read_autopilot(js):
    return js.get_button(BUTTON_CIRCLE)


# --- UI ---
def create_label(parent, text):
    label = tk.Label(parent, text=text, font=("Courier", 20))
    label.pack(anchor="w")
    return label


def update_labels(js, labels, state):
    pygame.event.pump()

    roll     = read_roll(js)
    pitch    = read_pitch(js)
    rudder   = read_rudder(js)
    throttle = read_throttle(js)

    pressed = read_autopilot(js)

    # toggle on press edge
    if pressed and not state["held"]:
        state["autopilot"] = not state["autopilot"]

    state["held"] = pressed

    labels["roll"].config(text=f"Roll:     {roll:+.2f}")
    labels["pitch"].config(text=f"Pitch:    {pitch:+.2f}")
    labels["rudder"].config(text=f"Rudder:   {rudder:+.2f}")
    labels["throttle"].config(text=f"Throttle: {throttle:.2f}")
    labels["auto"].config(text=f"Auto:     {'ON' if state['autopilot'] else 'OFF'}")


# --- Main ---
def main():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No controller found")
        return

    js = pygame.joystick.Joystick(0)
    js.init()

    window = tk.Tk()
    window.title("Controller Monitor")

    labels = {
        "roll":     create_label(window, "Roll:"),
        "pitch":    create_label(window, "Pitch:"),
        "rudder":   create_label(window, "Rudder:"),
        "throttle": create_label(window, "Throttle:"),
        "auto":     create_label(window, "Auto:")
    }

    state = {
        "autopilot": False,
        "held": False
    }

    def loop():
        update_labels(js, labels, state)
        window.after(POLL_RATE_MS, loop)
      

    loop()
    window.mainloop()


if __name__ == "__main__":
    main()

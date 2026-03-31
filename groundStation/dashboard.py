import tkinter as tk
import pygame

# ── Colours ──────────────────────────────────────────────────────────────────
BG     = "#0a0e1a"
PANEL  = "#111827"
BORDER = "#1e2d40"
ACCENT = "#00d4ff"
GREEN  = "#00ff88"
RED    = "#ff3b3b"
TEXT   = "#e0f0ff"
MUTED  = "#4a6080"

POLL_MS = 50  # ms between reads (~20 Hz)


class AxisBar(tk.Frame):
    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, bg=PANEL, **kwargs)
        tk.Label(self, text=label, bg=PANEL, fg=MUTED,
                 font=("Courier New", 9), width=14, anchor="w").pack(side="left")
        self.canvas = tk.Canvas(self, width=200, height=14,
                                bg=BORDER, highlightthickness=0)
        self.canvas.pack(side="left", padx=6)
        self.val_label = tk.Label(self, text=" 0.000", bg=PANEL, fg=TEXT,
                                  font=("Courier New", 9), width=7)
        self.val_label.pack(side="left")
        self.canvas.create_line(100, 0, 100, 14, fill=MUTED, width=1)
        self.bar = self.canvas.create_rectangle(100, 2, 100, 12,
                                                fill=ACCENT, outline="")

    def set(self, value: float):
        value = max(-1.0, min(1.0, value))
        cx, px = 100, 100 + int(value * 98)
        x0, x1 = sorted([cx, px])
        if x0 == x1:
            x1 += 1
        self.canvas.coords(self.bar, x0, 2, x1, 12)
        self.val_label.config(text=f"{value:+.3f}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Controller Monitor")
        self.configure(bg=BG)
        self.resizable(False, False)

        pygame.init()
        pygame.joystick.init()

        self.joystick   = None
        self.axis_bars  = {}
        self.btn_labels = {}
        self.hat_labels = {}

        self._build_waiting_screen()
        self._poll()

    def _init_joystick(self):
        js = pygame.joystick.Joystick(0)
        js.init()
        self.joystick = js

    # ── Waiting screen ────────────────────────────────────────────────────────
    def _build_waiting_screen(self):
        self._clear()
        f = tk.Frame(self, bg=BG)
        f.pack(expand=True, fill="both", padx=40, pady=40)
        tk.Label(f, text="🎮", bg=BG, font=("", 48)).pack(pady=(0, 12))
        tk.Label(f, text="Waiting for controller…",
                 bg=BG, fg=MUTED, font=("Courier New", 12)).pack()
        tk.Label(f, text="No controller detected",
                 bg=BG, fg=RED, font=("Courier New", 9)).pack(pady=6)

    # ── Controller UI ─────────────────────────────────────────────────────────
    def _build_controller_ui(self):
        self._clear()
        js = self.joystick

        # Header
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(hdr, text=f"🎮  {js.get_name()}",
                 bg=BG, fg=ACCENT, font=("Courier New", 11, "bold")).pack(side="left")
        tk.Label(hdr, text="● CONNECTED",
                 bg=BG, fg=GREEN, font=("Courier New", 9)).pack(side="right")

        # Axes
        if js.get_numaxes() > 0:
            axes_frame = tk.LabelFrame(self, text="  AXES  ", bg=PANEL, fg=ACCENT,
                                       font=("Courier New", 9, "bold"),
                                       bd=1, highlightthickness=1,
                                       highlightbackground=BORDER)
            axes_frame.pack(fill="x", padx=12, pady=6, ipadx=8, ipady=6)
            self.axis_bars = {}
            for i in range(js.get_numaxes()):
                bar = AxisBar(axes_frame, f"Axis {i}")
                bar.pack(anchor="w", pady=1)
                self.axis_bars[i] = bar

        # Buttons
        if js.get_numbuttons() > 0:
            btn_frame = tk.LabelFrame(self, text="  BUTTONS  ", bg=PANEL, fg=ACCENT,
                                      font=("Courier New", 9, "bold"),
                                      bd=1, highlightthickness=1,
                                      highlightbackground=BORDER)
            btn_frame.pack(fill="x", padx=12, pady=6, ipadx=8, ipady=6)
            self.btn_labels = {}
            row = tk.Frame(btn_frame, bg=PANEL)
            row.pack()
            for i in range(js.get_numbuttons()):
                lbl = tk.Label(row, text=str(i), bg=BORDER, fg=MUTED,
                               font=("Courier New", 8), width=3,
                               relief="flat", padx=2, pady=3)
                lbl.pack(side="left", padx=2, pady=2)
                self.btn_labels[i] = lbl

        # Hats (D-pad)
        if js.get_numhats() > 0:
            hat_frame = tk.LabelFrame(self, text="  HATS / D-PAD  ", bg=PANEL, fg=ACCENT,
                                      font=("Courier New", 9, "bold"),
                                      bd=1, highlightthickness=1,
                                      highlightbackground=BORDER)
            hat_frame.pack(fill="x", padx=12, pady=6, ipadx=8, ipady=6)
            self.hat_labels = {}
            row = tk.Frame(hat_frame, bg=PANEL)
            row.pack()
            for i in range(js.get_numhats()):
                lbl = tk.Label(row, text=f"Hat {i}: (0, 0)",
                               bg=PANEL, fg=TEXT, font=("Courier New", 9))
                lbl.pack(side="left", padx=8)
                self.hat_labels[i] = lbl

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ── Poll loop ─────────────────────────────────────────────────────────────
    def _poll(self):
        # Drain the full event queue — required for pygame to update button/axis state
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                self._init_joystick()
                self._build_controller_ui()
            elif event.type == pygame.JOYDEVICEREMOVED:
                self.joystick   = None
                self.axis_bars  = {}
                self.btn_labels = {}
                self.hat_labels = {}
                self._build_waiting_screen()

        # Catch controllers already plugged in at startup
        if self.joystick is None and pygame.joystick.get_count() > 0:
            self._init_joystick()
            self._build_controller_ui()

        # Read live state
        if self.joystick is not None:
            try:
                for i, bar in self.axis_bars.items():
                    bar.set(self.joystick.get_axis(i))
                for i, lbl in self.btn_labels.items():
                    pressed = self.joystick.get_button(i)
                    lbl.config(bg=ACCENT if pressed else BORDER,
                               fg=BG    if pressed else MUTED)
                for i, lbl in self.hat_labels.items():
                    lbl.config(text=f"Hat {i}: {self.joystick.get_hat(i)}")
            except pygame.error:
                self.joystick = None
                self._build_waiting_screen()

        self.after(POLL_MS, self._poll)


if __name__ == "__main__":
    App().mainloop()

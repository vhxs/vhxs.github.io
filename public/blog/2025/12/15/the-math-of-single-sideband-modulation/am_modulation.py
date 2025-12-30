import numpy as np
import matplotlib.pyplot as plt

# ----- Parameters -----
fs = 1000        # sampling rate (Hz)
fc = 10          # carrier frequency (Hz)
fm = 1           # modulating frequency (Hz)
m = 0.8          # modulation index
duration = 3.0   # seconds

# ----- Time axis -----
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# ----- Signals -----
carrier = np.sin(2 * np.pi * fc * t)
envelope = 1 + m * np.sin(2 * np.pi * fm * t)
am_signal = envelope * carrier

# ----- Plot -----
plt.figure(figsize=(12, 4))

# Unmodulated carrier
plt.subplot(1, 2, 1)
plt.plot(t, carrier, color="red")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("10 Hz Unmodulated Carrier")
plt.gca().set_facecolor((1.0, 0.9, 0.9))

# AM signal with envelope
plt.subplot(1, 2, 2)
plt.plot(t, am_signal, color="red")
plt.plot(t, envelope, color="purple", linewidth=2)
plt.plot(t, -envelope, color="purple", linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("10 Hz Carrier AM by 1 Hz Signal")
plt.gca().set_facecolor((1.0, 0.9, 0.9))

plt.tight_layout()
plt.show()


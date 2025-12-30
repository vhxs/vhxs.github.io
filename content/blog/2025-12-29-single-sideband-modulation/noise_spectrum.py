import numpy as np
import matplotlib.pyplot as plt

# ----- Parameters -----
fs = 1000          # sampling rate (Hz)
fc = 40            # carrier frequency (Hz)
m = 0.9            # modulation index (0 < m <= 1)
duration = 3.0     # seconds

# ----- Time-domain signal -----
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

carrier = np.cos(2 * np.pi * fc * t)

# ----------------------------------------------------------
# Build a more complex real-valued modulating waveform
# ----------------------------------------------------------
rng = np.random.default_rng(0)

base_freqs = np.array([1.3, 2.1, 3.7, 5.2, 7.9, 11.0])
phases = rng.uniform(0, 2 * np.pi, size=len(base_freqs))
amps = np.array([1.0, 0.8, 0.6, 0.45, 0.3, 0.2])

message = np.zeros_like(t)
for a, f, p in zip(amps, base_freqs, phases):
    wobble = 0.03 * np.sin(2 * np.pi * 0.25 * t + 1.7 * p)
    message += a * np.sin(2 * np.pi * (f + wobble) * t + p)

# Slow envelope variation
slow_env = 0.6 + 0.4 * np.sin(2 * np.pi * 0.35 * t) * np.sin(2 * np.pi * 0.12 * t + 0.8)
message *= slow_env

# Normalize message to [-1, 1]
message /= np.max(np.abs(message))

# AM signal
modulator = 1 + m * message
x = modulator * carrier

# ----- Fourier transform -----
X = np.fft.fft(x)
freqs = np.fft.fftfreq(len(X), d=1 / fs)

# ----- Plot -----
plt.figure(figsize=(16, 4))

# 1) Modulating signal
plt.subplot(1, 3, 1)
plt.plot(t, message, color="red")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Modulating Signal (Baseband)")
plt.gca().set_facecolor((1.0, 0.9, 0.9))

# 2) AM signal in time
plt.subplot(1, 3, 2)
plt.plot(t, x, color="red")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("AM Signal")
plt.gca().set_facecolor((1.0, 0.9, 0.9))

# 3) Frequency domain
plt.subplot(1, 3, 3)
plt.plot(freqs, np.abs(X), color="red")
plt.xlim(-50, 50)
plt.ylim(0, 300)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.title("AM Spectrum")
plt.gca().set_facecolor((1.0, 0.9, 0.9))

plt.tight_layout()
plt.show()


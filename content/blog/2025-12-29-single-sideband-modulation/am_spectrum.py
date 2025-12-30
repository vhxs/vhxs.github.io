import numpy as np
import matplotlib.pyplot as plt

# ----- Parameters -----
fs = 1000          # sampling rate (Hz)
fc = 40           # carrier frequency (Hz)
fm = 2             # modulation frequency (Hz)
m = 0.9            # modulation index (0 < m <= 1)
duration = 3.0     # seconds

# ----- Time-domain signal -----
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

carrier = np.cos(2 * np.pi * fc * t)
modulator = 1 + m * np.cos(2 * np.pi * fm * t)
x = modulator * carrier

# ----- Fourier transform -----
X = np.fft.fft(x)
freqs = np.fft.fftfreq(len(X), d=1/fs)

# ----- Plot -----
plt.figure(figsize=(12, 4))

# Time domain
plt.subplot(1, 2, 1)
plt.plot(t, x, color="red")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.title("Amplitude Modulation of 40Hz by 1Hz wave")
plt.gca().set_facecolor((1.0, 0.9, 0.9))

# Frequency domain (unshifted)
plt.subplot(1, 2, 2)
plt.plot(freqs, np.abs(X), color="red")
plt.xlim(-50, 50)
plt.xlabel("Frequency")
plt.ylabel("Magnitude")
plt.title("AM Spectrum")
plt.gca().set_facecolor((1.0, 0.9, 0.9))

plt.tight_layout()
plt.show()


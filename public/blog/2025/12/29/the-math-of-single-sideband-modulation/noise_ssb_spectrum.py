import numpy as np
import matplotlib.pyplot as plt

# ----- Parameters -----
fs = 1000
fc = 40
m = 0.9
duration = 3.0

# ----- Time-domain signal -----
t = np.linspace(0, duration, int(fs * duration), endpoint=False)
carrier = np.cos(2 * np.pi * fc * t)

# ----- Complex modulating waveform -----
rng = np.random.default_rng(0)

base_freqs = np.array([1.3, 2.1, 3.7, 5.2, 7.9, 11.0])
phases = rng.uniform(0, 2 * np.pi, size=len(base_freqs))
amps = np.array([1.0, 0.8, 0.6, 0.45, 0.3, 0.2])

message = np.zeros_like(t)
for a, f, p in zip(amps, base_freqs, phases):
    wobble = 0.03 * np.sin(2 * np.pi * 0.25 * t + 1.7 * p)
    message += a * np.sin(2 * np.pi * (f + wobble) * t + p)

slow_env = 0.6 + 0.4 * np.sin(2 * np.pi * 0.35 * t) * np.sin(2 * np.pi * 0.12 * t + 0.8)
message *= slow_env
message /= np.max(np.abs(message))

# ----- Suppressed-carrier AM (DSB-SC) -----
x = m * message * carrier

# ----- Fourier transform -----
X = np.fft.fft(x)
freqs = np.fft.fftfreq(len(X), d=1 / fs)
mag = np.abs(X)

# ----- Sideband masks -----
B = float(np.max(base_freqs))

usb = ((freqs >= fc) & (freqs <= fc + B)) | ((freqs <= -fc) & (freqs >= -(fc + B)))
lsb = ((freqs >= fc - B) & (freqs <= fc)) | ((freqs <= -(fc - B)) & (freqs >= -fc))

# ----- Helper: sort + break lines across gaps by inserting NaNs -----
df = fs / len(freqs)

def sorted_xy_with_gaps(mask, gap_bins=1.5):
    x = freqs[mask]
    y = mag[mask]
    order = np.argsort(x)
    x = x[order]
    y = y[order]

    dx = np.diff(x)
    gap = dx > (gap_bins * df)

    if np.any(gap):
        idx = np.where(gap)[0] + 1
        x = np.insert(x, idx, np.nan)
        y = np.insert(y, idx, np.nan)

    return x, y

f_usb, m_usb = sorted_xy_with_gaps(usb)
f_lsb, m_lsb = sorted_xy_with_gaps(lsb)

# ----- Plot -----
plt.figure(figsize=(10, 4))
plt.plot(f_usb, m_usb, color="red", linewidth=1.5, label="Upper sideband")
plt.plot(f_lsb, m_lsb, color="blue", linewidth=1.5, label="Lower sideband")

plt.xlim(-(fc + B + 2), fc + B + 2)
plt.ylim(0, 300)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("Spectrum (No Carrier; Blue is Lower Sideband, and Red is Upper)")
plt.legend()
plt.gca().set_facecolor((1.0, 0.9, 0.9))
plt.tight_layout()
plt.show()


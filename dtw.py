import numpy as np
import matplotlib.pyplot as plt
from dtw import *

# Generate sample data
np.random.seed(42)
t = np.linspace(0, 2*np.pi, 100)
x = np.sin(t)  # Reference sequence
y = np.sin(t + 0.5) + 0.1 * np.random.randn(100)  # Sequence to be aligned

# Perform DTW alignment
alignment = dtw(x, y, keep_internals=True)

# Create aligned version of y using the warping path
y_aligned = np.zeros_like(x)
for idx_x, idx_y in zip(alignment.index1, alignment.index2):
    y_aligned[idx_x] = y[idx_y]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t, x, 'b-', label='Reference (x)', linewidth=2)
plt.plot(t, y, 'r--', label='Original y', alpha=0.5)
plt.plot(t, y_aligned, 'g-', label='Aligned y', linewidth=2)
plt.title('DTW Sequence Alignment')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Print alignment quality metric
print(f"DTW distance: {alignment.distance:.4f}")

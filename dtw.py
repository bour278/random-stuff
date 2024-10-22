import numpy as np
import matplotlib.pyplot as plt
from dtw import *

# Generate sample data
np.random.seed(42)
t = np.linspace(0, 2*np.pi, 100)
x = np.sin(t)  # Fixed reference sequence
y = np.sin(t + 0.5) + 0.1 * np.random.randn(100)  # Sequence to be aligned

def analyze_dtw_path(x, y):
    """
    Analyze and visualize DTW path between two sequences using dtw-python.
    
    Parameters:
        x (array): Reference sequence
        y (array): Sequence to be aligned
    """
    # Calculate DTW alignment
    alignment = dtw(x, y, keep_internals=True)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Original sequences with matching points
    ax1.plot(t, x, 'b-', label='Reference (x)', linewidth=2)
    ax1.plot(t, y, 'r-', label='Target (y)', linewidth=2)
    ax1.set_title('Sequences with DTW Matching Points')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid(True)
    
    # Draw matching lines between sequences
    for idx_x, idx_y in zip(alignment.index1, alignment.index2):
        ax1.plot([t[idx_x], t[idx_y]], [x[idx_x], y[idx_y]], 
                 'g-', alpha=0.3, linewidth=0.5)
    
    # Plot 2: DTW distance matrix and optimal path
    im = ax2.imshow(alignment.costMatrix, 
                    origin='lower', 
                    cmap='YlGnBu',
                    aspect='auto')
    
    # Plot optimal path
    path_x = alignment.index2
    path_y = alignment.index1
    ax2.plot(path_x, path_y, 'r-', linewidth=2, label='Optimal path')
    
    ax2.set_title('DTW Cost Matrix and Optimal Path')
    ax2.set_xlabel('Target Index')
    ax2.set_ylabel('Reference Index')
    plt.colorbar(im, ax=ax2, label='Cost')
    ax2.legend()
    
    plt.tight_layout()
    return fig, alignment

# Run the analysis
fig, alignment = analyze_dtw_path(x, y)

# Print alignment statistics
print(f"DTW distance: {alignment.distance:.4f}")
print(f"Normalized distance: {alignment.normalizedDistance:.4f}")
print(f"Number of steps in path: {len(alignment.index1)}")

# Additional analysis of the warping
step_pattern = alignment.stepPattern
print("\nStep pattern type:", step_pattern.hint)
print("Step pattern symmetry:", step_pattern.symmetry)

# Compute and display path characteristics
path_length = len(alignment.index1)
diagonal_moves = sum(1 for i in range(path_length-1) 
                    if (alignment.index1[i+1] - alignment.index1[i] == 1 and 
                        alignment.index2[i+1] - alignment.index2[i] == 1))
print(f"\nDiagonal moves: {diagonal_moves}")
print(f"Diagonal percentage: {(diagonal_moves/path_length)*100:.2f}%")

# Save the visualization
plt.savefig('dtw_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

import numpy as np
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(42)
t = np.linspace(0, 2*np.pi, 100)
x = np.sin(t)  # Fixed reference sequence
y = np.sin(t + 0.5) + 0.1 * np.random.randn(100)  # Sequence to be aligned

def analyze_dtw_path(x, y):
    """
    Analyze and visualize DTW path between two sequences.
    
    Parameters:
        x (array): Reference sequence
        y (array): Sequence to be aligned
    """
    # Calculate DTW distance matrix and optimal path
    d = dtw.distance_matrix_fast(np.array([x, y]))
    path = dtw.warping_paths(x, y)
    best_path = dtw.best_path(path)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    
    # Plot original sequences
    ax1.plot(t, x, 'b-', label='Reference (x)')
    ax1.plot(t, y, 'r-', label='Target (y)')
    ax1.set_title('Original Sequences')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid(True)
    
    # Visualize DTW path
    dtwvis.plot_warpingpaths(x, y, path, best_path, ax=ax2)
    ax2.set_title('DTW Warping Path')
    
    # Add connecting lines between matched points
    for idx_x, idx_y in best_path:
        ax1.plot([t[idx_x], t[idx_y]], [x[idx_x], y[idx_y]], 
                 'g-', alpha=0.3, linewidth=0.5)
    
    plt.tight_layout()
    return fig, path, best_path

# Run the analysis
fig, path, best_path = analyze_dtw_path(x, y)

# Print some statistics
dtw_distance = path[best_path[-1][0], best_path[-1][1]]
print(f"DTW distance: {dtw_distance:.4f}")
print(f"Number of path steps: {len(best_path)}")

# Save the visualization
plt.savefig('dtw_analysis.png')
plt.close()

import numpy as np
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt

def generate_samples(n_samples=1000000):
    """Generate samples from standard normal distribution"""
    X = np.random.standard_normal(n_samples)
    Y = np.random.standard_normal(n_samples)
    return X, Y

def compute_condition(X, Y):
    """Compute (X-1)^2 + Y^2"""
    return (X - 1)**2 + Y**2

def estimate_conditional_expectation(n_samples=1000000, n_bins=100):
    """
    Estimate E[X|(X-1)^2 + Y^2] using kernel density estimation
    """
    # Generate samples
    X, Y = generate_samples(n_samples)
    
    # Compute condition values
    condition_values = compute_condition(X, Y)
    
    # Sort everything by condition values
    sorted_indices = np.argsort(condition_values)
    condition_values = condition_values[sorted_indices]
    X = X[sorted_indices]
    
    # Use kernel density estimation
    kernel = gaussian_kde(np.vstack([condition_values, X]))
    
    # Create grid for evaluation
    grid_points = np.linspace(np.min(condition_values), np.percentile(condition_values, 95), n_bins)
    
    # Estimate conditional expectation
    conditional_expectations = []
    for z in grid_points:
        # Create points for evaluation
        eval_points = np.vstack([np.full_like(X, z), X])
        # Compute conditional density
        density = kernel(eval_points)
        # Compute conditional expectation
        conditional_expectation = np.sum(X * density) / np.sum(density)
        conditional_expectations.append(conditional_expectation)
    
    return grid_points, conditional_expectations

def plot_results(grid_points, conditional_expectations):
    """Plot the estimated conditional expectation"""
    plt.figure(figsize=(10, 6))
    plt.plot(grid_points, conditional_expectations, 'b-', label='E[X|(X-1)^2 + Y^2]')
    plt.xlabel('(X-1)^2 + Y^2')
    plt.ylabel('Conditional Expectation')
    plt.title('Estimated Conditional Expectation')
    plt.grid(True)
    plt.legend()
    plt.show()

# Run simulation
grid_points, conditional_expectations = estimate_conditional_expectation()

# Plot results
plot_results(grid_points, conditional_expectations)

# Print some specific values
print("\nSome specific conditional expectations:")
for i in range(0, len(grid_points), len(grid_points)//5):
    print(f"E[X|(X-1)^2 + Y^2 = {grid_points[i]:.2f}] ≈ {conditional_expectations[i]:.4f}")

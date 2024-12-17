import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from numba import jit, float64
import time
from typing import Optional, Tuple, List
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize default session state
def init_session_state():
    defaults = {
        # Model Parameters
        'mu0': 0.0,
        'mu1': 2.0,
        'sigma': 1.0,
        'threshold': 100.0,
        
        # Prior Parameters
        'alpha': 0.1,
        'rho': 0.1,
        'pi': 0.1,
        
        # Simulation Parameters
        'change_point': 100,
        'update_interval': 0.1,
        'running': False,
        
        # Display Parameters
        'window_size': 200,
        'plot_height': 800
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

@dataclass
class SRParameters:
    """Parameters for the Shiryaev-Roberts procedure"""
    alpha: float
    rho: float
    pi: float
    mu0: float
    mu1: float
    sigma: float

@jit(float64(float64, float64, float64, float64), nopython=True)
def likelihood_ratio(x: float, mu0: float, mu1: float, sigma: float) -> float:
    """Compute likelihood ratio for normal distributions"""
    return np.exp((-(x - mu1)**2 + (x - mu0)**2) / (2 * sigma**2))

class ShiryaevRobertsDetector:
    def __init__(self, params: SRParameters, threshold: float):
        self.params = params
        self.threshold = threshold
        
        # Initialize statistics
        self.R = 0.0
        self.observations: List[float] = []
        self.Rs: List[float] = []
        self.detections: List[bool] = []
        self.pis: List[float] = []
        self.times: List[int] = []
        
    def update(self, x: float, t: int) -> Tuple[float, bool, float]:
        """Update detector with new observation"""
        self.observations.append(x)
        self.times.append(t)
        
        # Compute likelihood ratio
        lr = likelihood_ratio(
            x, 
            self.params.mu0, 
            self.params.mu1, 
            self.params.sigma
        )
        
        # Update SR statistic recursively
        self.R = (1 + self.R) * lr
        self.Rs.append(self.R)
        
        # Compute posterior probability
        pi = self.R / (1 + self.R)
        self.pis.append(pi)
        
        # Check for detection
        detection = self.R >= self.threshold
        self.detections.append(detection)
        
        if detection:
            self.R = 0  # Reset after detection
            
        return self.R, detection, pi

def create_detector_plot(detector):
    """Create plotly figure for detector state"""
    fig = make_subplots(
        rows=3, cols=1, 
        subplot_titles=(
            'Data Stream with Change Detection',
            'Shiryaev-Roberts Statistic',
            'Posterior Probability of Change'
        )
    )
    
    # Data stream plot
    fig.add_trace(
        go.Scatter(x=detector.times, y=detector.observations, 
                  name='Observations', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Add detection points
    detections = np.where(detector.detections)[0]
    if len(detections) > 0:
        fig.add_trace(
            go.Scatter(
                x=[detector.times[i] for i in detections],
                y=[detector.observations[i] for i in detections],
                mode='markers',
                name='Detections',
                marker=dict(color='red', symbol='triangle-up', size=10)
            ),
            row=1, col=1
        )
    
    # SR statistic plot
    fig.add_trace(
        go.Scatter(x=detector.times, y=detector.Rs, 
                  name='SR Statistic', line=dict(color='green')),
        row=2, col=1
    )
    fig.add_hline(y=detector.threshold, line_dash="dash", 
                  line_color="red", name="Threshold",
                  row=2, col=1)
    
    # Posterior probability plot
    fig.add_trace(
        go.Scatter(x=detector.times, y=detector.pis, 
                  name='Posterior π', line=dict(color='blue')),
        row=3, col=1
    )
    
    # Update layout
    fig.update_layout(
        height=st.session_state.plot_height, 
        showlegend=True,
        title_text="Shiryaev-Roberts Change Detection Monitor"
    )
    fig.update_yaxes(range=[-5, 5], row=1, col=1, title_text="Value")
    fig.update_yaxes(range=[0, detector.threshold*1.2], row=2, col=1, title_text="SR Statistic")
    fig.update_yaxes(range=[0, 1], row=3, col=1, title_text="Probability")
    fig.update_xaxes(title_text="Time", row=3, col=1)
    
    return fig

def main():
    st.set_page_config(layout="wide", page_title="SR Change Detection")
    
    # Initialize session state
    init_session_state()
    
    # Title and description
    st.title("Shiryaev-Roberts Change Detection Monitor")
    st.markdown("""
    This application demonstrates real-time change detection using the Shiryaev-Roberts procedure.
    Adjust the parameters in the sidebar to experiment with different settings.
    """)
    
    # Sidebar configuration
    st.sidebar.title("Configuration")
    
    # Model Parameters section
    st.sidebar.header("📊 Model Parameters")
    with st.sidebar.expander("Distribution Parameters", expanded=True):
        st.session_state.mu0 = st.number_input(
            "Pre-change mean (μ₀)", 
            value=st.session_state.mu0,
            help="Mean value before the change"
        )
        st.session_state.mu1 = st.number_input(
            "Post-change mean (μ₁)", 
            value=st.session_state.mu1,
            help="Mean value after the change"
        )
        st.session_state.sigma = st.number_input(
            "Standard deviation (σ)", 
            value=st.session_state.sigma,
            min_value=0.1,
            help="Standard deviation of the observations"
        )
    
    # Detection Parameters
    with st.sidebar.expander("Detection Parameters", expanded=True):
        st.session_state.threshold = st.number_input(
            "Detection threshold (A)", 
            value=st.session_state.threshold,
            min_value=1.0,
            help="Threshold for declaring a change"
        )
        st.session_state.change_point = st.number_input(
            "Change Point", 
            value=st.session_state.change_point,
            min_value=1,
            help="Time at which the change occurs"
        )
    
    # Prior Parameters
    st.sidebar.header("🎲 Prior Parameters")
    with st.sidebar.expander("Prior Distribution", expanded=False):
        st.session_state.alpha = st.number_input(
            "Alpha (α)", 
            value=st.session_state.alpha,
            min_value=0.0,
            max_value=1.0,
            help="Parameter for geometric prior"
        )
        st.session_state.rho = st.number_input(
            "Rho (ρ)", 
            value=st.session_state.rho,
            min_value=0.0,
            max_value=1.0,
            help="Conditional probability"
        )
        st.session_state.pi = st.number_input(
            "Pi (π)", 
            value=st.session_state.pi,
            min_value=0.0,
            max_value=1.0,
            help="Initial probability"
        )
    
    # Display Parameters
    st.sidebar.header("🎯 Display Settings")
    with st.sidebar.expander("Visualization", expanded=False):
        st.session_state.window_size = st.number_input(
            "Window Size", 
            value=st.session_state.window_size,
            min_value=50,
            help="Number of observations to display"
        )
        st.session_state.update_interval = st.slider(
            "Update Interval", 
            min_value=0.01,
            max_value=1.0,
            value=st.session_state.update_interval,
            help="Time between updates (seconds)"
        )
    
    # Initialize detector
    params = SRParameters(
        alpha=st.session_state.alpha,
        rho=st.session_state.rho,
        pi=st.session_state.pi,
        mu0=st.session_state.mu0,
        mu1=st.session_state.mu1,
        sigma=st.session_state.sigma
    )
    
    if 'detector' not in st.session_state:
        st.session_state.detector = ShiryaevRobertsDetector(params, st.session_state.threshold)
    
    # Create placeholders for plots and stats
    plot_placeholder = st.empty()
    stats_placeholder = st.empty()
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('▶️ Start/Stop'):
            st.session_state.running = not st.session_state.running
    with col2:
        if st.button('🔄 Reset'):
            st.session_state.running = False
            st.session_state.detector = ShiryaevRobertsDetector(params, st.session_state.threshold)
    with col3:
        if st.button('❓ Help'):
            st.info("""
            **How to use:**
            1. Adjust parameters in the sidebar
            2. Click Start to begin monitoring
            3. Watch for change detections
            4. Click Reset to start over
            """)
    
    # Main simulation loop
    while st.session_state.running:
        t = len(st.session_state.detector.observations)
        
        # Generate observation
        if t < st.session_state.change_point:
            x = np.random.normal(st.session_state.mu0, st.session_state.sigma)
        else:
            x = np.random.normal(st.session_state.mu1, st.session_state.sigma)
            
        # Update detector
        R, detection, pi = st.session_state.detector.update(x, t)
        
        # Update plot
        fig = create_detector_plot(st.session_state.detector)
        plot_placeholder.plotly_chart(fig, use_container_width=True)
        
        # Update stats
        stats = f"""
        ### Current Statistics
        - **Time**: {t}
        - **SR Statistic**: {R:.2f}
        - **Posterior Probability**: {pi:.2f}
        - **Total Detections**: {sum(st.session_state.detector.detections)}
        """
        stats_placeholder.markdown(stats)
        
        if detection:
            st.warning(f"🚨 Change detected at time {t}!")
        
        time.sleep(st.session_state.update_interval)

if __name__ == "__main__":
    main()

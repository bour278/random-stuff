import streamlit as st
import time
import random
import numpy as np
import matplotlib.pyplot as plt

def generate_loading_animation():
    animations = [
        "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏",
        "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁",
        "🌑🌒🌓🌔🌕🌖🌗🌘"
    ]
    return random.choice(animations)

def create_ascii_stadium():
    stadium = """
    🏟️  MOLINEUX STADIUM  🏟️
         ___________
        /           \\
       /             \\
      /               \\
     /                 \\
    |                   |
    |    🐺  vs  😈    |
    |                   |
    |    WOLVES v MUN   |
    |___________________|
    """
    return stadium

def generate_random_metrics():
    metrics = np.random.rand(10)
    return metrics

def main():
    st.title("Match Prediction Generator 🎮")
    
    # Center the button using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🎲 Run Prediction 🎲", use_container_width=True)

    if predict_button:
        # Display stadium ASCII art
        st.text(create_ascii_stadium())
        
        # Create a loading message placeholder
        loading_placeholder = st.empty()
        metrics_placeholder = st.empty()
        
        # Loading animation
        animation = generate_loading_animation()
        for i in range(15):
            frame = animation[i % len(animation)]
            loading_placeholder.markdown(f"### Computing prediction {frame}")
            
            # Generate and display random metrics
            metrics = generate_random_metrics()
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.plot(metrics, color='purple')
            ax.set_title('Match Analysis in Progress...')
            ax.grid(True)
            metrics_placeholder.pyplot(fig)
            plt.close()
            
            time.sleep(0.3)
        
        # Clear the loading animations
        loading_placeholder.empty()
        metrics_placeholder.empty()
        
        # Display final prediction with emojis and styling
        st.markdown("""
        <div style='background-color: #fdba74; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #1e293b;'>
                🐺 Wolves 2 - 0 Man Utd 😈
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Display some fun stats
        st.markdown("### Match Statistics 📊")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Possession", "55%", "🐺")
            st.metric("Shots on Target", "6", "↗️")
        with col2:
            st.metric("Expected Goals", "2.3", "📈")
            st.metric("Clean Sheet Probability", "75%", "🧤")

if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Match Prediction",
        page_icon="⚽",
        layout="wide"
    )
    main()

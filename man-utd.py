import streamlit as st
import time
import random
import numpy as np
import matplotlib.pyplot as plt

def generate_loading_animation():
    animations = [
        "🌑 🌒 🌓 🌔 🌕 🌖 🌗 🌘",
        "⚡ 🌟 ✨ 💫 ⭐ 🌟 ✨ 💫",
        "🎲 🎮 🎯 🎲 🎮 🎯",
        "🔮 ✨ 💫 🔮 ✨ 💫"
    ]
    return random.choice(animations).split()

def main():
    # Hide default menu and footer
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Add vertical space to center button
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    
    # Center the button using columns
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button(
            "Run Prediction",
            use_container_width=True,
            type="primary"  # This makes it blue
        )

    if predict_button:
        # Create placeholders for dynamic content
        loading_placeholder = st.empty()
        metrics_placeholder = st.empty()
        
        # Loading animation
        animation = generate_loading_animation()
        for i in range(12):
            # Generate random numbers for the "computation" effect
            # Mix emojis with numbers for a fun effect
            numbers = ' '.join([str(random.randint(0, 9)) for _ in range(15)])
            emojis = ' '.join(random.sample(['🎲', '🎮', '🎯', '🔮', '✨', '💫', '⭐', '🌟'], 3))
            frame = animation[i % len(animation)]
            
            loading_placeholder.markdown(f"""
            ```
            {frame} Computing prediction... {emojis}
            {numbers}
            ```
            """)
            
            # Generate and plot random data for "analysis"
            metrics = np.random.rand(10) * random.random()
            fig, ax = plt.subplots(figsize=(8, 2))
            ax.plot(metrics, color='blue', alpha=0.7)
            ax.set_xticks([])
            ax.set_yticks([])
            metrics_placeholder.pyplot(fig)
            plt.close()
            
            time.sleep(0.3)
        
        # Clear the loading animations
        loading_placeholder.empty()
        metrics_placeholder.empty()
        
        # Display final prediction with emojis and styling
        st.markdown("""
        <div style='background-color: #fbbf24; padding: 20px; border-radius: 10px; text-align: center;'>
            <h2 style='color: #1e293b; font-family: monospace;'>
                🐺 Wolves 2 - 0 Man Utd 😈
            </h2>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Set minimal page configuration
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()

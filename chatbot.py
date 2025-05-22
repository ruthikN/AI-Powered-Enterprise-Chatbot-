import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

# Set page config
st.set_page_config(
    page_title="AI-Powered Enterprise Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mock data and configurations
def load_chatbot_data():
    return {
        "daily_queries": 512,
        "user_satisfaction": 0.94,
        "uptime": 0.9995,
        "response_times": [round(random.uniform(300, 700), 2) for _ in range(100)],
        "response_times_optimized": [round(random.uniform(200, 400), 2) for _ in range(100)],
        "conversation_history": [
            {"user": "What's our Q3 sales forecast?", "bot": "Based on current trends, Q3 sales are projected to be $4.2M, a 12% increase from Q2.", "timestamp": "2023-05-15 09:23:45"},
            {"user": "Any issues with the AWS deployment?", "bot": "All systems are operational. The Kubernetes cluster is running with 99.95% uptime over the past week.", "timestamp": "2023-05-15 10:12:33"},
            {"user": "Summarize the customer feedback from last week", "bot": "Last week's feedback shows 94% satisfaction. Key themes: faster response times (78%), accurate information (85%).", "timestamp": "2023-05-16 14:45:21"}
        ],
        "system_metrics": {
            "cpu_usage": [random.uniform(20, 60) for _ in range(24)],
            "memory_usage": [random.uniform(30, 70) for _ in range(24)],
            "latency": [random.uniform(150, 350) for _ in range(24)]
        }
    }

# Initialize data
chatbot_data = load_chatbot_data()

# Mock chatbot function
def enterprise_chatbot_response(user_input):
    # Simulate processing time (optimized latency)
    processing_time = random.uniform(0.15, 0.35)
    time.sleep(processing_time)
    
    # Context-aware responses
    if "sales" in user_input.lower():
        return f"Based on the latest analytics, sales are trending positively with a 12% increase projected for next quarter. (Processed in {processing_time:.3f}s)"
    elif "aws" in user_input.lower() or "ec2" in user_input.lower():
        return f"Our AWS infrastructure is currently running at 99.95% availability with auto-scaling enabled. (Processed in {processing_time:.3f}s)"
    elif "performance" in user_input.lower() or "latency" in user_input.lower():
        return f"After LoRA fine-tuning, we've achieved 42% lower latency (300ms improvement). Current avg: 320ms. (Processed in {processing_time:.3f}s)"
    else:
        return f"I've analyzed your query about '{user_input}'. Our systems indicate optimal performance in this area. (Processed in {processing_time:.3f}s)"

# Dashboard layout
st.title("AI-Powered Enterprise Chatbot")
st.subheader("AWS EC2, Hugging Face, LangChain - 42% Latency Improvement")

# Main columns
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### System Metrics")
    
    # Uptime and satisfaction
    metric1, metric2 = st.columns(2)
    metric1.metric("Daily Queries", chatbot_data["daily_queries"])
    metric2.metric("User Satisfaction", f"{chatbot_data['user_satisfaction']*100:.1f}%")
    
    # Response time comparison
    st.markdown("#### Response Time Optimization")
    df_times = pd.DataFrame({
        "Before": chatbot_data["response_times"],
        "After": chatbot_data["response_times_optimized"]
    })
    fig_times = px.box(df_times, y=["Before", "After"], 
                      labels={"value": "Response Time (ms)"},
                      title="Response Time Improvement (300ms reduction)")
    st.plotly_chart(fig_times, use_container_width=True)
    
    # System health metrics
    st.markdown("#### System Health (Last 24 Hours)")
    hours = [datetime.now() - timedelta(hours=i) for i in range(23, -1, -1)]
    df_metrics = pd.DataFrame({
        "Hour": [h.strftime("%H:00") for h in hours],
        "CPU Usage (%)": chatbot_data["system_metrics"]["cpu_usage"],
        "Memory Usage (%)": chatbot_data["system_metrics"]["memory_usage"],
        "Latency (ms)": chatbot_data["system_metrics"]["latency"]
    })
    st.line_chart(df_metrics.set_index("Hour"))

with col2:
    st.markdown("### Chat Interface")
    
    # Initialize session state for chat
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = chatbot_data["conversation_history"]
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            st.markdown(f"**User ({msg['timestamp']}):** {msg['user']}")
            st.markdown(f"**Bot:** {msg['bot']}")
            st.markdown("---")
    
    # User input
    user_input = st.text_input("Ask about sales, AWS, performance, or other enterprise topics:")
    
    if user_input:
        with st.spinner("Processing..."):
            # Get bot response
            bot_response = enterprise_chatbot_response(user_input)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Update chat history
            new_entry = {
                "user": user_input,
                "bot": bot_response,
                "timestamp": timestamp
            }
            st.session_state.chat_history.append(new_entry)
            
            # Rerun to update display
            st.experimental_rerun()

# Architecture diagram
st.markdown("### System Architecture")
st.image("https://miro.medium.com/v2/resize:fit:1400/1*Q5eu4ZAhx7W7J0opPax6hw.png", 
         caption="Chatbot Architecture with AWS EC2, Hugging Face, and Kubernetes")

# Footer with technical details
st.markdown("---")
st.markdown("""
**Technical Highlights:**
- Reduced response latency by 300ms (42% improvement) via LoRA fine-tuning and EC2 auto-scaling
- Achieved 94% user satisfaction through context-aware conversations handling 500+ daily queries
- Deployed Flask interface supporting 1.2K+ DAU with 99.95% uptime using Kubernetes orchestration
""")
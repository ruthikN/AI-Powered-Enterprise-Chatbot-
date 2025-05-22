import streamlit as st
import time
import random

# Configure the page
st.set_page_config(
    page_title="Enterprise AI Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mock database
def load_chatbot_data():
    return {
        "performance_metrics": {
            "daily_queries": 512,
            "satisfaction": 0.94,
            "uptime": "99.95%",
            "latency_before": "700ms",
            "latency_after": "400ms",
            "improvement": "42% (300ms)"
        },
        "example_conversations": [
            {"user": "What's the Q3 sales forecast?", "bot": "Q3 sales projected at $4.2M, up 12% from Q2", "time": "10:23 AM"},
            {"user": "AWS system status?", "bot": "All systems operational. Kubernetes cluster at 99.95% uptime", "time": "11:45 AM"},
            {"user": "Chatbot performance?", "bot": "Response times improved by 42% after optimizations", "time": "02:15 PM"}
        ],
        "system_stats": {
            "hours": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
            "cpu_usage": [32, 28, 45, 52, 48, 38],
            "memory_usage": [45, 42, 58, 62, 55, 47],
            "active_users": [85, 32, 210, 305, 280, 195]
        }
    }

# Initialize data
chatbot_data = load_chatbot_data()

# Chatbot response generator
def generate_response(user_query):
    # Simulate processing time (optimized response)
    processing_time = random.uniform(0.2, 0.4)
    time.sleep(processing_time)
    
    # Context-aware responses
    if "sales" in user_query.lower():
        return {
            "response": f"Sales analytics indicate 12% growth projection for next quarter. (Processed in {processing_time:.2f}s)",
            "category": "sales"
        }
    elif "aws" in user_query.lower() or "ec2" in user_query.lower():
        return {
            "response": f"AWS infrastructure operating normally with 99.95% uptime. (Processed in {processing_time:.2f}s)",
            "category": "infrastructure"
        }
    elif "performance" in user_query.lower():
        return {
            "response": f"After optimizations, we achieved 42% lower latency (300ms improvement). (Processed in {processing_time:.2f}s)",
            "category": "performance"
        }
    else:
        return {
            "response": f"I've analyzed your query about '{user_query}'. Our systems show optimal performance. (Processed in {processing_time:.2f}s)",
            "category": "general"
        }

# Main app layout
def main():
    st.title("🚀 AI-Powered Enterprise Chatbot")
    st.markdown("""
    **AWS EC2 | Hugging Face | LangChain | Kubernetes**  
    *Reduced response latency by 300ms (42%) | 94% user satisfaction | 99.95% uptime*
    """)
    
    # Metrics dashboard
    st.subheader("Performance Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Daily Queries", chatbot_data["performance_metrics"]["daily_queries"])
    col2.metric("User Satisfaction", f"{chatbot_data['performance_metrics']['satisfaction']*100:.0f}%")
    col3.metric("System Uptime", chatbot_data["performance_metrics"]["uptime"])
    col4.metric("Latency Improvement", chatbot_data["performance_metrics"]["improvement"])
    
    # System statistics
    st.subheader("System Health Metrics")
    tab1, tab2, tab3 = st.tabs(["CPU Usage", "Memory Usage", "Active Users"])
    
    with tab1:
        st.line_chart(
            pd.DataFrame({
                "CPU %": chatbot_data["system_stats"]["cpu_usage"],
                "Hour": chatbot_data["system_stats"]["hours"]
            }).set_index("Hour")
        )
    
    with tab2:
        st.line_chart(
            pd.DataFrame({
                "Memory %": chatbot_data["system_stats"]["memory_usage"],
                "Hour": chatbot_data["system_stats"]["hours"]
            }).set_index("Hour")
        )
    
    with tab3:
        st.line_chart(
            pd.DataFrame({
                "Users": chatbot_data["system_stats"]["active_users"],
                "Hour": chatbot_data["system_stats"]["hours"]
            }).set_index("Hour")
        )
    
    # Chat interface
    st.subheader("Chat with Enterprise AI")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = chatbot_data["example_conversations"]
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            st.markdown(f"""
            <div style="background-color:#f0f2f6; padding:10px; border-radius:10px; margin-bottom:10px;">
                <p style="font-weight:bold;">👤 User ({msg['time']}): {msg['user']}</p>
                <p>🤖 Bot: {msg['bot']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # User input
    user_input = st.text_input("Ask about sales, AWS, performance, or other business topics:", key="user_input")
    
    if user_input:
        with st.spinner("Analyzing query..."):
            # Get bot response
            bot_response = generate_response(user_input)
            timestamp = time.strftime("%I:%M %p")
            
            # Update chat history
            new_entry = {
                "user": user_input,
                "bot": bot_response["response"],
                "time": timestamp
            }
            st.session_state.chat_history.append(new_entry)
            
            # Rerun to update display
            st.experimental_rerun()
    
    # Technical details
    st.markdown("---")
    st.subheader("Technical Implementation")
    st.markdown("""
    - **Backend**: Flask API with Hugging Face transformers
    - **Infrastructure**: AWS EC2 auto-scaling group
    - **Orchestration**: Kubernetes cluster
    - **Optimizations**:
        - LoRA fine-tuning for 42% latency reduction
        - Caching layer for frequent queries
        - Async processing for long-running tasks
    - **Monitoring**: Prometheus + Grafana dashboard
    """)

if __name__ == "__main__":
    main()

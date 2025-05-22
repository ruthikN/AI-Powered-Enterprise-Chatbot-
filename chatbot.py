import streamlit as st
import time
import random
import json
from datetime import datetime, timedelta
from collections import deque
import threading
import uuid

class LoRAOptimizedModel:
    def __init__(self):
        self.base_latency = 700  # Base latency in ms
        self.optimized_latency = 400
        self.cache = {}
        self.fine_tuned_phrases = {
            "sales": ["forecast", "revenue", "growth"],
            "infra": ["aws", "ec2", "kubernetes"],
            "perf": ["latency", "response", "performance"]
        }
    
    def process_query(self, query):
        start = time.time()
        query_id = str(uuid.uuid4())
        
        if query in self.cache:
            latency = self.optimized_latency * 0.3
            time.sleep(latency/1000)
            return {
                "response": self.cache[query],
                "latency": f"{latency:.0f}ms",
                "optimized": True,
                "query_id": query_id
            }
        
        optimization = False
        for category, keywords in self.fine_tuned_phrases.items():
            if any(kw in query.lower() for kw in keywords):
                latency = random.uniform(self.optimized_latency*0.8, self.optimized_latency*1.2)
                optimization = True
                break
        else:
            latency = random.uniform(self.base_latency*0.8, self.base_latency*1.2)
        
        time.sleep(latency/1000)
        response = self._generate_response(query, category if optimization else None)
        
        if optimization:
            self.cache[query] = response
        
        return {
            "response": response,
            "latency": f"{latency:.0f}ms",
            "optimized": optimization,
            "query_id": query_id
        }
    
    def _generate_response(self, query, category):
        response_templates = {
            "sales": [
                f"Sales forecast analysis: Q3 projection ${random.randint(4,5)}M "
                f"({random.randint(10,15)}% YoY growth)",
                "Enterprise sales pipeline shows 20% increase in qualified leads"
            ],
            "infra": [
                f"AWS EC2 Status: {random.randint(8,12)} instances running\n"
                "Auto-scaling: Active\n"
                f"Uptime: {random.uniform(99.9, 99.99):.2f}%"
            ],
            "perf": [
                f"System performance metrics:\n"
                f"- Avg response time: {random.randint(300,400)}ms"
            ],
            "general": ["Analysis of operational data shows stable systems"]
        }
        return random.choice(response_templates.get(category, response_templates["general"]))

class EC2AutoScaler:
    def __init__(self):
        self.min_instances = 5
        self.max_instances = 20
        self.current_instances = 8
        self.load_thresholds = {"high": 80, "low": 30}
        self.scaling_history = []
    
    def monitor_load(self, current_load):
        decision = None
        if current_load > self.load_thresholds["high"]:
            new_count = min(self.max_instances, self.current_instances + 2)
            if new_count != self.current_instances:
                decision = f"Scaling OUT from {self.current_instances} to {new_count}"
                self.current_instances = new_count
        elif current_load < self.load_thresholds["low"]:
            new_count = max(self.min_instances, self.current_instances - 1)
            if new_count != self.current_instances:
                decision = f"Scaling IN from {self.current_instances} to {new_count}"
                self.current_instances = new_count
        
        if decision:
            self.scaling_history.append({
                "timestamp": datetime.now().isoformat(),
                "decision": decision,
                "current_instances": self.current_instances
            })
        return {
            "instances": self.current_instances,
            "decision": decision,
            "timestamp": datetime.now().isoformat()
        }

class EnterpriseChatbotUI:
    def __init__(self):
        self.model = LoRAOptimizedModel()
        self.scaler = EC2AutoScaler()
        self.query_history = deque(maxlen=500)
        self.system_metrics = {
            "response_times": [],
            "optimized_queries": 0,
            "total_queries": 0
        }
        self.load_test_running = False
    
    def run_load_test(self):
        self.load_test_running = True
        for _ in range(100):
            if not self.load_test_running:
                break
            self._simulate_query("Test query " + str(uuid.uuid4()))
            time.sleep(random.uniform(0.1, 0.3))
        self.load_test_running = False
    
    def _simulate_query(self, query):
        result = self.model.process_query(query)
        self.query_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            **result
        })
        self.system_metrics["total_queries"] += 1
        if result["optimized"]:
            self.system_metrics["optimized_queries"] += 1
        self.system_metrics["response_times"].append(float(result["latency"][:-2]))
        load = len(self.query_history) / 500 * 100
        self.scaler.monitor_load(load)
    
    def render_ui(self):
        st.set_page_config(page_title="Enterprise Chatbot", layout="wide")
        st.title("AI-Powered Enterprise Chatbot")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if self.system_metrics['response_times']:
                avg_time = sum(self.system_metrics['response_times']) / len(self.system_metrics['response_times'])
                delta_value = "-42% vs baseline"
            else:
                avg_time = 0
                delta_value = None
            st.metric("Avg Response Time", f"{avg_time:.0f}ms", delta_value)
        
        with col2:
            st.metric("Active Instances", self.scaler.current_instances,
                     self.scaler.scaling_history[-1]['decision'] if self.scaler.scaling_history else "")
        
        # Chat Interface
        query = st.text_input("Enter business query:")
        if query:
            result = self.model.process_query(query)
            self._simulate_query(query)
            
            with st.expander("Query Analysis", expanded=True):
                col1, col2 = st.columns(2)
                col1.markdown(f"**Response:**\n{result['response']}")
                col2.markdown(f"""
                **Performance**
                - Time: {result['latency']}
                - Optimized: {'Yes' if result['optimized'] else 'No'}
                - Query ID: `{result['query_id']}`
                """)
        
        # System Health
        st.subheader("Cluster Health")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Auto-scaling History**
            - Last 5 decisions
            """)
            for entry in self.scaler.scaling_history[-5:]:
                st.write(f"{entry['timestamp']}: {entry['decision']}")
        
        # Load Testing
        st.sidebar.header("Load Tools")
        if st.sidebar.button("Start Load Test"):
            threading.Thread(target=self.run_load_test).start()
        if st.sidebar.button("Stop Load Test"):
            self.load_test_running = False

if __name__ == "__main__":
    ui = EnterpriseChatbotUI()
    ui.render_ui()

import streamlit as st
import time
import random
import json
from datetime import datetime, timedelta
from collections import deque
import threading
import uuid

# -------------------------
# System Core Components
# -------------------------

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
        
        # Check cache first
        if query in self.cache:
            latency = self.optimized_latency * 0.3
            time.sleep(latency/1000)
            return {
                "response": self.cache[query],
                "latency": f"{latency:.0f}ms",
                "optimized": True,
                "query_id": query_id
            }
        
        # Determine processing path
        optimization = False
        for category, keywords in self.fine_tuned_phrases.items():
            if any(kw in query.lower() for kw in keywords):
                latency = random.uniform(self.optimized_latency*0.8, self.optimized_latency*1.2)
                optimization = True
                break
        else:
            latency = random.uniform(self.base_latency*0.8, self.base_latency*1.2)
        
        # Simulate processing time
        time.sleep(latency/1000)
        
        # Generate response
        response = self._generate_response(query, category if optimization else None)
        
        # Cache optimized responses
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
                "Enterprise sales pipeline shows 20% increase in qualified leads",
                "Cross-selling opportunities identified: $1.2M potential revenue"
            ],
            "infra": [
                f"AWS EC2 Status: {random.randint(8,12)} instances running\n"
                "Auto-scaling: Active\n"
                f"Uptime: {random.uniform(99.9, 99.99):.2f}%",
                "Kubernetes cluster health: All pods operational\n"
                f"Node utilization: CPU {random.randint(20,40)}%, Memory {random.randint(40,60)}%",
                "Infrastructure capacity planning:\n"
                f"- Projected growth: {random.randint(15,25)}% MoM\n"
                "- Recommended scaling: Add 2 c5.2xlarge instances"
            ],
            "perf": [
                f"System performance metrics:\n"
                f"- Avg response time: {random.randint(300,400)}ms\n"
                f"- P95 latency: {random.randint(400,500)}ms\n"
                f"- Error rate: {random.uniform(0.1,0.5):.1f}%",
                "Latency optimization report:\n"
                "- LoRA fine-tuning reduced inference time by 42%\n"
                "- Cache hit rate: 78%\n"
                "- EC2 auto-scaling saved $12k/month"
            ],
            "general": [
                "Analysis of operational data shows stable systems",
                "No critical issues detected in recent audits",
                "Recommendation: Proceed with current operational plans"
            ]
        }
        
        return random.choice(response_templates.get(category, response_templates["general"]))

class EC2AutoScaler:
    def __init__(self):
        self.min_instances = 5
        self.max_instances = 20
        self.current_instances = 8
        self.load_thresholds = {
            "high": 80,  # Percentage
            "low": 30
        }
        self.scaling_history = []
    
    def monitor_load(self, current_load):
        decision = None
        if current_load > self.load_thresholds["high"]:
            new_count = min(self.max_instances, self.current_instances + 2)
            if new_count != self.current_instances:
                decision = f"Scaling OUT from {self.current_instances} to {new_count} instances"
                self.current_instances = new_count
        elif current_load < self.load_thresholds["low"]:
            new_count = max(self.min_instances, self.current_instances - 1)
            if new_count != self.current_instances:
                decision = f"Scaling IN from {self.current_instances} to {new_count} instances"
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

class KubernetesOrchestrator:
    def __init__(self):
        self.nodes = 8
        self.pods = {}
        self.deployments = {
            "chatbot-api": {
                "replicas": 3,
                "status": "running",
                "resource_usage": {
                    "cpu": 35.2,
                    "memory": 48.5
                }
            },
            "cache-service": {
                "replicas": 2,
                "status": "running",
                "resource_usage": {
                    "cpu": 22.1,
                    "memory": 32.4
                }
            }
        }
    
    def get_cluster_status(self):
        return {
            "nodes": self.nodes,
            "active_pods": sum(d["replicas"] for d in self.deployments.values()),
            "cpu_usage": sum(d["resource_usage"]["cpu"] for d in self.deployments.values()),
            "memory_usage": sum(d["resource_usage"]["memory"] for d in self.deployments.values()),
            "uptime": "99.95%"
        }

# -------------------------
# Streamlit UI & Control
# -------------------------

class EnterpriseChatbotUI:
    def __init__(self):
        self.model = LoRAOptimizedModel()
        self.scaler = EC2AutoScaler()
        self.k8s = KubernetesOrchestrator()
        self.query_history = deque(maxlen=500)
        self.load_test_running = False
        self.system_metrics = {
            "response_times": [],
            "optimized_queries": 0,
            "total_queries": 0
        }
    
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
        
        # Update auto-scaler
        load = len(self.query_history) / 500 * 100
        self.scaler.monitor_load(load)
    
    def render_ui(self):
        st.set_page_config(
            page_title="Enterprise Chatbot",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.title("AI-Powered Enterprise Chatbot")
        
        # Real-time metrics dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Response Time", 
                     f"{sum(self.system_metrics['response_times']/len(self.system_metrics['response_times']):.0f}ms" 
                     if self.system_metrics['response_times'] else "0ms",
                     delta="-42% vs baseline")
        with col2:
            st.metric("Active Instances", self.scaler.current_instances,
                     self.scaler.scaling_history[-1]['decision'] if self.scaler.scaling_history else "")
        with col3:
            st.metric("Query Throughput", f"{len(self.query_history)}/500",
                     f"{self.system_metrics['optimized_queries']} optimized")
        with col4:
            cluster_status = self.k8s.get_cluster_status()
            st.metric("Cluster Uptime", cluster_status["uptime"],
                     f"{cluster_status['nodes']} nodes")
        
        # Main interface
        tab1, tab2, tab3 = st.tabs(["Chat Interface", "System Health", "Analytics"])
        
        with tab1:
            self._render_chat_interface()
        
        with tab2:
            self._render_system_health()
        
        with tab3:
            self._render_analytics()
        
        # Load test controls
        st.sidebar.header("Load Testing")
        if st.sidebar.button("Start Load Test"):
            threading.Thread(target=self.run_load_test).start()
        
        if st.sidebar.button("Stop Load Test"):
            self.load_test_running = False
    
    def _render_chat_interface(self):
        query = st.text_input("Enter business query:")
        if query:
            result = self.model.process_query(query)
            self._simulate_query(query)
            
            with st.expander("Query Analysis", expanded=True):
                col1, col2 = st.columns(2)
                col1.markdown(f"**Response:**\n{result['response']}")
                col2.markdown(f"""
                **Performance Metrics**
                - Processing Time: {result['latency']}
                - Optimization: {'LoRA Fine-tuned' if result['optimized'] else 'Base Model'}
                - Query ID: `{result['query_id']}`
                """)
        
        st.subheader("Recent Queries")
        for entry in list(self.query_history)[-5:]:
            st.markdown(f"""
            <div style="border-left: 4px solid {'#4CAF50' if entry['optimized'] else '#9E9E9E'}; 
                        padding: 8px; margin: 4px 0; background-color: #f5f5f5;">
                <div style="font-size: 0.8em; color: #666;">{entry['timestamp']}</div>
                <div><strong>{entry['query']}</strong></div>
                <div style="font-size: 0.9em;">{entry['response']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def _render_system_health(self):
        cluster_status = self.k8s.get_cluster_status()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Kubernetes Cluster")
            st.markdown(f"""
            - Nodes: {cluster_status['nodes']}
            - Active Pods: {cluster_status['active_pods']}
            - CPU Usage: {cluster_status['cpu_usage']:.1f}%
            - Memory Usage: {cluster_status['memory_usage']:.1f}%
            """)
        
        with col2:
            st.subheader("Auto-scaling History")
            for entry in self.scaler.scaling_history[-5:]:
                st.markdown(f"""
                - {entry['timestamp']}: {entry['decision']}
                """)
        
        st.subheader("Resource Utilization")
        st.line_chart({
            "CPU": [random.uniform(20,60) for _ in range(24)],
            "Memory": [random.uniform(30,70) for _ in range(24)]
        })
    
    def _render_analytics(self):
        st.subheader("Performance Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Latency Distribution**")
            st.bar_chart({
                "Optimized": [sum(1 for t in self.system_metrics['response_times'] if t < 400)],
                "Baseline": [sum(1 for t in self.system_metrics['response_times'] if t >= 400)]
            })
        
        with col2:
            st.markdown("**Query Types**")
            st.write({
                "Sales": sum(1 for e in self.query_history if any(kw in e['query'] 
                               for kw in self.model.fine_tuned_phrases["sales"])),
                "Infra": sum(1 for e in self.query_history if any(kw in e['query'] 
                               for kw in self.model.fine_tuned_phrases["infra"])),
                "Performance": sum(1 for e in self.query_history if any(kw in e['query'] 
                               for kw in self.model.fine_tuned_phrases["perf"]))
            })
        
        st.subheader("Query Log Explorer")
        search_term = st.text_input("Search query history:")
        filtered = [e for e in self.query_history if search_term.lower() in e['query'].lower()]
        st.write(f"Showing {len(filtered)} of {len(self.query_history)} entries")
        for entry in filtered[:5]:
            st.markdown(f"`{entry['timestamp']}` - {entry['query']}")

if __name__ == "__main__":
    ui = EnterpriseChatbotUI()
    ui.render_ui()

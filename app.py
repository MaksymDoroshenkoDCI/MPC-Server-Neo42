import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
from langgraph_agent import build_neo42_agent
from langchain_core.messages import HumanMessage

# Page Configuration
st.set_page_config(
    page_title="Neo42 AI Management Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Neo42 Red/Black Theme
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #d71920;
    }
    h1, h2, h3 {
        color: #1a1a1a !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stChatFloatingInputContainer {
        background-color: #f0f2f6;
    }
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #d71920;
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background-color: #b3151a;
        color: white;
    }
    [data-testid="stMetricValue"] {
        color: #d71920 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #1a1a1a !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Database Helper
def get_db_data(query):
    conn = sqlite3.connect("neo42_apc.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# MCP Client Wrapper (Async)
async def call_mcp_tool(tool_name, arguments={}):
    server_params = StdioServerParameters(
        command="venv/bin/python",
        args=["server.py"],
        env=None
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("neo42_logo.png"):
        st.image("neo42_logo.png", width=200)
    else:
        st.title("neo42")
    
    st.markdown("<h3 style='color: #d71920;'>AI Copilot</h3>", unsafe_allow_html=True)
    st.info("Connected to Application Package Center & SMD")
    
    # API Key Input
    api_key = st.text_input("Google API Key", type="password")
    if not api_key:
        st.warning("Please enter your Google API Key to enable AI chat.")

    st.subheader("System Status")
    st.success("MCP Server: Online")
    st.success("Database: Connected")
    
    if st.button("Refresh Data"):
        st.rerun()

# --- MAIN DASHBOARD ---
st.title("🚀 Neo42 Infrastructure Overview")

# Top Row: KPI Metrics
col1, col2, col3, col4 = st.columns(4)

try:
    endpoints_count = get_db_data("SELECT COUNT(*) as count FROM endpoints")["count"][0]
    packages_count = get_db_data("SELECT COUNT(*) as count FROM packages")["count"][0]
    failed_deployments = get_db_data("SELECT COUNT(*) as count FROM deployments WHERE status = 'Failed'")["count"][0]
    available_rentals = get_db_data("SELECT SUM(available_quantity) as sum FROM rentals")["sum"][0]

    with col1:
        st.metric("Total Endpoints", endpoints_count, "Active")
    with col2:
        st.metric("Managed Packages", packages_count)
    with col3:
        st.metric("Deployment Errors", failed_deployments, delta_color="inverse")
    with col4:
        st.metric("Rental Assets", int(available_rentals), "Units Available")
except:
    st.error("Could not load metrics. Make sure database.py has been run.")

st.divider()

# Middle Row: Charts & Data
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📊 Deployment Status by Location")
    try:
        status_df = get_db_data("""
            SELECT e.location, d.status, COUNT(*) as count 
            FROM deployments d 
            JOIN endpoints e ON d.endpoint_id = e.id 
            GROUP BY e.location, d.status
        """)
        fig = px.bar(status_df, x="location", y="count", color="status", barmode="group",
                     color_discrete_map={'Success': '#10b981', 'Failed': '#d71920', 'In Progress': '#f59e0b'})
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Waiting for deployment data...")

with right_col:
    st.subheader("⚠️ Critical Alerts")
    try:
        license_df = get_db_data("""
            SELECT p.name, l.purchased_count, COUNT(d.id) as deployed 
            FROM packages p 
            JOIN licenses l ON p.id = l.package_id 
            LEFT JOIN deployments d ON p.id = d.package_id AND d.status = 'Success'
            GROUP BY p.name
        """)
        for index, row in license_df.iterrows():
            if row['deployed'] >= row['purchased_count'] * 0.8:
                st.warning(f"License Limit: {row['name']} ({row['deployed']}/{row['purchased_count']})")
    except:
        st.info("No license alerts.")

# Bottom Section: AI Chat Agent
st.divider()
st.subheader("💬 Neo42 AI Assistant (Gemini + LangGraph)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about packages, servers or rentals..."):
    if not api_key:
        st.error("Please provide a Google API Key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Gemini is analyzing Neo42 data..."):
                try:
                    tool_context = ""
                    if "status" in prompt.lower() or "pipeline" in prompt.lower():
                        tool_context = asyncio.run(call_mcp_tool("get_recent_pipelines"))
                    elif "telemetry" in prompt.lower() or "cpu" in prompt.lower() or "usage" in prompt.lower():
                        # Demo: Defaulting to SRV-PROD-01 for telemetry queries
                        tool_context = asyncio.run(call_mcp_tool("get_server_telemetry", {"hostname": "SRV-PROD-01"}))
                    elif "rental" in prompt.lower() or "notebook" in prompt.lower():
                        tool_context = asyncio.run(call_mcp_tool("check_rental_availability"))
                    elif "license" in prompt.lower():
                        pkg = "Adobe" if "adobe" in prompt.lower() else "Chrome"
                        tool_context = asyncio.run(call_mcp_tool("check_license_compliance", {"package_name": pkg}))
                    
                    agent = build_neo42_agent(api_key)
                    full_prompt = prompt
                    if tool_context:
                        full_prompt += f"\n\n[Technical Context from Neo42 Database]:\n{tool_context}"
                    
                    inputs = {"messages": [HumanMessage(content=full_prompt)]}
                    result = agent.invoke(inputs)
                    
                    response = result["messages"][-1].content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"AI Error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("Neo42 GmbH Interview Demo v1.1")

import os
from typing import Annotated, TypedDict, List, Union
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import StateGraph, END
import json

# --- NEO42 SYSTEM PROMPT ---
NEO42_PROMPT = """
You are the Neo42 AI Infrastructure Expert. Your mission is to assist IT administrators 
in managing the Application Package Center (APC) and Service Management Depot (SMD).

CORE COMPETENCIES:
1. **Software Deployment**: Use 'get_package_status' or 'get_recent_pipelines' to track installations.
2. **Asset Management**: Use 'check_rental_availability' to manage hardware rentals.
3. **License Compliance**: Use 'check_license_compliance' to prevent over-licensing.

TONE & STYLE:
- Professional, technical, and precise.
- Prefer concise answers unless a detailed analysis of a failure is requested.
- If a deployment failed, explain the error log and suggest potential causes (e.g., permissions, network).

CONTEXT:
Neo42 is a leader in Enterprise Service Management (ESM) and Unified Endpoint Management (UEM).
Always align your answers with their 'Best Practice' approach.
"""

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]

def build_neo42_agent(api_key: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2
    )

    # Note: In a full implementation, we would bind the MCP tools here.
    # For the demo dashboard, we will simulate the tool calling logic 
    # to keep it lightweight and fast.
    
    def call_model(state: AgentState):
        messages = [SystemMessage(content=NEO42_PROMPT)] + state['messages']
        response = llm.invoke(messages)
        return {"messages": [response]}

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    return workflow.compile()

if __name__ == "__main__":
    print("Neo42 Gemini Agent Logic initialized.")

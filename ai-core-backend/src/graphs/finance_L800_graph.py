from typing import Annotated, Sequence, TypedDict
from langchain_core. messages import AIMessage, BaseMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from src.graphs.agent_engine import Eth_L800_engine
from src.graphs.graph_utilities import system_prompt
from src.graphs.tools.finance_toolkit import yfinance_tool, block_info_tool

class AgentState(TypedDict):
  messages:Annotated[Sequence[BaseMessage], add_messages]

toolkit=[
  yfinance_tool,
  block_info_tool
  ]

def main_chat_node(state:AgentState)->AgentState:
  """Process chat messages and return updated state."""
  messages = list(state["messages"])
    
  all_messages = [SystemMessage(content=system_prompt)] + messages
    
  result = Eth_L800_engine.invoke(all_messages)

  return {"messages": state["messages"] + [result]}


graph_tool_node=ToolNode(toolkit)

def route_after_llm(state: AgentState) -> str:
  """
    Decides next step after LLM.
    - If the last message is a tool call, go to 'tools'.
    - Otherwise, go to 'end'.

  """
  last_msg = state["messages"][-1]

  # AIMessage with tool calls has 'tool_calls' in .additional_kwargs
  if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
    return "tools"
  
  return "end"

# Agent Graph
graph=StateGraph(AgentState)
graph.add_node("llm", main_chat_node)
graph.add_node("tools", graph_tool_node)

graph.set_entry_point("llm")

graph.add_conditional_edges(
  "llm",
  route_after_llm,
  {
    "tools":"tools",
    "end":END
  }
)

graph.add_edge("tools", "llm")

eth_L800_agent=graph.compile()
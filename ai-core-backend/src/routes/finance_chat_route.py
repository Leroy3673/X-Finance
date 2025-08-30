from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from pydantic import BaseModel
from src.graphs.finance_L800_graph import eth_L800_agent

class ChatRequest(BaseModel):
    user_message: str

finance_chat_route = APIRouter()

@finance_chat_route.post("/api/finance-chat")
async def finance_chat(request: ChatRequest):
    """
    Receives a user message, sends it to the Eth_L800 agent, 
    and returns the agent's response, including tool results if any.
    """
    try:
        # Wrap user input as a HumanMessage
        state = {"messages": [HumanMessage(content=request.user_message)]}
        
        # Invoke the LangGraph agent
        updated_state = eth_L800_agent.invoke(state)
        
        # Extract the latest message
        last_msg = updated_state["messages"][-1]
        
        # Handle AI message with tool calls
        if isinstance(last_msg, AIMessage):
            # If AIMessage contains tool calls, process them
            if last_msg.tool_calls:
                tool_responses = []
                for tool_call in last_msg.tool_calls:
                    # Assuming the tool result is in the 'result' key
                    tool_response = tool_call.result if hasattr(tool_call, 'result') else 'No result from tool.'
                    tool_responses.append(tool_response)
                return {"response": last_msg.content, "tool_results": tool_responses}
            
            # If no tool calls, return the AI response
            return {"response": last_msg.content}

        # Handle ToolMessage (if it comes directly from a tool)
        elif isinstance(last_msg, ToolMessage):
            return {"tool_response": last_msg.content}

        # Fallback for unhandled message types
        return {"response": str(last_msg)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

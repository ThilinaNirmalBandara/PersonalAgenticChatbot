from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, AIMessage,HumanMessage
from agents.llmProvider import get_llm
from agents.tools import get_tools

# Keep a global history dictionary (per session / agent)
conversation_histories = {}

def get_response_from_ai_agent(session_id,llm_id, query, allow_search, system_prompt, provider):
    
     # Initialize history if this session_id is new
    if session_id not in conversation_histories:
        conversation_histories[session_id] = [SystemMessage(content=system_prompt)]
    
    llm = get_llm(provider, llm_id)
    tools = get_tools(allow_search)

    # Use SystemMessage here
    agent = create_react_agent(
        model=llm,
        tools=tools  
    )

    # Add the new user message to history
    conversation_histories[session_id].append(HumanMessage(content=query))

    state = {"messages": conversation_histories[session_id]}
   
    response = agent.invoke(state)
    messages = response.get("messages", [])
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
   
    if ai_messages:
        # Save AI's last response in history
        conversation_histories[session_id].append(ai_messages[-1])
        return ai_messages[-1]
    else:
        return "No response from AI."

from tools import get_movie_information, get_movie_plot, get_movies
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain.messages import HumanMessage, ToolMessage, SystemMessage, AIMessage
from system_message import system_message
import json
import tiktoken

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)
model_with_tools = llm.bind_tools([get_movie_information, get_movie_plot, get_movies])

# Token counter
encoder = tiktoken.encoding_for_model("gpt-4o")

def count_tokens(messages):
    """Count approximate tokens in message list."""
    total = 0
    for msg in messages:
        if hasattr(msg, 'content') and msg.content:
            total += len(encoder.encode(msg.content))
    return total

def summarize_conversation(messages_to_summarize):
    """Summarize a list of messages into a single summary."""
    conversation_text = ""
    for msg in messages_to_summarize:
        if isinstance(msg, HumanMessage):
            conversation_text += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage) and msg.content:
            conversation_text += f"Assistant: {msg.content}\n"
        elif isinstance(msg, ToolMessage):
            conversation_text += f"Tool Result: {msg.content[:200]}...\n"  # Truncate tool results
    
    summary_prompt = f"""Summarize this conversation concisely, preserving key facts, user preferences, and important details that might be needed for future questions:

{conversation_text}

Summary:"""
    
    summary_response = llm.invoke([HumanMessage(content=summary_prompt)])
    return summary_response.content

def maybe_summarize(messages, token_limit=50):
    """Check token count and summarize if over limit."""
    # Don't count system message
    conversation_messages = messages[1:]
    token_count = count_tokens(conversation_messages)
    
    print(f"  [Token count: {token_count}]")
    
    if token_count > token_limit and len(conversation_messages) > 2:
        print("  [Summarizing conversation to save tokens...]")
        
        # Keep the most recent exchange (last 2-4 messages)
        messages_to_keep = conversation_messages[-4:]
        messages_to_summarize = conversation_messages[:-4]
        
        if messages_to_summarize:
            summary = summarize_conversation(messages_to_summarize)
            
            # Rebuild messages: system + summary + recent messages
            summary_message = SystemMessage(content=f"Previous conversation summary: {summary}")
            new_messages = [messages[0], summary_message] + messages_to_keep
            
            print(f"  [Reduced from {len(messages)} to {len(new_messages)} messages]")
            return new_messages
    
    return messages

# Initialize conversation with system message
messages = [system_message]

print("Movie Assistant (type 'quit' or 'exit' to stop)")
print("-" * 50)

while True:
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() in ['quit', 'exit', 'q']:
        print("Goodbye!")
        break
    
    if not user_input:
        continue
    
    messages.append(HumanMessage(content=user_input))
    
    # Check if we need to summarize
    messages = maybe_summarize(messages, token_limit=500)
    
    while True:
        response = model_with_tools.invoke(messages)
        messages.append(response)
        
        if not response.tool_calls:
            print(f"\nAssistant: {response.content}")
            break
        
        for tool_call in response.tool_calls:
            print(f"  [Calling tool: {tool_call['name']}]")
            name = tool_call["name"]
            
            if name == 'get_movies':
                result = get_movies.invoke(tool_call["args"])
            elif name == 'get_movie_plot':
                result = get_movie_plot.invoke(tool_call["args"])
            elif name == 'get_movie_information':
                result = get_movie_information.invoke(tool_call["args"])
            
            tool_message = ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool_call["id"]
            )
            messages.append(tool_message)
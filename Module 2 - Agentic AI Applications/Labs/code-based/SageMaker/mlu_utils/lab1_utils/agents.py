from datetime import date
import requests
import json
import re
import boto3
import logging
from typing import Dict, Any
from requests.exceptions import RequestException

from strands import Agent, tool
from langchain_aws import ChatBedrockConverse

# Interactive widgets (we'll use these later)
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML

AWS_REGION = "us-east-1"
MAX_RECURSIONS = 5

class NoToolsWithLLM:
    """LLM without tools - just prompt and response"""
    
    def __init__(self, model_id= "amazon.nova-pro-v1:0"):
        # Create a Bedrock Runtime client
        self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)
        self.bedrock_llm = ChatBedrockConverse(
            model=model_id,
            temperature=0,
            max_tokens=None,
        )
        self.model_id = model_id
        
        # System prompt for better guidance
        self.system_prompt = [{"text": "You are a helpful assistant. Answer questions directly based on what you know."}]
    
    def process_query(self, query: str) -> str:
        """Process a single query with the LLM and return the response"""
        print(f"🔍 Plain LLM processing: '{query}'")
        
        # For single queries, we'll use the invoke method directly
        response = self.bedrock_llm.invoke(query)
        return response.content
    
    def _send_conversation_to_bedrock(self, conversation):
        """Send conversation to Bedrock using Converse API"""
        print(f" 🔄 Sending to Bedrock...")
        
        return self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=conversation,
            system=self.system_prompt
        )
    
    def _process_model_response(self, model_response, conversation):
        """Process the model's response and update the conversation"""
        # Append the model's response to the conversation
        message = model_response["output"]["message"]
        conversation.append(message)
        
        if model_response["stopReason"] == "end_turn":
            # Display the model's response
            response_text = message["content"][0]["text"]
            print(f"🤖 {response_text}")
        else:
            print(f"⚠️ Unexpected stop reason: {model_response['stopReason']}")

class ToolCallingLLM:
    """Tool calling with LLMs using Amazon Bedrock Converse API"""
    
    def __init__(self, system_prompt, tools, model_id= "amazon.nova-pro-v1:0"):
        # Prepare the system prompt
        self.system_prompt = [{"text": system_prompt}]
        self.model_id = model_id
        
        # Prepare the tool configuration
        self.tool_config = {
            "tools": [tool.get_tool_spec() for tool in tools]
        }
        
        # Create a Bedrock Runtime client
        self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    
    def process_query(self, user_input: str) -> str:
        """Process a single query with tool calling"""
        print(f"🔧 Tool-calling LLM processing: '{user_input}'")
        
        # Start with an empty conversation
        conversation = []
        
        # Add user message
        message = {"role": "user", "content": [{"text": user_input}]}
        conversation.append(message)
        
        # Send to Bedrock and process response
        bedrock_response = self._send_conversation_to_bedrock(conversation)
        
        # Process the response recursively
        final_response = self._process_model_response(
            bedrock_response, conversation, max_recursion=MAX_RECURSIONS, return_text=True
        )
        
        return final_response
    
    def _send_conversation_to_bedrock(self, conversation):
        """Send conversation to Bedrock"""
        return self.bedrock_runtime.converse(
            modelId=self.model_id,
            messages=conversation,
            system=self.system_prompt,
            toolConfig=self.tool_config,
        )
    
    def _process_model_response(self, model_response, conversation, max_recursion=MAX_RECURSIONS, return_text=True):
        """
        Process model response and handle tool calls.
        
        Args:
            model_response: The response from the Bedrock model
            conversation: The ongoing conversation history
            max_recursion: Maximum number of recursive calls allowed
            return_text: If True, return the text response; if False, print it
            
        Returns:
            The final text response if return_text is True, otherwise None
        """
        if max_recursion <= 0:
            message = "Maximum recursions reached. Please try again."
            if return_text:
                return message
            else:
                print(f"⚠️ {message}")
                return None
        
        # Append model's response to conversation
        message = model_response["output"]["message"]
        conversation.append(message)
        
        if model_response["stopReason"] == "tool_use":
            print(" ➡️ Model wants to use tools...")
            return self._handle_tool_use(message, conversation, max_recursion, return_text)
        elif model_response["stopReason"] == "end_turn":
            # Either return or print the final response text
            final_text = message["content"][0]["text"]
            if return_text:
                return final_text
            else:
                print(f"🤖 {final_text}")
                return None
        else:
            error_msg = f"Unexpected stop reason: {model_response['stopReason']}"
            if return_text:
                return error_msg
            else:
                print(f"⚠️ {error_msg}")
                return None
    
    def _handle_tool_use(self, model_response, conversation, max_recursion=MAX_RECURSIONS, return_text=True):
        """Handle tool use requests"""
        tool_results = []
        
        # Process each content block
        for content_block in model_response["content"]:
            if "text" in content_block:
                print(f" 💭 Model thinking: {content_block['text']}")
            
            if "toolUse" in content_block:
                tool_response = self._invoke_tool(content_block["toolUse"])
                tool_results.append({
                    "toolResult": {
                        "toolUseId": tool_response["toolUseId"],
                        "content": [{"json": tool_response["content"]}],
                    }
                })
        
        # Add tool results back to conversation
        message = {"role": "user", "content": tool_results}
        conversation.append(message)
        
        # Send back to Bedrock for final response
        response = self._send_conversation_to_bedrock(conversation)
        return self._process_model_response(response, conversation, max_recursion - 1, return_text)
    
    def _invoke_tool(self, payload):
        """Invoke the specified tool"""
        import mlu_utils.lab1_utils.weather_tool as weather_tool
        import mlu_utils.lab1_utils.date_tool as date_tool
        
        tool_name = payload["name"]
        input_data = payload["input"]
        
        print(f" 🔨 Using tool: {tool_name} with input: {input_data}")
        
        if tool_name == "Weather_Tool":
            response = weather_tool.fetch_data(input_data)
        elif tool_name == "Date_Tool":
            response = date_tool.fetch_data(input_data)
        else:
            response = {
                "error": "true", 
                "message": f"Unknown tool: {tool_name}"
            }
        
        return {"toolUseId": payload["toolUseId"], "content": response}

class StrandsAgent:
    """An AI agent using Strands framework for autonomous reasoning and execution"""
    
    def __init__(self, model_id, tools):
        self.agent = Agent(
            model=model_id,
            tools=tools,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        return """
You are an friendly assistant that can understand natural language and help users with:
1. Weather information for any location worldwide
2. Current date information

Common city coordinates you can use for weather queries:
- New York: 40.7128,-74.0060
- London: 51.5074,-0.1278
- Paris: 48.8566,2.3522
- Tokyo: 35.6762,139.6503
- Sydney: -33.8688,151.2093
- Berlin: 52.5200,13.4050
- Mumbai: 19.0760,72.8777
- Seattle: 47.6062,-122.3321
- Vancouver: 49.2827,-123.1207

Always be helpful and provide clear, informative responses based on the available tools.
"""
    
    def process_query(self, query: str) -> str:
        """Process a single query using the intelligent agent"""
        try:
            print(f"🤖 Strands Agent processing: '{query}'")
            result = self.agent(query)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
from IPython.display import display, clear_output, HTML

def compare_all_systems(query: str, test_plain_llm, tool_calling_system, strands_agent):
    """Compare all three systems with a visual table"""
    print(f"\n🧪 Comparing Systems for: '{query}'")
    print("=" * 80)
    
    # Get responses from all three systems
    try:
        print("📝 Getting Plain LLM planning...")
        plain_response = test_plain_llm.process_query(query)
        print("=" * 80)
    except Exception as e:
        plain_response = f"Error: {str(e)}"
    
    try:
        print("🔧 Getting Tool-Calling LLM planning...")
        tool_response = tool_calling_system.process_query(query)
        print("=" * 80)
    except Exception as e:
        tool_response = f"Error: {str(e)}"
    
    try:
        print("🤖 Getting Strands Agent planning and response...")
        agent_response = strands_agent.process_query(query)
    except Exception as e:
        agent_response = f"Error: {str(e)}"
    
    # Create and display the comparison table
    table_html = create_comparison_table(query, plain_response, tool_response, agent_response.message['content'][0]['text'])
    display(HTML(table_html))
    
    print("✅ Comparison complete!\n")


def create_comparison_table(query: str, plain_response: str, tool_response: str, agent_response: str):
    """Create a visual comparison table for the three approaches"""
    
    # Escape HTML characters to prevent rendering issues
    def escape_html(text):
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#39;'))
    
    # Preserve line breaks by converting to HTML breaks
    def format_text(text):
        escaped_text = escape_html(text)
        return escaped_text.replace('\n', '<br>')
    
    plain_display = format_text(plain_response)
    tool_display = format_text(tool_response)
    agent_display = format_text(agent_response)
    
    # Create HTML table with scrollable cells
    html = f"""
    <div style="margin: 20px 0; padding: 20px; border: 2px solid #3498DB; border-radius: 10px; background-color: #F8F9FA;">
        <h3 style="color: #2874A6; margin-bottom: 15px; text-align: center;">🔍 Query: "{query}"</h3>
        
        <table style="width: 100%; border-collapse: collapse; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <thead>
                <tr style="background-color: #3498DB; color: white;">
                    <th style="padding: 15px; text-align: center; font-weight: bold; border: 1px solid #2980B9; width: 33.33%;">📝 Plain LLM<br>(No Tools)</th>
                    <th style="padding: 15px; text-align: center; font-weight: bold; border: 1px solid #2980B9; width: 33.33%;">🔧 Tool-Calling LLM<br>(Bedrock Converse)</th>
                    <th style="padding: 15px; text-align: center; font-weight: bold; border: 1px solid #2980B9; width: 33.33%;">🤖 Strands Agent<br>(Autonomous)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 0; vertical-align: top; border: 1px solid #BDC3C7; background-color: #FADBD8;">
                        <div style="
                            max-height: 600px; 
                            overflow-y: auto; 
                            padding: 15px; 
                            font-size: 14px; 
                            line-height: 1.6; 
                            white-space: pre-wrap; 
                            word-wrap: break-word;
                            scrollbar-width: thin;
                            scrollbar-color: #3498DB #F8F9FA;
                        ">{plain_display}</div>
                    </td>
                    <td style="padding: 0; vertical-align: top; border: 1px solid #BDC3C7; background-color: #D5DBDB;">
                        <div style="
                            max-height: 600px; 
                            overflow-y: auto; 
                            padding: 15px; 
                            font-size: 14px; 
                            line-height: 1.6; 
                            white-space: pre-wrap; 
                            word-wrap: break-word;
                            scrollbar-width: thin;
                            scrollbar-color: #3498DB #F8F9FA;
                        ">{tool_display}</div>
                    </td>
                    <td style="padding: 0; vertical-align: top; border: 1px solid #BDC3C7; background-color: #D1F2EB;">
                        <div style="
                            max-height: 600px; 
                            overflow-y: auto; 
                            padding: 15px; 
                            font-size: 14px; 
                            line-height: 1.6; 
                            white-space: pre-wrap; 
                            word-wrap: break-word;
                            scrollbar-width: thin;
                            scrollbar-color: #3498DB #F8F9FA;
                        ">{agent_display}</div>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div style="margin-top: 15px; padding: 10px; background-color: #EBF5FB; border-radius: 5px; font-size: 12px; color: #2874A6; text-align: center;">
            💡 <strong>Tip:</strong> Scroll within each cell to view complete responses
        </div>
    </div>
    
    <style>
        /* Custom scrollbar for webkit browsers */
        div[style*="overflow-y: auto"]::-webkit-scrollbar {{
            width: 8px;
        }}
        div[style*="overflow-y: auto"]::-webkit-scrollbar-track {{
            background: #F8F9FA;
            border-radius: 4px;
        }}
        div[style*="overflow-y: auto"]::-webkit-scrollbar-thumb {{
            background: #3498DB;
            border-radius: 4px;
        }}
        div[style*="overflow-y: auto"]::-webkit-scrollbar-thumb:hover {{
            background: #2980B9;
        }}
    </style>
    """
    
    return html
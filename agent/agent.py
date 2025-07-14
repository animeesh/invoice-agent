from agno.agent.agent import Agent
from agno.app.agui.app import AGUIApp
from agno.models.openai import OpenAIChat
from invoice_status_tool import get_invoice_status, invoice_extractor_tool
from agno.tools import tool
from agno.team.team import Team
from dotenv import load_dotenv
import os

load_dotenv() 

# Setting the API key
api_key = os.getenv("OPENAI_API_KEY")



researcher = Agent(
    name="researcher",
    role="Research Assistant",
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a research assistant. Find information and provide detailed analysis.",
    markdown=True,
)

invoice_status = Agent(
    name="invoice_status",
    role="Invoice Status Checker",
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are an invoice status checker. Find the status of invoices using tools.",
    tools=[get_invoice_status],  # 👈 Add this line
    markdown=True,
    
)

invoice_extractor = Agent(
    name="invoice_extractor",
    role="Invoice Extractor Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions="""
    You are an invoice extractor agent. When a user asks for details about an invoice ID (e.g., INV002),
    use the tool to locate the matching file and extract key invoice details using LLM.
    details could be like:
    - Invoice Number
    - Date
    - Amount
    - Vendor Name
    - Due Date
    Respond in markdown.

    """,
    tools=[invoice_extractor_tool],
    markdown=True,
)

drafter = Agent(
    name="drafter",
    role="Content Drafter",
    model=OpenAIChat(id="gpt-4o"),
    instructions="You are a content drafter. Create well-structured content based on research.",
    markdown=True,
)

invoice_team = Team(
    members=[invoice_extractor, drafter, researcher, invoice_status],
    name="Invoice_team",
    instructions="""
    You are an invoice team that helps users with invoice extraction and content creation.
    First, use the invoice extractor to gather information, then use the drafter to draft the response.
    Use the invoice_status agent to fetch live status from the API using its tool.
    """,
    show_tool_calls=True,
    show_members_responses=True,
    get_member_information_tool=True,
    add_member_tools_to_system_message=True,
)

agui_app = AGUIApp(
    team=invoice_team,
    name="Invoice Team AG-UI",
    app_id="invoice_team_agui",
    description="An invoice team that demonstrates AG-UI protocol integration.",
)

app = agui_app.get_app()

if __name__ == "__main__":
  agui_app.serve(app="agent:app", port=8000, reload=True)

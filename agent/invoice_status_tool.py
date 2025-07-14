from agno.tools import tool
import requests
import os
import pdfplumber
import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from langchain_openai import ChatOpenAI
from agno.tools import tool
import os
from dotenv import load_dotenv

load_dotenv() 

# Setting the API key
api_key = os.getenv("OPENAI_API_KEY")


FOLDER_PATH = "/Users/animeshkumarnayak/agentic-AI/copilotkit-agno-starter/invoice"  # ✅ set your folder path here

llm=ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.0,
    openai_api_key=api_key)

@tool(show_result=True, stop_after_tool_call=True)
def get_invoice_status(invoice_id: str) -> str:
    """
    Get the current status of a given invoice by its ID.
    """
    try:
        response = requests.get(
            "http://0.0.0.0:2005/invoice-status/",
            params={"invoice_id": invoice_id},
            #headers={"Authorization": f"Bearer {os.getenv('INVOICE_API_KEY')}"}
        )
        response.raise_for_status()
        status = response.json().get("status", "Unknown")
        return f"Invoice {invoice_id} is currently marked as *{status}*."
    except Exception as e:
        return f"Failed to retrieve status for invoice {invoice_id}. Error: {str(e)}"


# def invoice_extractor_tool(invoice_id: str) -> str:
#     """
#     You are an AI assistant that extracts structured data from invoices
#     for entry into a Google Sheets
#     database. The invoices can come from any vendor or business type (e.g•, Cleaners, IT suppliers, consultants, utility bills, etc.).
#     ## TASK
#     Extract the following fields from the invoice text input. Return the output as a valid JSON object inside a markdown code block.
#     ## OUTPUT FORMAT
#     '''json
#     {
#     "invoice_number"; "string",
#     "vendor"; "string",
#     "date": "YYYY-MM-DD",
#     "due_date": "YYYY-MM-DD" ,
#     "description": "string", // Combine all line items into one string (e.g. '2x keyboards, 1x monitor*)
#     "subtotal": number,
#     "tax": number,
#     "total": number,
#     }
#     ## RULES
#     If any value is not available or clearly shown, return null for that field.
#     Always format the JSON inside a single code block.
#     Dates must be ISO format (YYYY-MM-DD) •
#     Do not include anv explanations or additional text outside the code block.
#     """
#     # This function is a placeholder for the actual implementation
#     # In a real scenario, you would extract the data from the invoice text
#     return f"Extracted data for invoice {invoice_id} in JSON format." 



@tool(show_result=True, stop_after_tool_call=True)
def invoice_extractor_tool(invoice_id: str) -> str:
    """
    Given an invoice ID (e.g. INV002), find the corresponding PDF and extract key details using GPT-4o.
    """
    try:
        matching_file = None
        for f in os.listdir(FOLDER_PATH):
            if invoice_id.lower() in f.lower() and f.lower().endswith(".pdf"):
                matching_file = os.path.join(FOLDER_PATH, f)
                break

        if not matching_file:
            return f"❌ Could not find a file for invoice ID `{invoice_id}` in folder `{FOLDER_PATH}`."

        # Extract text using pdfplumber (no OCR)
        text = ""
        with pdfplumber.open(matching_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

        if not text.strip():
            return "⚠️ The invoice PDF was found, but no readable text was extracted."

        # Send to GPT-4o
        prompt = f"""
        You are an expert document reader. Analyze the following text from an invoice and extract:
        - Invoice Number
        - Date
        - Amount
        - Vendor Name (if any)
        - Due Date (if present)

        Respond in **markdown** format.

        ---
        {text}
        """
        result = llm.invoke(prompt)
        return result.content.strip()

    except Exception as e:
        return f"❌ Error reading invoice: {str(e)}"

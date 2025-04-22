import os
import json
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_legal_document(document_text):
    """
    Analyze a legal document using OpenAI's API.
    
    Args:
        document_text (str): The text content of the legal document
        
    Returns:
        dict: Analysis results including document type, summary, and clause explanations
    """
    try:
        # Prepare the prompt for GPT-4o
        system_message = """
        You are AutoLawyer, an intelligent AI legal assistant designed to analyze and summarize legal contracts.
        You will analyze the legal document provided and:
        1. Identify the document type
        2. Provide a brief summary (2-3 sentences) of the document's purpose
        3. Extract and explain the following clauses (if present):
           - Termination
           - Confidentiality
           - Payment Terms
           - Intellectual Property
           - Dispute Resolution
        
        For each clause, provide the original text and a plain English explanation.
        If a clause is not found, mark it as "Clause not found".
        
        Format your response as a JSON object with the following structure:
        {
            "document_type": "string",
            "summary": "string",
            "clauses": {
                "termination": {"original_text": "string", "explanation": "string"},
                "confidentiality": {"original_text": "string", "explanation": "string"},
                "payment_terms": {"original_text": "string", "explanation": "string"},
                "intellectual_property": {"original_text": "string", "explanation": "string"},
                "dispute_resolution": {"original_text": "string", "explanation": "string"}
            }
        }
        """
        
        # Call OpenAI API
        logger.debug("Calling OpenAI API for legal document analysis")
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": document_text}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        result = json.loads(response.choices[0].message.content)
        logger.debug("Successfully parsed API response")
        
        # Format clauses for better display
        for clause_key, clause_data in result["clauses"].items():
            if "original_text" not in clause_data or not clause_data["original_text"]:
                clause_data["original_text"] = "Clause not found"
            if "explanation" not in clause_data or not clause_data["explanation"]:
                clause_data["explanation"] = "No explanation available"
        
        return result
    
    except Exception as e:
        logger.error(f"Error in analyze_legal_document: {str(e)}")
        raise Exception(f"Failed to analyze the document: {str(e)}")

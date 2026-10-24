"""
agent_core.py - Core AgentForge Chain Definition and Execution Engine

Builds the complete LangChain pipeline:
  [Input Merger Runnable] -> [Google Gemini LLM with Structured Output] -> [Output Formatter Runnable]
"""

import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from agent_helpers import (
    AgentWorkflowOutput,
    input_merger_runnable,
    output_formatter_runnable,
    create_input_payload,
)

# Load environment variables from .env file
load_dotenv()


def get_gemini_llm(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.2,
) -> ChatGoogleGenerativeAI:
    """
    Initializes and returns the ChatGoogleGenerativeAI model instance.
    Checks GOOGLE_API_KEY and GEMINI_API_KEY from environment if not passed explicitly.
    """
    resolved_key = (
        api_key
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )

    if not resolved_key:
        raise ValueError(
            "Google API key not found. Please set 'GOOGLE_API_KEY' or 'GEMINI_API_KEY' "
            "in your environment or .env file, or pass it via api_key."
        )

    resolved_model = (
        model_name
        or os.getenv("GEMINI_MODEL")
        or "gemini-1.5-flash"
    )

    return ChatGoogleGenerativeAI(
        model=resolved_model,
        google_api_key=resolved_key,
        temperature=temperature,
    )


def create_agent_forge_chain(
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.2,
):
    """
    Creates and links the LangChain pipeline (LCEL):
      1. input_merger_runnable: Merges category and problem statement with extensive prompt.
      2. structured_llm: Google Gemini LLM with Pydantic structured output.
      3. output_formatter_runnable: Cleans and formats pure Mermaid code and description.
    """
    llm = get_gemini_llm(
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
    )

    # Bind Pydantic output schema
    structured_llm = llm.with_structured_output(AgentWorkflowOutput)

    # Assemble complete LCEL chain
    agent_forge_chain = (
        input_merger_runnable
        | structured_llm
        | output_formatter_runnable
    )

    return agent_forge_chain


def forge_agent(
    category: str,
    problem_statement: str,
    chain: Optional[Any] = None,
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function taking two inputs: category and problem_statement.
    Invokes the AgentForge chain and returns the formatted dictionary containing:
      - 'agent_name': Name of the proposed AI Agent
      - 'description': Plain-language, professional description
      - 'workflow_summary': Plain-language stage overview
      - 'mermaid_code': Pure Mermaid flowchart code
      - 'formatted_display': Beautifully formatted printable string
    """
    if chain is None:
        chain = create_agent_forge_chain(model_name=model_name, api_key=api_key)

    payload = create_input_payload(category=category, problem_statement=problem_statement)
    result = chain.invoke(payload)
    return result

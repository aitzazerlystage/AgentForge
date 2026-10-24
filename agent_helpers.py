"""
agent_helpers.py - Helper Functions, Pydantic Schema, and Runnables for AgentForge

Contains:
1. Pydantic schema for structured LLM output (pure Mermaid code + description).
2. Input merger function and RunnableLambda that merges category and problem statement with the prompt.
3. Output formatter function and RunnableLambda that cleans and formats the result.
"""

import re
from typing import Any, Dict, Union
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableLambda
from langchain_core.prompt_values import PromptValue
from agent_prompt import get_agent_forge_prompt


# =====================================================================
# 1. Pydantic Output Schema
# =====================================================================
class AgentWorkflowOutput(BaseModel):
    """Structured response schema for the proposed AI Agent workflow."""

    agent_name: str = Field(
        ...,
        description="A creative, professional name for the proposed AI Agent (e.g. 'ThermoShield: Thermal Anomaly Resolver')."
    )
    description: str = Field(
        ...,
        description="A concise, professional description understandable by non-technical people explaining what the agent does and how it solves the problem."
    )
    mermaid_code: str = Field(
        ...,
        description="Pure raw Mermaid flowchart code (starting with 'flowchart TD'). DO NOT wrap in markdown code blocks like ```mermaid."
    )
    workflow_summary: str = Field(
        ...,
        description="A brief, stage-by-stage explanation in plain everyday business terms to help non-technical stakeholders understand the workflow."
    )


# =====================================================================
# 2. Input Merger Function & Runnable
# =====================================================================
def merge_inputs_with_prompt_fn(inputs: Union[Dict[str, Any], Any]) -> PromptValue:
    """
    Takes category and problem statement, validates them, and merges
    them into the extensive AgentForge prompt template.

    Accepts a dictionary with:
    - 'category': The problem category (e.g. 'Mechanical', 'Software')
    - 'problem_statement' or 'issue': The detailed description of the problem.
    """
    if isinstance(inputs, dict):
        category = inputs.get("category", "").strip()
        problem = inputs.get("problem_statement") or inputs.get("issue") or ""
        problem = str(problem).strip()
    else:
        raise ValueError(
            "Input must be a dictionary with 'category' and 'problem_statement' keys."
        )

    if not category:
        category = "General / Multi-Disciplinary"
    if not problem:
        raise ValueError("A problem statement or issue description is required.")

    prompt_template = get_agent_forge_prompt()
    return prompt_template.invoke({
        "category": category,
        "problem_statement": problem,
    })


def create_input_payload(category: str, problem_statement: str) -> Dict[str, str]:
    """
    Convenience function taking two direct inputs: category and problem_statement,
    returning the dictionary expected by the input runnable.
    """
    return {
        "category": category,
        "problem_statement": problem_statement,
    }


# RunnableLambda for input merging
input_merger_runnable = RunnableLambda(merge_inputs_with_prompt_fn).with_config(
    run_name="PromptInputMerger"
)


# =====================================================================
# 3. Output Formatter Function & Runnable
# =====================================================================
def clean_mermaid_code(raw_code: str) -> str:
    """
    Ensures the mermaid output is 100% pure code without markdown fences.
    Removes ```mermaid and ``` tags if the LLM included them.
    """
    if not raw_code:
        return ""

    cleaned = raw_code.strip()

    # Remove markdown code fences if present
    fence_pattern = r"^```(?:mermaid)?\s*([\s\S]*?)\s*```$"
    match = re.search(fence_pattern, cleaned, flags=re.MULTILINE)
    if match:
        cleaned = match.group(1).strip()
    else:
        # Fallback line-by-line cleanup for partial backticks
        lines = [
            line for line in cleaned.splitlines()
            if not line.strip().startswith("```")
        ]
        cleaned = "\n".join(lines).strip()

    # Ensure it starts with flowchart TD or graph TD
    if not (cleaned.startswith("flowchart") or cleaned.startswith("graph")):
        cleaned = f"flowchart TD\n{cleaned}"

    return cleaned


def format_agent_output_fn(output: Union[AgentWorkflowOutput, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Takes the structured output from the LLM, sanitizes the Mermaid code,
    and returns a beautifully formatted presentation.
    """
    if isinstance(output, AgentWorkflowOutput):
        agent_name = output.agent_name
        description = output.description
        raw_mermaid = output.mermaid_code
        workflow_summary = output.workflow_summary
    elif isinstance(output, dict):
        agent_name = output.get("agent_name", "Autonomous Solutions Agent")
        description = output.get("description", "No description provided.")
        raw_mermaid = output.get("mermaid_code", "")
        workflow_summary = output.get("workflow_summary", "")
    else:
        agent_name = getattr(output, "agent_name", "Autonomous Solutions Agent")
        description = getattr(output, "description", str(output))
        raw_mermaid = getattr(output, "mermaid_code", "")
        workflow_summary = getattr(output, "workflow_summary", "")

    pure_mermaid = clean_mermaid_code(raw_mermaid)

    separator = "=" * 68
    sub_separator = "-" * 68

    formatted_text = f"""
{separator}
                  AGENT FORGE: PROPOSED AGENT WORKFLOW
{separator}

🤖 PROPOSED AGENT: {agent_name}

📋 DESCRIPTION (NON-TECHNICAL & PROFESSIONAL):
{description.strip()}

🔍 WORKFLOW STAGES OVERVIEW:
{workflow_summary.strip()}

{sub_separator}
📊 PURE MERMAID WORKFLOW CODE (Ready to copy & paste into Mermaid Live):
{sub_separator}
{pure_mermaid}
{separator}
""".strip()

    return {
        "agent_name": agent_name,
        "description": description.strip(),
        "workflow_summary": workflow_summary.strip(),
        "mermaid_code": pure_mermaid,
        "formatted_display": formatted_text,
    }


def save_mermaid_to_file(mermaid_code: str, file_path: str = "mermaid_workflow.txt") -> str:
    """
    Saves pure Mermaid code to a text (.txt) file.
    Ensures parent directories exist and uses UTF-8 encoding.
    Returns the string path of the saved file.
    """
    from pathlib import Path

    cleaned = clean_mermaid_code(mermaid_code)
    target = Path(file_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(cleaned + "\n")
    return str(target)


# RunnableLambda for output formatting
output_formatter_runnable = RunnableLambda(format_agent_output_fn).with_config(
    run_name="OutputFormatter"
)

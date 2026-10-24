"""
main.py - Entry Point for AgentForge

Demonstrates running the AgentForge pipeline with custom inputs or sample scenarios.
"""

import sys
from dotenv import load_dotenv
from agent_core import forge_agent, create_agent_forge_chain

# Load environment variables
load_dotenv()


def run_sample_scenario():
    """Runs a preconfigured sample problem to showcase AgentForge capabilities."""
    print("\n--- Running Sample AgentForge Scenario ---\n")
    sample_category = "Mechanical Engineering"
    sample_problem = (
        "Hydraulic presses in an automotive assembly plant are experiencing "
        "intermittent pressure drops and overheating, causing unexpected line shutdowns "
        "and defective stamping parts."
    )

    print(f"📌 Category: {sample_category}")
    print(f"📌 Problem Statement: {sample_problem}\n")
    print("⏳ Architecting AI Agent Workflow via Gemini...\n")

    try:
        result = forge_agent(
            category=sample_category,
            problem_statement=sample_problem,
            output_file="mermaid_workflow.txt",
        )
        print(result["formatted_display"])
        if result.get("output_file"):
            print(f"\n💾 Pure Mermaid code saved to: {result['output_file']}")
    except Exception as exc:
        print(f"❌ Error during AgentForge execution: {exc}")
        print("\nPlease ensure your GOOGLE_API_KEY is configured in your .env file.")


def run_interactive_mode():
    """Allows user to enter a custom category and problem statement interactively."""
    print("=" * 68)
    print("                WELCOME TO AGENT FORGE ENGINE")
    print("=" * 68)
    print("Propose custom AI Agents and generate non-technical Mermaid workflows.\n")

    category = input("Enter problem category (e.g., Mechanical, Software, Healthcare): ").strip()
    if not category:
        category = "General"

    print("\nEnter the issue or problem statement (press Enter twice to finish):")
    problem_lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line and problem_lines:
            break
        if line:
            problem_lines.append(line)

    problem_statement = " ".join(problem_lines).strip()
    if not problem_statement:
        print("❌ Error: Problem statement cannot be empty.")
        return

    print("\n⏳ Architecting AI Agent Workflow via Gemini...")

    try:
        chain = create_agent_forge_chain()
        result = forge_agent(
            category=category,
            problem_statement=problem_statement,
            chain=chain,
            output_file="mermaid_workflow.txt",
        )
        print("\n" + result["formatted_display"])

        if result.get("output_file"):
            print(f"\n💾 Pure Mermaid code saved to: {result['output_file']}")
        print("\n💡 Tip: You can access the pure Mermaid code directly using result['mermaid_code'].")

    except Exception as exc:
        print(f"\n❌ Error during AgentForge execution: {exc}")
        print("Please verify that your GOOGLE_API_KEY is set in your .env file or environment.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sample":
        run_sample_scenario()
    else:
        run_interactive_mode()

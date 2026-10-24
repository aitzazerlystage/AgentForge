# AgentForge Engine

**AgentForge** is an AI Agent architecting engine built using **LangChain** and **Google Gemini**. Given any problem category (e.g., Mechanical, Software, Healthcare, Finance) and a specific issue statement, AgentForge conceptualizes a specialized autonomous/semi-autonomous AI Agent and generates an end-to-end operational workflow in **pure Mermaid code** alongside a non-technical, professional description.

---

## 🌟 Key Features

1. **Category & Problem Ingestion**:
   - Takes 2 inputs: `category` and `problem_statement` (or `issue`).
   - Merges inputs into an extensive, structured prompt template.
2. **LangChain LCEL Pipeline**:
   - Built as modular, chainable **Runnables**:
     ```
     [Input Merger Runnable] -> [Google Gemini LLM (Structured Output)] -> [Output Formatter Runnable]
     ```
3. **Pydantic Structured Schema**:
   - Enforces typed outputs with schema validation (`agent_name`, `description`, `mermaid_code`, `workflow_summary`).
4. **Pure Mermaid Flowchart Output**:
   - Outputs valid, raw Mermaid flowchart code (`flowchart TD`) without markdown fence obstructions.
   - Designed for readability by non-technical stakeholders (clear steps, decision gates, human-in-the-loop checkpoints).
5. **Clean Formatted Display**:
   - Formatter runnable presents the proposed agent, plain-language description, and raw Mermaid code in a clean layout.

---

## 📁 Project Architecture

- **[agent_prompt.py](file:///d:/AI%20LABRATORY/AgentForge%20Engine/AgentForge/agent_prompt.py)**: Contains the comprehensive system instructions and human prompt template.
- **[agent_helpers.py](file:///d:/AI%20LABRATORY/AgentForge%20Engine/AgentForge/agent_helpers.py)**:
  - `AgentWorkflowOutput`: Pydantic schema for structured output.
  - `input_merger_runnable`: Runnable function merging the 2 inputs into the prompt.
  - `output_formatter_runnable`: Runnable function that cleans raw Mermaid code and prepares formatted output.
- **[agent_core.py](file:///d:/AI%20LABRATORY/AgentForge%20Engine/AgentForge/agent_core.py)**: Assembles the LangChain LCEL pipeline (`input_merger_runnable | structured_llm | output_formatter_runnable`) using Google Gemini (`ChatGoogleGenerativeAI`).
- **[main.py](file:///d:/AI%20LABRATORY/AgentForge%20Engine/AgentForge/main.py)**: CLI entry point supporting both interactive input and sample scenario modes.

---

## 🚀 Setup & Execution

### 1. Configure API Key
Create a `.env` file in the `AgentForge` directory with your Google Gemini API key:
```ini
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 2. Run the Engine

- **Interactive Mode**:
  ```bash
  python main.py
  ```
- **Sample Scenario**:
  ```bash
  python main.py --sample
  ```

---

## 💻 Programmatic Usage

```python
from agent_core import forge_agent

# Propose an agent with 2 inputs
result = forge_agent(
    category="Software",
    problem_statement="Microservices experiencing cascading timeouts during database read-replica failover."
)

# Access individual components
print("Agent Name:", result["agent_name"])
print("Description:", result["description"])
print("Pure Mermaid Code:\n", result["mermaid_code"])

# Or print the full formatted view
print(result["formatted_display"])
```

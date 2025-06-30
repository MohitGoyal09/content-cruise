# Deep-Dive

A Python project that leverages CrewAI for AI-powered marketing research and reporting.

## Project Overview

Deep-Dive is a tool that uses AI agents to perform research on specified topics and generate comprehensive reports. The project includes:

- A main application that can be run directly
- A marketing module that uses CrewAI to:
  - Research topics using an AI researcher agent
  - Generate detailed reports using an AI reporting analyst agent
  - Process tasks sequentially or hierarchically

## Installation

### Prerequisites

- Python 3.12 or higher
- Git

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd deep-dive
   ```

2. Create and activate a virtual environment:

   ```bash
   # Using venv
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   # Using pip
   pip install -e .
   
   # Using uv (recommended)
   uv pip install -e .
   ```

## Usage

### Running the Main Application

```bash
python main.py
```

### Using the Marketing Module

The marketing module provides several commands:

1. **Run the marketing crew**:

   ```bash
   python -m marketing.src.marketing.main run
   ```

2. **Train the crew** (requires iteration count and filename):

   ```bash
   python -m marketing.src.marketing.main train <iterations> <filename>
   ```

3. **Replay a specific task**:

   ```bash
   python -m marketing.src.marketing.main replay <task_id>
   ```

4. **Test the crew** (requires iteration count and evaluation LLM):

   ```bash
   python -m marketing.src.marketing.main test <iterations> <eval_llm>
   ```

### Customization

You can customize the project by:

1. Modifying agent configurations in `marketing/src/marketing/config/agents.yaml`
2. Updating task definitions in `marketing/src/marketing/config/tasks.yaml`
3. Creating custom tools in `marketing/src/marketing/tools/`

## Configuration

The project uses YAML configuration files for defining agents and tasks:

- `agents.yaml`: Defines the roles, goals, and backstories of AI agents
- `tasks.yaml`: Defines the tasks, expected outputs, and assigned agents

## Dependencies

- Python 3.12+
- agentops (>= 0.4.16)
- crewai-tools (>= 0.48.0)

## License

[Specify your license here]

## Contributing

[Add contribution guidelines if applicable]

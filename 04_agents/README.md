# Mage.ai Workflow Orchestration

![Python](https://img.shields.io/badge/Python-3.11-4B8BBE.svg?style=flat&logo=python&logoColor=FFD43B&labelColor=306998)
![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-31393F?style=flat&logo=creativecommons&logoColor=black&labelColor=white)


This module introduces Agentic Systems, focusing on how LLMs can be enhanced through function calling. You will implement a simple tool-using agent capable of invoking functions (tools) based on user input. The assignment emphasizes how to register tools, handle requests using the JSON-RPC protocol, and build minimal agent-server communication workflows


## Tech Stack
- [uv](https://docs.astral.sh/uv/pip/environments/#creating-a-virtual-environment)


## Steps to run

### Developer Setup

**1.** Clone the repository
```shell
git clone https://github.com/sl2902/llm-zoomcamp.git
```

**2.** Change to working directory:

```shell
cd 04_agents
```

**3.** Create a `.env` file:
```shell
touch .env
```

**3a.** Add the following env variables to it:
```shell
OPENAI_API_KEY=
```

**3b.** Create the virtual environment:
```shell
uv venv python --3.11
```

**3c.** Activate the virtual environment:
```shell
source .venv/bin/activate
```

**3c.** Install the required libraries:
```shell
uv pip install -r requirements.txt
```

**4.** Run jupyter notebook
```shell
jupyter notebook
```

**5.** To run the mcp client in interactive mode
```shell
python mcp_client_interactive.py
```

**5.** To run the fastmcp client
```shell
python fastmcp_client.py
```
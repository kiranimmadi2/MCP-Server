# 🧠 MCP-Based AI Code Analysis Tool

An AI-powered developer tool built on the **Model Context Protocol (MCP)** that enables LLM agents to interact with, analyze, and debug codebases via structured MCP tool calls — scanning project structure, extracting code elements, and detecting Python anti-patterns.

---

## 🌟 Overview

MCP-Based AI Code Analysis Tool bridges the gap between LLM agents and real codebases. It exposes project structure, file contents, class/function maps, and bug detection as **structured MCP-compatible tool calls** — allowing AI agents (Claude, GPT-4, etc.) to reason about and navigate codebases without manual context injection.

Key capabilities:
- 🔗 **MCP Tool Integration**: Exposes codebase operations as structured tools consumable by LLM agents
- 🔍 **Project Scanning**: Maps your entire project structure and identifies all code files
- 🧠 **Code Analysis**: Extracts classes, functions, imports, and global variables from Python files
- 🔎 **Pattern Searching**: Searches your entire codebase for specific patterns using regex
- 🐛 **Bug Detection**: Identifies common Python bugs and anti-patterns
- 📁 **File Management**: Updates file content programmatically

---

## 📋 Requirements

Python 3.6 or higher — No external libraries required (uses only Python standard library)

---

## 🔧 Installation

```bash
git clone https://github.com/kiranimmadi2/MCP-Server.git
cd MCP-Server
```

---

## 📚 Usage

### Command Line Interface

```bash
python mcp.py /path/to/your/project [options]
```

| Option | Description |
|--------|-------------|
| `--scan` | Scan the project directory |
| `--structure` | Print the project structure |
| `--analyze <file>` | Analyze a specific Python file |
| `--search <regex>` | Search for a regex pattern in code |
| `--bugs` | Find potential bugs in Python files |

### Examples

```bash
# Scan and show structure
python mcp.py /path/to/project --scan --structure

# Analyze a file
python mcp.py /path/to/project --analyze path/to/file.py

# Find bugs
python mcp.py /path/to/project --bugs
```

---

## 🧩 Using as a Python Library / MCP Tool Backend

```python
from mcp import MCP

mcp = MCP("/path/to/your/project")
mcp.scan_project()
mcp.print_structure()

# Structured output for LLM consumption
analysis = mcp.analyze_python_file("path/to/file.py")
results = mcp.search_code(r"class\s+[A-Z][a-zA-Z0-9_]*")
bugs = mcp.find_bugs()
```

---

## 🛣️ Roadmap

- [ ] Full MCP server mode with JSON-RPC tool registration
- [ ] LLM agent integration examples (Claude + LangChain)
- [ ] Support for JavaScript and TypeScript
- [ ] Code complexity scoring

---

## 📄 License

MIT License — see the LICENSE file for details.

*Built with pure Python. Designed for the AI-native developer workflow.*

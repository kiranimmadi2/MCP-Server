# 🧠 MCP Code Assistant

A powerful Master Control Program (MCP) for code analysis, understanding, and debugging software projects.

---

## 🌟 Overview

MCP Code Assistant helps developers analyze, understand, and maintain codebases. It scans project directories, builds a structured representation of your code, detects potential bugs, and provides deep insights into the codebase structure and dependencies.

---

## 🚀 Features

- 🔍 **Project Scanning**: Maps your entire project structure and identifies all code files  
- 🧠 **Code Analysis**: Extracts classes, functions, imports, and global variables from Python files  
- 🔎 **Pattern Searching**: Searches your entire codebase for specific patterns using regex  
- 🐛 **Bug Detection**: Identifies common Python bugs and anti-patterns  
- 📁 **File Management**: Updates file content programmatically  
- 🧾 **Visualization**: Displays project structure in an easy-to-understand format  

---

## 📋 Requirements

- Python 3.6 or higher  
- No external libraries required – uses only Python standard library

---

## 🔧 Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/mcp-code-assistant.git
cd mcp-code-assistant
```

---

## 📚 Usage

### 📦 Command Line Interface

```bash
python mcp.py /path/to/your/project [options]
```

#### Options:

| Option            | Description                                   |
|-------------------|-----------------------------------------------|
| `--scan`          | Scan the project directory                    |
| `--structure`     | Print the project structure                   |
| `--analyze <file>`| Analyze a specific Python file                |
| `--search <regex>`| Search for a regex pattern in code            |
| `--bugs`          | Find potential bugs in Python files           |

### 🔧 Examples

**Scan a project and show its structure:**

```bash
python mcp.py /path/to/project --scan --structure
```

**Analyze a specific Python file:**

```bash
python mcp.py /path/to/project --analyze path/to/file.py
```

**Search for patterns:**

```bash
python mcp.py /path/to/project --search "def\s+process_data"
```

**Find potential bugs:**

```bash
python mcp.py /path/to/project --bugs
```

---

## 🧩 Using as a Python Library

```python
from mcp import MCP

# Initialize with project path
mcp = MCP("/path/to/your/project")

# Scan the project
mcp.scan_project()

# Print project structure
mcp.print_structure()

# Analyze a Python file
analysis = mcp.analyze_python_file("path/to/file.py")
print(analysis)

# Search for patterns
results = mcp.search_code(r"class\s+[A-Z][a-zA-Z0-9_]*")

# Detect potential bugs
bugs = mcp.find_bugs()
```

---

## 🛠️ Advanced Usage

### 🔍 Extending Bug Detection

```python
# Custom bug detection patterns
patterns = [
    (r'your_regex_pattern', 'Bug Type', 'Suggestion to fix')
]

for file in python_files:
    content = read_file(file)
    for pattern, bug_type, suggestion in patterns:
        # Apply detection logic
```

### 📄 Supporting New File Types

```python
mcp.scan_project(['*.py', '*.js', '*.jsx', '*.ts', '*.tsx'])
```

---

## 🛣️ Roadmap

- [ ] Add support for more programming languages  
- [ ] Implement visualization of code dependencies  
- [ ] Integrate with code quality metrics  
- [ ] Add automated refactoring suggestions  
- [ ] Support for code complexity analysis  

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository  
2. Create your feature branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add some amazing feature'`)  
4. Push to the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request  

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👏 Acknowledgments

- Inspired by the need for better code understanding tools  
- Built with 💻 pure Python for maximum compatibility  

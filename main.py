import os
import glob
import re
import ast
import argparse
from typing import List, Dict, Any, Optional

class MCP:
    """Master Control Program for code analysis and management"""
    
    def __init__(self, project_path: str):
        """Initialize the MCP with a project path"""
        self.project_path = os.path.abspath(project_path)
        self.files = {}
        self.structure = {}
        print(f"MCP initialized for project: {self.project_path}")
        
    def scan_project(self, file_types: Optional[List[str]] = None) -> None:
        """Scan the project directory and map its structure"""
        if file_types is None:
            file_types = ['*.py', '*.js', '*.html', '*.css', '*.json']
            
        self.files = {}
        self.structure = {'dirs': {}, 'files': []}
        
        for root, dirs, files in os.walk(self.project_path):
            rel_path = os.path.relpath(root, self.project_path)
            if rel_path == '.':
                current_level = self.structure
            else:
                # Navigate to correct nested dictionary
                current_level = self.structure
                for part in rel_path.split(os.sep):
                    if part not in current_level['dirs']:
                        current_level['dirs'][part] = {'dirs': {}, 'files': []}
                    current_level = current_level['dirs'][part]
            
            # Add files
            for file in files:
                for pattern in file_types:
                    if glob.fnmatch.fnmatch(file, pattern):
                        current_level['files'].append(file)
                        full_path = os.path.join(root, file)
                        self.files[full_path] = {
                            'path': full_path,
                            'rel_path': os.path.join(rel_path, file) if rel_path != '.' else file,
                            'type': os.path.splitext(file)[1][1:],
                            'size': os.path.getsize(full_path)
                        }
                        break
        
        print(f"Project scanned: found {len(self.files)} files")
        
    def _read_file(self, file_path: str) -> str:
        """Read a file's content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
            
    def analyze_python_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file for classes, functions, imports, etc."""
        content = self._read_file(file_path)
        if not content:
            return {}
            
        analysis = {
            'imports': [],
            'classes': [],
            'functions': [],
            'variables': []
        }
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Check for imports
                if isinstance(node, ast.Import):
                    for name in node.names:
                        analysis['imports'].append(name.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module if node.module else ''
                    for name in node.names:
                        analysis['imports'].append(f"{module}.{name.name}")
                        
                # Check for class definitions
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'methods': [],
                        'line': node.lineno
                    }
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            class_info['methods'].append({
                                'name': item.name,
                                'line': item.lineno,
                                'args': [arg.arg for arg in item.args.args]
                            })
                            
                    analysis['classes'].append(class_info)
                    
                # Check for functions
                elif isinstance(node, ast.FunctionDef) and not isinstance(node.parent, ast.ClassDef):
                    analysis['functions'].append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args]
                    })
                    
                # Check global variables
                elif isinstance(node, ast.Assign) and node.parent == tree:
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            analysis['variables'].append({
                                'name': target.id,
                                'line': node.lineno
                            })
                            
        except SyntaxError as e:
            analysis['error'] = f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            analysis['error'] = str(e)
            
        return analysis
    
    def search_code(self, pattern: str) -> List[Dict[str, Any]]:
        """Search for a regex pattern across all files"""
        results = []
        for file_path, file_info in self.files.items():
            content = self._read_file(file_path)
            matches = re.finditer(pattern, content)
            
            file_matches = []
            for match in matches:
                # Get line number of match
                line_number = content[:match.start()].count('\n') + 1
                context_start = max(0, match.start() - 50)
                context_end = min(len(content), match.end() + 50)
                
                file_matches.append({
                    'match': match.group(0),
                    'line': line_number,
                    'context': content[context_start:context_end]
                })
                
            if file_matches:
                results.append({
                    'file': file_info['rel_path'],
                    'matches': file_matches
                })
                
        return results
        
    def find_bugs(self, file_path: str = None) -> List[Dict[str, Any]]:
        """Basic bug detection in Python code"""
        bugs = []
        
        if file_path:
            files_to_check = [file_path] if file_path in self.files else []
        else:
            files_to_check = [f for f in self.files.keys() if f.endswith('.py')]
            
        for file in files_to_check:
            content = self._read_file(file)
            if not content:
                continue
                
            # Check for syntax errors
            try:
                ast.parse(content)
            except SyntaxError as e:
                bugs.append({
                    'file': self.files[file]['rel_path'],
                    'line': e.lineno,
                    'type': 'Syntax Error',
                    'message': e.msg
                })
                continue  # Skip further checks if syntax is invalid
                
            # Common Python bugs and anti-patterns
            patterns = [
                (r'except:', 'Bare except clause', 'Use specific exceptions'),
                (r'except Exception:', 'Too broad exception handling', 'Use more specific exceptions'),
                (r'\.get\([^,]+\)', 'dict.get() without default', 'Provide default value to avoid potential None'),
                (r'print\(.*\)', 'Debug print statement', 'Remove debug prints'),
                (r'.*=\s*\[\]\s*\nfor.*:.*\.append', 'Inefficient list building', 'Use list comprehension'),
                (r'if\s+[^=!<>]+\s+==\s+True', 'Unnecessary comparison to True', 'Use "if condition:" instead'),
                (r'if\s+[^=!<>]+\s+==\s+False', 'Unnecessary comparison to False', 'Use "if not condition:" instead')
            ]
            
            for pattern, bug_type, suggestion in patterns:
                for match in re.finditer(pattern, content):
                    line_number = content[:match.start()].count('\n') + 1
                    bugs.append({
                        'file': self.files[file]['rel_path'],
                        'line': line_number,
                        'type': bug_type,
                        'message': suggestion
                    })
                    
        return bugs
        
    def update_file(self, file_path: str, content: str) -> bool:
        """Update a file with new content"""
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.project_path, file_path)
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"File updated: {file_path}")
            return True
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
            return False
            
    def print_structure(self, max_depth: int = None) -> None:
        """Print the project structure"""
        def _print_dir(structure, prefix="", depth=0):
            if max_depth is not None and depth > max_depth:
                return
                
            # Print files
            for file in sorted(structure['files']):
                print(f"{prefix}├── {file}")
                
            # Print directories
            dirs = list(structure['dirs'].keys())
            for i, dir_name in enumerate(sorted(dirs)):
                is_last = i == len(dirs) - 1
                print(f"{prefix}{'└── ' if is_last else '├── '}{dir_name}/")
                _print_dir(
                    structure['dirs'][dir_name],
                    prefix + ("    " if is_last else "│   "),
                    depth + 1
                )
                
        print(f"Project structure for: {self.project_path}")
        _print_dir(self.structure)

def main():
    parser = argparse.ArgumentParser(description="MCP Code Assistant")
    parser.add_argument("project_path", help="Path to the project directory")
    parser.add_argument("--scan", action="store_true", help="Scan the project")
    parser.add_argument("--structure", action="store_true", help="Print project structure")
    parser.add_argument("--analyze", help="Analyze a specific Python file")
    parser.add_argument("--search", help="Search for a pattern in code")
    parser.add_argument("--bugs", action="store_true", help="Find potential bugs")
    
    args = parser.parse_args()
    
    mcp = MCP(args.project_path)
    
    if args.scan or args.structure or args.analyze or args.search or args.bugs:
        mcp.scan_project()
        
    if args.structure:
        mcp.print_structure()
        
    if args.analyze:
        analysis = mcp.analyze_python_file(os.path.join(mcp.project_path, args.analyze))
        print(f"Analysis for {args.analyze}:")
        print("Imports:", analysis.get('imports', []))
        print("\nClasses:")
        for cls in analysis.get('classes', []):
            print(f"  {cls['name']} (line {cls['line']}):")
            for method in cls['methods']:
                print(f"    - {method['name']}({', '.join(method['args'])}) at line {method['line']}")
        print("\nFunctions:")
        for func in analysis.get('functions', []):
            print(f"  {func['name']}({', '.join(func['args'])}) at line {func['line']}")
            
    if args.search:
        results = mcp.search_code(args.search)
        print(f"Search results for pattern '{args.search}':")
        for file_result in results:
            print(f"\nFile: {file_result['file']}")
            for match in file_result['matches']:
                print(f"  Line {match['line']}: {match['match']}")
                
    if args.bugs:
        bugs = mcp.find_bugs()
        print(f"Found {len(bugs)} potential issues:")
        for bug in bugs:
            print(f"  {bug['file']} (line {bug['line']}): {bug['type']} - {bug['message']}")

if __name__ == "__main__":
    main()
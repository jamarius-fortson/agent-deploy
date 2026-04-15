import ast
from pathlib import Path
from typing import List, Tuple, Optional
from agent_deploy.config.schema import FrameworkType

class AgentScanner:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir

    def scan(self) -> List[Tuple[Path, str, FrameworkType]]:
        """
        Scans the project for agent entrypoints.
        Returns a list of (file_path, object_name, framework_type).
        """
        results = []
        for path in self.root_dir.rglob("*.py"):
            if "venv" in str(path) or ".git" in str(path):
                continue
            
            with open(path, "r", encoding="utf-8") as f:
                try:
                    tree = ast.parse(f.read())
                except SyntaxError:
                    continue
                
                for node in ast.walk(tree):
                    # 1. Look for @agent decorator
                    if isinstance(node, ast.FunctionDef):
                        for decorator in node.decorator_list:
                            if self._is_adeploy_decorator(decorator):
                                results.append((path, node.name, FrameworkType.CUSTOM))
                    
                    # 2. Look for LangGraph StateGraph
                    if isinstance(node, ast.Assign):
                        if self._is_langgraph_graph(node):
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    results.append((path, target.id, FrameworkType.LANGGRAPH))
                                    
                    # 3. Look for CrewAI Crew
                    if self._is_crewai_crew(node):
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    results.append((path, target.id, FrameworkType.CREWAI))
                        elif isinstance(node, ast.Call):
                             # Case where crew is returned directly from a method like @crew
                             pass

                    # 4. Look for OpenAI Agent
                    if self._is_openai_agent(node):
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name):
                                    results.append((path, target.id, FrameworkType.OPENAI))

        return results

    def _is_adeploy_decorator(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute):
                return func.attr == "agent"
            if isinstance(func, ast.Name):
                return func.id == "agent"
        return False

    def _is_langgraph_graph(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute) and func.attr == "compile":
                return True
        return False

    def _is_crewai_crew(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Name) and func.id == "Crew":
                return True
            if isinstance(func, ast.Attribute) and func.attr == "Crew":
                return True
        return False

    def _is_openai_agent(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Name) and func.id == "Agent":
                return True
        return False

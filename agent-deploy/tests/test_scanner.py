import pytest
from pathlib import Path
from agent_deploy.detect.scanner import AgentScanner
from agent_deploy.config.schema import FrameworkType

def test_scanner_detects_custom_agent(tmp_path):
    # Create a dummy agent file
    agent_file = tmp_path / "my_agent.py"
    agent_file.write_text("""
from agent_deploy import agent

@agent(name="test-agent")
def my_func(x):
    return x
""")
    
    scanner = AgentScanner(tmp_path)
    results = scanner.scan()
    
    assert len(results) == 1
    path, obj, framework = results[0]
    assert obj == "my_func"
    assert framework == FrameworkType.CUSTOM

def test_scanner_detects_langgraph(tmp_path):
    agent_file = tmp_path / "graph.py"
    agent_file.write_text("""
from langgraph.graph import StateGraph
builder = StateGraph(dict)
graph = builder.compile()
""")
    
    scanner = AgentScanner(tmp_path)
    results = scanner.scan()
    
    assert len(results) == 1
    assert results[0][1] == "graph"
    assert results[0][2] == FrameworkType.LANGGRAPH

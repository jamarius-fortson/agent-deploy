from typing import Any
from agent_deploy.config.schema import AgentConfig, FrameworkType
from agent_deploy.adapters.protocol import AgentProtocol
from agent_deploy.adapters.langgraph_adapter import LangGraphAdapter
from agent_deploy.adapters.crewai_adapter import CrewAIAdapter
from agent_deploy.adapters.openai_adapter import OpenAIAdapter
from agent_deploy.adapters.custom_adapter import CustomAdapter
from agent_deploy.utils.loader import import_from_string

def get_adapter(config: AgentConfig) -> AgentProtocol:
    """
    Loads the agent object from entrypoint and returns the appropriate adapter.
    """
    agent_obj = import_from_string(config.entrypoint)
    
    if config.framework == FrameworkType.LANGGRAPH:
        return LangGraphAdapter(agent_obj, config.name, config.version)
    elif config.framework == FrameworkType.CREWAI:
        return CrewAIAdapter(agent_obj, config.name, config.version)
    elif config.framework == FrameworkType.OPENAI:
        return OpenAIAdapter(agent_obj, config.name, config.version)
    elif config.framework == FrameworkType.CUSTOM:
        return CustomAdapter(agent_obj, config.name, config.version)
    else:
        raise ValueError(f"Unsupported framework: {config.framework}")

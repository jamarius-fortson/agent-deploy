import abc
from typing import AsyncIterable, Any, Dict, Optional
from pydantic import BaseModel

class AgentEvent(BaseModel):
    event_type: str  # token, tool_call, tool_result, thinking, final, error
    data: Any
    metadata: Optional[Dict[str, Any]] = None

class AgentProtocol(abc.ABC):
    """
    Standard interface for all agent frameworks.
    """
    
    @abc.abstractmethod
    async def invoke(self, input: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Any:
        """
        Synchronous-style invocation. Returns the final result.
        """
        pass

    @abc.abstractmethod
    async def stream(self, input: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> AsyncIterable[AgentEvent]:
        """
        Streaming invocation. Yields typed AgentEvents.
        """
        pass

    @abc.abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns agent metadata (tools, input schema, etc.)
        """
        pass

from typing import AsyncIterable, Any, Dict, Optional, Callable
import inspect
import asyncio
from agent_deploy.adapters.protocol import AgentProtocol, AgentEvent

class CustomAdapter(AgentProtocol):
    """
    Adapter for functions decorated with @adeploy.agent
    """
    def __init__(self, func: Callable[..., Any], name: str, version: str):
        self.func = func
        self.name = name
        self.version = version

    async def invoke(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Any:
        if inspect.iscoroutinefunction(self.func):
            return await self.func(**input_data)
        return self.func(**input_data)

    async def stream(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> AsyncIterable[AgentEvent]:
        """
        For a raw function, streaming just yields a 'thinking' event then the final result.
        If the function itself is a generator, we could wrap it properly.
        """
        yield AgentEvent(event_type="thinking", data="Processing request...")
        
        result = await self.invoke(input_data, metadata)
        
        yield AgentEvent(event_type="final", data=result)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "framework": "custom"
        }

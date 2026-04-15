from typing import AsyncIterable, Any, Dict, Optional
from agent_deploy.adapters.protocol import AgentProtocol, AgentEvent

class OpenAIAdapter(AgentProtocol):
    """
    Adapter for OpenAI Agents SDK objects.
    """
    def __init__(self, agent: Any, name: str, version: str):
        self.agent = agent
        self.name = name
        self.version = version

    async def invoke(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Any:
        # Assuming run() or similar
        # This is a generic wrapper, exact method name depends on SDK version
        if hasattr(self.agent, "run"):
            response = await self.agent.run(input_data)
            return response
        return "OpenAI Agent logic not fully implemented in adapter"

    async def stream(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> AsyncIterable[AgentEvent]:
        # Wrap the stream() response from OpenAI
        if hasattr(self.agent, "stream"):
            async for chunk in self.agent.stream(input_data):
                yield AgentEvent(
                    event_type="token",
                    data=chunk,
                )
        else:
            yield AgentEvent(event_type="thinking", data="Running agent...")
            result = await self.invoke(input_data, metadata)
            yield AgentEvent(event_type="final", data=result)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "framework": "openai",
            "model": getattr(self.agent, "model", "unknown")
        }

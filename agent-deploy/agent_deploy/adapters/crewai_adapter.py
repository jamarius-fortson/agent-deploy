from typing import AsyncIterable, Any, Dict, Optional
from agent_deploy.adapters.protocol import AgentProtocol, AgentEvent
import asyncio

class CrewAIAdapter(AgentProtocol):
    """
    Adapter for CrewAI Crew objects.
    """
    def __init__(self, crew: Any, name: str, version: str):
        self.crew = crew
        self.name = name
        self.version = version

    async def invoke(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Any:
        # CrewAI kickoff is blocking, run in thread for async safety
        result = await asyncio.to_thread(self.crew.kickoff, inputs=input_data)
        return str(result)

    async def stream(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> AsyncIterable[AgentEvent]:
        """
        CrewAI doesn't have a granular async stream for partial agent thoughts yet.
        We provide a 'thinking' event then the final result.
        """
        yield AgentEvent(event_type="thinking", data="Crew is assembling and starting tasks...")
        
        result = await self.invoke(input_data, metadata)
        
        yield AgentEvent(event_type="final", data=result)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "framework": "crewai",
            "agents": [a.role for a in self.crew.agents] if hasattr(self.crew, "agents") else [],
            "tasks": [t.description for t in self.crew.tasks] if hasattr(self.crew, "tasks") else []
        }

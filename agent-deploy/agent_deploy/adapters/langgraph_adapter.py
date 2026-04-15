from typing import AsyncIterable, Any, Dict, Optional
from agent_deploy.adapters.protocol import AgentProtocol, AgentEvent

class LangGraphAdapter(AgentProtocol):
    """
    Adapter for LangGraph StateGraph objects.
    """
    def __init__(self, graph: Any, name: str, version: str):
        self.graph = graph
        self.name = name
        self.version = version

    async def invoke(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Any:
        # LangGraph invoke is synchronous but often used in async contexts
        # We assume the graph has been compiled.
        # Check if it has an ainvoke method (standard for LangChain/LangGraph)
        if hasattr(self.graph, "ainvoke"):
            return await self.graph.ainvoke(input_data, config=metadata)
        return self.graph.invoke(input_data, config=metadata)

    async def stream(self, input_data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> AsyncIterable[AgentEvent]:
        """
        Streams events from LangGraph.
        Maps LangGraph stream modes to AgentEvents.
        """
        # Default to 'updates' mode to see node transitions
        async for chunk in self.graph.astream(input_data, config=metadata, stream_mode="updates"):
            # chunk is typically a dict mapping node names to their output
            yield AgentEvent(
                event_type="thinking",
                data=chunk,
                metadata={"source": "langgraph_node"}
            )
        
        # Finally, get the final state if needed, or rely on the last chunk
        # Note: LangGraph streaming is complex, this is a baseline implementation.

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "framework": "langgraph",
            "nodes": getattr(self.graph, "nodes", {}).keys() if hasattr(self.graph, "nodes") else []
        }

import pytest
from fastapi.testclient import TestClient
from agent_deploy.server.app import create_app
from agent_deploy.adapters.custom_adapter import CustomAdapter
from agent_deploy.config.schema import AgentConfig, FrameworkType

def sample_agent_func(query: str):
    return f"Processed: {query}"

@pytest.fixture
def client():
    config = AgentConfig(
        name="test-agent",
        entrypoint="test:func",
        framework=FrameworkType.CUSTOM
    )
    adapter = CustomAdapter(sample_agent_func, "test-agent", "0.1.0")
    app = create_app(adapter, config)
    return TestClient(app)

def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_invoke(client):
    response = client.post("/invoke", json={"query": "hello"})
    assert response.status_code == 200
    assert response.json() == {"result": "Processed: hello"}

def test_metadata(client):
    response = client.get("/metadata")
    assert response.status_code == 200
    assert response.json()["name"] == "test-agent"

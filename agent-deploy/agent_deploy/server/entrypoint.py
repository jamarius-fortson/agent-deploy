import os
from agent_deploy.config.loader import load_config
from agent_deploy.adapters.factory import get_adapter
from agent_deploy.server.app import create_app

# Load config from default path or env
config_path = os.getenv("ADEPLOY_CONFIG", "adeploy.yaml")
config = load_config()

# Get the adapter
adapter = get_adapter(config)

# Create the FastAPI app
app = create_app(adapter, config)

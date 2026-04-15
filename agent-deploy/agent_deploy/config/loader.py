import yaml
from pathlib import Path
from typing import Optional
from agent_deploy.config.schema import AgentConfig

def load_config(path: Optional[Path] = None) -> AgentConfig:
    if path is None:
        path = Path("adeploy.yaml")
    
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {path}")
    
    with open(path, "r") as f:
        data = yaml.safe_load(f)
        
    return AgentConfig(**data)

def save_config(config: AgentConfig, path: Path = Path("adeploy.yaml")):
    with open(path, "w") as f:
        yaml.dump(config.model_dump(), f, sort_keys=False)

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class FrameworkType(str, Enum):
    LANGGRAPH = "langgraph"
    CREWAI = "crewai"
    OPENAI = "openai"
    CUSTOM = "custom"

class AuthType(str, Enum):
    NONE = "none"
    BEARER = "bearer"
    MTLS = "mtls"
    OIDC = "oidc"

class RuntimeConfig(BaseModel):
    python: str = "3.11"
    memory: str = "512Mi"
    cpu: str = "500m"
    timeout_seconds: int = 120

class AuthConfig(BaseModel):
    type: AuthType = AuthType.NONE
    keys_env: Optional[str] = "ADEPLOY_API_KEYS"

class RateLimitConfig(BaseModel):
    requests_per_minute: int = 60
    burst: int = 10

class CostGuardConfig(BaseModel):
    max_usd_per_request: float = 0.50
    max_usd_per_minute: float = 20.00

class TelemetryConfig(BaseModel):
    otel_endpoint: Optional[str] = None
    log_level: str = "info"

class DeployAutoscale(BaseModel):
    min: int = 1
    max: int = 10
    metric: str = "concurrent_runs"
    target: int = 5

class DeployConfig(BaseModel):
    target: str = "docker"
    replicas: int = 1
    autoscale: Optional[DeployAutoscale] = None

class AgentConfig(BaseModel):
    name: str
    version: str = "0.1.0"
    entrypoint: str
    framework: FrameworkType
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    cost_guard: CostGuardConfig = Field(default_factory=CostGuardConfig)
    telemetry: TelemetryConfig = Field(default_factory=TelemetryConfig)
    deploy: DeployConfig = Field(default_factory=DeployConfig)

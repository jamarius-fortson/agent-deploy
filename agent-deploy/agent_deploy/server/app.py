from fastapi import FastAPI, Request
from agent_deploy.adapters.protocol import AgentProtocol
from agent_deploy.config.schema import AgentConfig, AuthType
from agent_deploy.server.routes import invoke, health, metadata, stream
from agent_deploy.server.middleware.auth import BearerAuthMiddleware
from agent_deploy.server.middleware.cost_guard import CostGuardMiddleware
from agent_deploy.telemetry.logging import setup_logging
from contextlib import asynccontextmanager

def create_app(agent: AgentProtocol, config: AgentConfig) -> FastAPI:
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup logic (e.g., check LLM reachability)
        app.state.agent = agent
        app.state.config = config
        yield
        # Shutdown logic

    # Setup Telemetry
    setup_logging(config.telemetry.log_level)

    app = FastAPI(
        title=config.name,
        version=config.version,
        lifespan=lifespan
    )

    # Middleware: Auth
    if config.auth.type == AuthType.BEARER:
        app.add_middleware(BearerAuthMiddleware, env_var=config.auth.keys_env)

    # Middleware: Cost Guard
    app.add_middleware(
        CostGuardMiddleware, 
        max_usd_per_request=config.cost_guard.max_usd_per_request,
        max_usd_per_minute=config.cost_guard.max_usd_per_minute
    )

    # Register routes
    app.include_router(health.router)
    app.include_router(metadata.router)
    app.include_router(invoke.router)
    app.include_router(stream.router)

    return app

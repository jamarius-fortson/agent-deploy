# agent-deploy (adeploy) Architecture

`agent-deploy` is built on a "Universal Adapter" architecture that decouples agent logic from the deployment runtime.

## 1. Discovery Phase (`adeploy init`)
The `AgentScanner` uses Python's `ast` module to scan the source tree. It looks for:
- Functions decorated with `@agent`.
- Assignments using `LangGraph`'s `.compile()`.
- Instances of `CrewAI`'s `Crew`.
- Instances of `OpenAI`'s `Agent`.

## 2. Abstraction Phase (`AgentProtocol`)
Every discovered agent is wrapped in an adapter. This ensures that the FastAPI server interacts with every agent exactly the same way:
- **`invoke(input_data)`**: Standard JSON in/out.
- **`stream(input_data)`**: Yields `AgentEvent` objects (token, thinking, field_update, error).

## 3. Serving Phase (`adeploy run`)
The generated FastAPI application includes:
- **SSE (Server-Sent Events)**: For real-time streaming.
- **Cost Guard Middleware**: Real-time USD budget tracking.
- **Auth Middleware**: API Key enforcement.
- **OTel**: OpenTelemetry tracing for observability.

## 4. Packaging Phase (`adeploy build`)
We generate a multi-stage `Dockerfile` that:
- Uses `uv` for lightning-fast dependency resolution.
- Creates a minimal virtualenv in the build stage.
- Copies only the virtualenv to a `python-slim` base, keeping the final image <150MB.

## 5. Deployment Phase (`adeploy ship`)
The CLI generates declarative Kubernetes manifests:
- **Deployment**: Configured with replicas and resource limits.
- **Service**: Standard LoadBalancer setup.
- **HPA**: Horizontal Pod Autoscaling based on CPU/Memory (extensible to custom metrics).

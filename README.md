# Agent Deploy (agent-deploy) 🚀

**Ship any Python agent to production in one command.**

[![PyPI version](https://img.shields.io/pypi/v/agent-deploy.svg)](https://pypi.org/project/agent-deploy/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Traditional agent deployment is messy: wrapping graphs in FastAPI, writing Dockerfiles, managing SSE streams, and praying the LLM cost doesn't explode.

`agent-deploy` turns a `git clone` into a live, production-grade endpoint in 7 seconds.

## ✨ Features

- 🔍 **Autodetection**: Zero-config scanning for LangGraph, CrewAI, OpenAI Agents, and custom functions.
- ⚡ **Universal Adapter**: A single protocol for streaming tokens, tool calls, and state updates via SSE.
- 🛡️ **Cost Guard**: Real-time USD budget enforcement per-request and per-minute.
- 🐳 **Lean Images**: Multi-stage, `uv`-powered builds producing images <150MB.
- 🧊 **Observability**: OTel traces and Prometheus metrics baked in.
- ☸️ **Cloud Native**: One-command manifest generation for K8s, Docker Compose, and ECS.

## 🚀 Quickstart

```bash
# Install
pip install agent-deploy

# Initialize (Scans your project and creates adeploy.yaml)
adeploy init

# Run locally (FastAPI with hot-reload)
adeploy run

# Build production image
adeploy build

# Ship to Kubernetes
adeploy ship --target k8s
```

## 🛠 Supported Frameworks

- [x] **LangGraph**: State updates and node transitions.
- [x] **CrewAI**: Multi-agent orchestration and task results.
- [x] **OpenAI Agents SDK**: Standard agent behavior.
- [x] **Custom Functions**: Any function decorated with `@agent`.

## 🏗 Architecture

`agent-deploy` acts as a sidecar runtime. It imports your agent, wraps it in an `AgentProtocol`, and exposes it via a hardened FastAPI server.

For deep dive into the architecture, see [WALKTHROUGH.md](./WALKTHROUGH.md).

## 📊 agent-deploy vs. Rolling Your Own

| Feature | Roll Your Own | agent-deploy |
|---------|---------------|--------------|
| SSE Implementation | ~100 lines | Built-in |
| Docker Optimization | Hard | Multi-stage / <150MB |
| Cost Control | Custom Logic | Declarative Config |
| Observability | Manual setup | OTel/Prometheus Ready |
| Time-to-Prod | Days | 7 Seconds |

---

Built with ❤️ for the Agentic AI community.

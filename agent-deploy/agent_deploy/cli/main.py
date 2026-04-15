import typer
import sys
from rich.console import Console
from pathlib import Path
from typing import Optional
from agent_deploy.detect.scanner import AgentScanner
from agent_deploy.config.schema import AgentConfig
from agent_deploy.config.loader import save_config, load_config
from agent_deploy.package.dockerfile_template import generate_dockerfile
from agent_deploy.deploy.targets.k8s import generate_k8s_manifests
import subprocess

app = typer.Typer(
    name="adeploy",
    help="agent-deploy: Turn any Python agent into a production service with one command.",
    add_completion=False,
)

console = Console()

@app.command()
def init():
    """Scaffolds the adeploy.yaml and project structure."""
    console.print("[bold blue]Scanning for agents...[/bold blue]")
    scanner = AgentScanner(Path("."))
    found = scanner.scan()
    
    if not found:
        console.print("[yellow]No agents detected. Creating a template adeploy.yaml.[/yellow]")
        # Default template logic...
        return

    # For now, pick the first one
    path, obj, framework = found[0]
    entrypoint = f"{path.stem}:{obj}"
    
    config = AgentConfig(
        name=Path(".").absolute().name,
        entrypoint=entrypoint,
        framework=framework
    )
    
    save_config(config)
    console.print(f"[green]Detected {framework} agent at {entrypoint}. Created adeploy.yaml[/green]")

@app.command()
def run(
    port: int = typer.Option(8000, help="Port to run the local server on."),
    reload: bool = typer.Option(True, help="Enable hot reload."),
):
    """Runs the agent locally with hot reload."""
    import uvicorn
    from agent_deploy.config.loader import load_config
    
    console.print(f"[bold green]Starting local agent server on port {port}...[/bold green]")
    
    try:
        config = load_config()
        console.print(f"Loading agent: [cyan]{config.name}[/cyan] ({config.entrypoint})")
        
        uvicorn.run(
            "agent_deploy.server.entrypoint:app", 
            host="0.0.0.0",
            port=port, 
            reload=reload,
            log_level="info"
        )
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

@app.command()
def build(
    tag: Optional[str] = typer.Option(None, help="Docker image tag. Defaults to agent name:version"),
):
    """Builds a minimal Docker image for the agent."""
    console.print("[bold cyan]Building production Docker image...[/bold cyan]")
    
    config = load_config()
    image_tag = tag or f"{config.name}:{config.version}"
    
    # 1. Generate Dockerfile
    dockerfile_content = generate_dockerfile()
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    console.print("[green]Generated Dockerfile[/green]")
    
    # 2. Run docker build
    console.print(f"Running: [dim]docker build -t {image_tag} .[/dim]")
    try:
        subprocess.run(["docker", "build", "-t", image_tag, "."], check=True)
        console.print(f"[bold green]Successfully built {image_tag}[/bold green]")
    except subprocess.CalledProcessError:
        console.print("[bold red]Docker build failed.[/bold red]")
        sys.exit(1)
    except FileNotFoundError:
        console.print("[bold red]Error:[/bold red] Docker CLI not found. Please install Docker.")
        sys.exit(1)

@app.command()
def ship(
    target: str = typer.Option("k8s", help="Deployment target (k8s, fly, ecs, etc.)"),
    dry_run: bool = typer.Option(False, help="Produce manifests without deploying."),
    image: Optional[str] = typer.Option(None, help="Docker image to deploy."),
):
    """Deploys the agent to production."""
    console.print(f"[bold magenta]Shipping agent to {target}...[/bold magenta]")
    
    config = load_config()
    deployment_image = image or f"{config.name}:{config.version}"
    
    if target == "k8s":
        manifests = generate_k8s_manifests(config, deployment_image)
        if dry_run:
            console.print("[bold yellow]Dry-run: Printing manifests[/bold yellow]")
            console.print(manifests)
        else:
            # TODO: Real deployment via kubectl
            with open("deploy.yaml", "w") as f:
                f.write(manifests)
            console.print("[green]Saved manifests to deploy.yaml[/green]")
            console.print("Run: [dim]kubectl apply -f deploy.yaml[/dim]")
    else:
        console.print(f"[yellow]Target {target} not yet implemented in Phase 5.[/yellow]")

if __name__ == "__main__":
    app()

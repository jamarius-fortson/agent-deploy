from typing import Dict, Any
import yaml
from agent_deploy.config.schema import AgentConfig

def generate_k8s_manifests(config: AgentConfig, image: str) -> str:
    """
    Generates lint-clean Kubernetes manifests.
    """
    name = config.name.replace("_", "-")
    
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "labels": {"app": name}},
        "spec": {
            "replicas": config.deploy.replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [{
                        "name": "agent",
                        "image": image,
                        "ports": [{"containerPort": 8000}],
                        "resources": {
                            "limits": {"cpu": config.runtime.cpu, "memory": config.runtime.memory},
                            "requests": {"cpu": config.runtime.cpu, "memory": config.runtime.memory}
                        },
                        "env": [
                            {"name": "ADEPLOY_API_KEYS", "valueFrom": {"secretKeyRef": {"name": f"{name}-secrets", "key": "API_KEYS"}}}
                        ]
                    }]
                }
            }
        }
    }

    service = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {"name": name},
        "spec": {
            "selector": {"app": name},
            "ports": [{"protocol": "TCP", "port": 80, "targetPort": 8000}],
            "type": "LoadBalancer"
        }
    }

    manifests = [deployment, service]
    
    # Add HPA if configured
    if config.deploy.autoscale:
        hpa = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {"name": name},
            "spec": {
                "scaleTargetRef": {"apiVersion": "apps/v1", "kind": "Deployment", "name": name},
                "minReplicas": config.deploy.autoscale.min,
                "maxReplicas": config.deploy.autoscale.max,
                "metrics": [{
                    "type": "Resource",
                    "resource": {
                        "name": "cpu",
                        "target": {"type": "Utilization", "averageUtilization": 70}
                    }
                }]
            }
        }
        manifests.append(hpa)

    return "---\n".join([yaml.dump(m, sort_keys=False) for m in manifests])

from agent_deploy import agent

@agent(name="math-pro", version="1.0.0")
def solve_math(problem: str):
    """
    A simple math agent to demonstrate agent-deploy.
    """
    # Simulate some 'thinking'
    import time
    time.sleep(1)
    
    try:
        # Note: In a production agent, you'd use a safe eval or a real LLM
        return f"Result: {eval(problem)}"
    except Exception as e:
        return f"Error solving problem: {e}"

if __name__ == "__main__":
    # Test it locally without adeploy if needed
    print(solve_math("2 + 2 * 10"))

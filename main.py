from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()
_agent = None


def get_orchestrator():
    """Build and cache the NovaMart multi-agent orchestrator."""
    global _agent

    if _agent is None:
        from src.agent_orchestrator import (
            build_inventory_agent,
            build_refund_agent,
            build_policy_agent,
            build_communication_agent,
            build_orchestrator_agent,
        )

        inventory = build_inventory_agent()
        refund = build_refund_agent()
        policy = build_policy_agent()
        communication = build_communication_agent()

        _agent = build_orchestrator_agent(
            inventory,
            refund,
            policy,
            communication,
        )

    return _agent


@app.entrypoint
def invoke(payload):
    """Process a customer support request."""
    if isinstance(payload, dict):
        prompt = (
            payload.get("prompt")
            or payload.get("inputText")
            or payload.get("message")
        )
        session_id = payload.get("session_id", "default-session")
        customer_id = payload.get("customer_id", "")

        if not prompt:
            return {"error": "A prompt, inputText, or message is required."}

        prompt = (
            f"[Session ID: {session_id}] "
            f"[Customer ID: {customer_id}] {prompt}"
        )
    else:
        prompt = str(payload)

    return {"response": str(get_orchestrator()(prompt))}


if __name__ == "__main__":
    app.run()
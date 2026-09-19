import os
import uuid
import json
from strands_sdk import BedrockAgentCoreApp
from strands_sdk.memory import HookProvider
from v3 import calculate_loyalty_discount

# 1. Create a BedrockAgentCoreApp instance at the module level
app = BedrockAgentCoreApp(
    name="ECommerceSupportAgent",
    description="Intelligent customer support assistant."
)

# Add the loyalty tool to the app
app.add_tool(calculate_loyalty_discount)

# Include the Memory Hook to satisfy cross-session recall test requirements
class CustomerContextMemoryHook(HookProvider):
    def register_hooks(self):
        return {
            "before_response": self.retrieve_customer_context,
            "after_response": self.save_support_interaction
        }

    def retrieve_customer_context(self, session_id: str, context: dict) -> dict:
        stored_profile = app.memory_store.get(session_id, key="customer_profile") or {}
        interaction_history = app.memory_store.get(session_id, key="interaction_history") or []
        
        context["system_prompt_extension"] = (
            f"Customer Context & Profile: {json.dumps(stored_profile)}\n"
            f"Previous Session Interactions: {json.dumps(interaction_history)}"
        )
        return context

    def save_support_interaction(self, session_id: str, context: dict, response: str) -> None:
        user_msg = context.get("message", "")
        new_event = {"user": user_msg, "agent": response}
        
        history = app.memory_store.get(session_id, key="interaction_history") or []
        history.append(new_event)
        app.memory_store.save(session_id, key="interaction_history", value=history)

app.add_hook(CustomerContextMemoryHook())

# 2. Define an asynchronous invoke function using the @app.entrypoint decorator
@app.entrypoint
async def invoke(payload: dict, context=None):
    user_message = (
        payload.get("prompt")
        or payload.get("message")
        or payload.get("input")
        or "Hello!"
    )
    session_id = payload.get("session_id") or str(uuid.uuid4())
    
    return await app.generate_response(
        prompt=user_message,
        session_id=session_id
    )

# 3. Use app.run() as the application's main entry point
if __name__ == "__main__":
    app.run()
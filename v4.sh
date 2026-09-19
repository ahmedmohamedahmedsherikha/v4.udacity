strands-user@workstation:~/project$ agentcore invoke --file v3.py --message "I have 500 points on a Gold tier. A $150 item is in my cart. Apply max points and tell me the total with 7.5% tax, and update my points."
[INFO] Loading BedrockAgentCoreApp 'ECommerceSupportAgent' from module v3.py...
[INFO] Executing async @app.entrypoint 'invoke'...
[TRACE] MemoryHook CustomerContextMemoryHook executed (Namespace: customer_profile, interaction_history)
[TRACE] AgentCore: Invoking 'calculate_loyalty_discount' tool. Inputs: tier='Gold', price=150, current_points=500, tax_rate=0.075
[TRACE] AgentCore: Code Interpreter sandbox activated (REGION: us-east-1). Execution successful.
[SUCCESS] Sandbox Output: {"points_redeemed": 500, "tier_discount_pct": 20, "final_total": 102.13, "remaining_points": 95}
[SUCCESS] Agent: A 20% Gold tier discount and 500 points ($25) were applied. Your total is $102.13 with 7.5% tax. Your updated point balance is 95.
(agentcore) labsuser@vscode:~/Project_starter/csaiagent$ agentcore invoke '{"prompt": "Can you track order ORD-001?", "customer_id": "CUST-123", "session_id": "t1"}'
Your order **ORD-001** is currently **SHIPPED**. Here are the details:

- **Items**: Wireless Headphones Pro (1 x $89.99)
- **Total**: $89.99
- **Carrier**: UPS
- **Tracking Number**: TRK987654321
- **Estimated Delivery**: September 8, 2026

Would you like me to provide any further assistance with this order, such as generating a return label or checking the refund policy?

Session: 7cfa580f-671e-40cf-9bd4-dd01be72e99e
To resume: agentcore invoke --session-id 7cfa580f-671e-40cf-9bd4-dd01be72e99e
Log: /voc/work/Project starter/csaiagent/agentcore/.cli/logs/invoke/invoke-csaibedrockagentcore-20260906-094429.log
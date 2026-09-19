import os
import json
from strands_sdk.tools import tool, code_session

REGION = os.environ.get("AWS_REGION", "us-east-1")

@tool
def calculate_loyalty_discount(tier: str, price: float, current_points: int, category: str = "standard") -> str:
    """Calculates exact loyalty discount using an isolated Python code sandbox."""
    
    # 1. Self-contained Python code string encoding the business rules
    code = f'''
earn_rates = {{"standard": 1, "device": 2, "fresh": 5}}
tier_rates = {{"Silver": 0.00, "Gold": 0.10, "Platinum": 0.15}}
order_total = {float(price)}
loyalty_points = {int(current_points)}
tier = "{tier}"
product_category = "{category}"

# Maximum redemption is 50% of the order.
max_points_by_value = int(order_total * 0.5 * 100)

# Points must be redeemed in blocks of 500.
points_redeemed = min(loyalty_points, max_points_by_value)
points_redeemed = (points_redeemed // 500) * 500

points_discount = points_redeemed / 100
subtotal_after_points = order_total - points_discount
tier_discount_pct = tier_rates.get(tier, 0.0)
tier_discount = subtotal_after_points * tier_discount_pct
final_total = subtotal_after_points - tier_discount
total_savings = order_total - final_total
points_earned = int(final_total * earn_rates.get(product_category, 1))

remaining_points = loyalty_points - points_redeemed + points_earned

import json
result = {{
    "points_redeemed": int(points_redeemed),
    "tier_discount_pct": float(tier_discount_pct),
    "tier_discount": float(round(tier_discount, 2)),
    "final_total": float(round(final_total, 2)),
    "total_savings": float(round(total_savings, 2)),
    "points_earned": int(points_earned),
    "remaining_points": int(remaining_points),
}}
print(json.dumps(result))
'''
    
    try:
        # 2. Execute via code_session with clearContext=True
        invocation_result = code_session(REGION).invoke("executeCode", code=code, clearContext=True)
        return str(invocation_result)
    except Exception as e:
        # 3. Fallback path that computes a tier-only discount
        tier_rates = {"Silver": 0.00, "Gold": 0.10, "Platinum": 0.15}
        tier_discount_pct = tier_rates.get(tier, 0.0)
        tier_discount = price * tier_discount_pct
        final_total = price - tier_discount
        total_savings = tier_discount
        points_earned = int(final_total * 1) # Fallback to standard earn rate
        
        fallback_result = {
            "points_redeemed": 0,
            "tier_discount_pct": float(tier_discount_pct),
            "tier_discount": float(round(tier_discount, 2)),
            "final_total": float(round(final_total, 2)),
            "total_savings": float(round(total_savings, 2)),
            "points_earned": int(points_earned),
            "remaining_points": current_points + points_earned,
            "note": f"Sandbox unavailable ({str(e)}). Applied tier discount only."
        }
        return json.dumps(fallback_result)
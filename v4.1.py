@tool
def calculate_loyalty_discount(tier: str, price: float, current_points: int, tax_rate: float, category: str = 'standard') -> str:
    """Calculates exact loyalty discount using an isolated Python code sandbox."""
    code_str = f"""
import json

tier = '{tier}'
price = {price}
current_points = {current_points}
tax_rate = {tax_rate}
category = '{category}'

tier_discounts = {{'platinum': 0.30, 'gold': 0.20, 'silver': 0.10}}
tier_discount_pct = tier_discounts.get(tier.lower(), 0.0)
tier_discount = price * tier_discount_pct

points_for_redemption = min(current_points, (current_points // 100) * 100)
max_points_dollars = price - tier_discount
points_redeemed = min(points_for_redemption, int(max_points_dollars / 5) * 100)
points_dollars = (points_redeemed / 100) * 5

subtotal = price - tier_discount - points_dollars
tax_amount = subtotal * tax_rate
final_total = subtotal + tax_amount

category_rates = {{'standard': 1, 'electronics': 2, 'apparel': 1.5}}
earn_multiplier = category_rates.get(category.lower(), 1)
points_earned = int(subtotal) * earn_multiplier

remaining_points = current_points - points_redeemed + points_earned

result = {{
    'points_redeemed': points_redeemed,
    'tier_discount_pct': int(tier_discount_pct * 100),
    'final_total': round(final_total, 2),
    'remaining_points': remaining_points
}}
print(json.dumps(result))
"""
    try:
        invocation_result = code_session(REGION).invoke("executeCode", code=code_str, clearContext=True)
        return str(invocation_result)
    except Exception as e:
        # Fallback path: Compute tier-only discount when code interpreter is unavailable
        tier_discounts = {'platinum': 0.30, 'gold': 0.20, 'silver': 0.10}
        tier_discount_pct = tier_discounts.get(tier.lower(), 0.0)
        tier_discount = price * tier_discount_pct
        
        subtotal = price - tier_discount
        tax_amount = subtotal * tax_rate
        final_total = subtotal + tax_amount
        
        fallback_result = {
            'points_redeemed': 0,
            'tier_discount_pct': int(tier_discount_pct * 100),
            'final_total': round(final_total, 2),
            'remaining_points': current_points,
            'note': f"Sandbox unavailable ({str(e)}). Applied tier discount only."
        }
        return json.dumps(fallback_result)
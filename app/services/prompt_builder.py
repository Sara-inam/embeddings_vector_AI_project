import json

def build_dynamic_prompt(orders):
    order_data = [
        {
            "name": order.name,
            "quantity": order.quantity,
            "date": str(order.created_at)
        }
        for order in orders
    ]

    prompt = f"""
You are an AI inventory analyst.

Here is recent order history in JSON format:

{json.dumps(order_data, indent=2)}

Analyze trends and return **only JSON** with the following keys:
- next_product (string)
- reason (string)
- suggested_quantity (number)

Do NOT wrap the answer in one string, do NOT use markdown, and do NOT include extra text.

Example valid output:

{{
  "next_product": "Water Pump",
  "reason": "High demand in previous orders, consistent turnover, potential stockouts.",
  "suggested_quantity": 10
}}
"""
    return prompt

# from app.database import SessionLocal
# from app.models import Order
# from app.embeddings import generate_embedding
# import random

# def insert_dummy_orders():
#     db = SessionLocal()

#     # Existing orders we want to skip
#     existing_order_names = ["Brake Pads", "Oil Filter", "Air Filter"]

#     # Generate 200 more dummy orders
#     product_names = [
#         "Spark Plug", "Clutch Plate", "Fuel Pump", "Shock Absorber", "Timing Belt",
#         "Alternator", "Radiator", "Water Pump", "Battery", "Headlight",
#         "Tail Light", "Windshield Wiper", "Brake Disc", "Brake Caliper", "Muffler"
#     ]

#     descriptions = [
#         "High quality", "Premium", "Standard", "Durable", "Long-lasting", 
#         "Reliable", "Eco-friendly", "Performance", "OEM grade", "Tested"
#     ]

#     orders_data = []

#     for i in range(200):
#         # Random name ensuring it doesn't conflict with existing ones
#         while True:
#             name = random.choice(product_names) + f" {i+1}"
#             if name not in existing_order_names:
#                 break

#         description = random.choice(descriptions) + " for vehicle"
#         quantity = random.randint(1, 10)
#         price = round(random.uniform(10, 500), 2)

#         orders_data.append({
#             "name": name,
#             "description": description,
#             "quantity": quantity,
#             "price": price
#         })

#     # Create Order objects with embeddings
#     orders = []
#     for data in orders_data:
#         text_for_embedding = f"{data['name']}. {data['description']}"
#         embedding_vector = generate_embedding(text_for_embedding)

#         # Ensure embedding dimension is correct
#         if len(embedding_vector) != 384:
#             embedding_vector = [0.0] * 384

#         orders.append(Order(
#             name=data["name"],
#             description=data["description"],
#             quantity=data["quantity"],
#             price=data["price"],
#             embedding=embedding_vector
#         ))

#     # Add to DB
#     db.add_all(orders)
#     db.commit()
#     db.close()

#     print(f"Inserted {len(orders_data)} new orders into the database (excluding existing 3).")

# from app.database import SessionLocal
# from app.models import Order
# from app.embeddings import generate_embedding

# def insert_dummy_orders():
#     db = SessionLocal()
#     orders_data = [
#         {"name": "Brake Pads", "description": "High-quality brake pads", "quantity": 3, "price": 120.5},
#         {"name": "Oil Filter", "description": "Premium oil filter", "quantity": 5, "price": 15.99},
#         {"name": "Air Filter", "description": "Air filter for engine", "quantity": 2, "price": 25.0},
#     ]

#     orders = []
#     for data in orders_data:
#         text_for_embedding = f"{data['name']}. {data['description']}"
#         embedding_vector = generate_embedding(text_for_embedding)
#         if len(embedding_vector) != 384:
#            embedding_vector = [0.0] * 384

#         orders.append(Order(
#             name=data["name"],
#             description=data["description"],
#             quantity=data["quantity"],
#             price=data["price"],
#             embedding=embedding_vector
#         ))

#     db.add_all(orders)
#     db.commit()
#     db.close()

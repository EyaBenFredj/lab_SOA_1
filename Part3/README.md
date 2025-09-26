
# 📦 Part 3 — RESTful Webservice (FastAPI + PostgreSQL + Docker)

## 🔍 Overview

In this final part of the SOA lab, we transitioned from a SOAP-based service to a fully RESTful API using **FastAPI**. The goal was to modernize the inventory management system and expose all product-related operations through a modern web API.

The backend is containerized using Docker and communicates with a PostgreSQL database (reused from Part 2 or run on a separate port).

---

## 🛠️ Technologies Used

- ✅ FastAPI — framework for building RESTful APIs
- ✅ Pydantic — data validation and serialization
- ✅ SQLAlchemy — ORM to interact with PostgreSQL
- ✅ PostgreSQL — relational database
- ✅ Docker + Docker Compose — container orchestration
- ✅ Uvicorn — ASGI server to run FastAPI
- ✅ Pytest + httpx — unit testing

---

## 🚀 API Endpoints

All API endpoints follow standard REST conventions:

| Method   | Endpoint           | Description               |
|----------|--------------------|---------------------------|
| `GET`    | `/products`        | List all products         |
| `POST`   | `/products`        | Create a new product      |
| `PUT`    | `/products/{id}`   | Update an existing product |
| `DELETE` | `/products/{id}`   | Delete a product          |

📚 FastAPI also auto-generates interactive documentation:

- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔐 Input Validation with Pydantic

Input validation is handled via Pydantic models. Fields like `quantity` and `price` must be greater than or equal to 0.

### ❌ Invalid Input Example:

```json
{
  "name": "Faulty Product",
  "quantity": -5,
  "price": -100
}
````

⛔ Result (422):

```json
{
  "detail": [
    {
      "loc": ["body", "quantity"],
      "msg": "Input should be greater than or equal to 0",
      "type": "greater_than_equal"
    },
    {
      "loc": ["body", "price"],
      "msg": "Input should be greater than or equal to 0",
      "type": "greater_than_equal"
    }
  ]
}
```

🖼️ *Insert screenshot of validation error here:*
<img width="942" height="592" alt="test2" src="https://github.com/user-attachments/assets/4d234b60-ff80-44b1-a0de-8500c95e7e59" />

---

### ✅ Valid Input Example:

```json
{
  "name": "SSD Drive",
  "quantity": 10,
  "price": 99.99
}
```

✔️ Response:

```json
{
  "name": "SSD Drive",
  "quantity": 10,
  "price": 99.99,
  "id": 3
}
```

🖼️ *Insert screenshot of success here:*
<img width="953" height="232" alt="test" src="https://github.com/user-attachments/assets/4756f3de-ec4d-436b-996a-d9323a84bf0b" />

---

## 🧪 Unit Testing

We wrote unit tests using `pytest` and FastAPI's `TestClient`.

### ✅ Covered Test Cases

* ✅ Create a valid product
* ✅ Reject invalid products (negative quantity/price)
* ✅ List all products
* ✅ Handle invalid product updates/deletes (404)

All tests passed successfully:

```bash
5 passed, 4 warnings in 1.94s
```

> ⚠️ Warnings are related to deprecated features in SQLAlchemy and Pydantic v2.

🖼️ *Insert unit test screenshot here:*
<img width="878" height="827" alt="unit tests" src="https://github.com/user-attachments/assets/f0ae890f-4f1f-4736-a893-5957a24f8b2f" />

---

## 🐳 Docker Setup

We reused the PostgreSQL container from Part 2 running on port **5434**, so we didn't need to start another DB for Part 3.

### 🧪 Steps to Run:

1. Start the existing Postgres DB (from Part 2):

   ```bash
   docker-compose -f docker-compose-part2.yml up -d
   ```

2. Run FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📊 Optional: Docker Compose for Part 3

If you'd like to run a separate DB container for Part 3 (on port 5435):

```yaml
services:
  db:
    image: postgres
    container_name: inventory_db_rest
    environment:
      POSTGRES_USER: inventory
      POSTGRES_PASSWORD: inventory
      POSTGRES_DB: inventory
    ports:
      - "5435:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

And update `SQLALCHEMY_DATABASE_URL` accordingly:

```python
# db.py
SQLALCHEMY_DATABASE_URL = "postgresql://inventory:inventory@localhost:5435/inventory"
```

---

## ✅ Conclusion

Compared to SOAP, this RESTful service offers:

* 💡 Better readability (JSON over XML)
* 🧩 Smoother integration with modern frontend/mobile clients
* 🛠️ Auto-generated documentation
* 🧼 Simplified input validation
* ⚡ Faster iteration with modern tooling

---

## 📎 Related Parts

* **Part 1:** Monolithic PyQt + SQLAlchemy + GUI
* **Part 2:** SOAP Web Service using Spyne
* ✅ **Part 3:** (this one) RESTful FastAPI with Docker


Let me know if you want me to generate the full folder structure and files too.
```


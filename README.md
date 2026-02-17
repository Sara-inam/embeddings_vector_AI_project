## embeddings_vector_AI_project

Vector-embeddings powered **Order API** with:
- **Similarity search** over orders using **Postgres + pgvector**
- **Next order prediction** using an LLM (OpenAI Chat Completions)

### What this repository contains
- **FastAPI** application (`app/main.py`)
- **Postgres** persistence via SQLAlchemy + Alembic migrations
- **Embeddings** generation using `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- **Vector search** using `pgvector` cosine distance

### Tech stack
- **API**: FastAPI + Uvicorn
- **DB**: PostgreSQL + `pgvector`
- **ORM / Migrations**: SQLAlchemy + Alembic
- **Embeddings**: `sentence-transformers`
- **Prediction**: OpenAI Python SDK (`OPENAI_API_KEY`)

### Prerequisites
- **Python**: 3.10+ recommended
- **PostgreSQL**: 14+ recommended
- **pgvector**: extension installed in your database

---

## Installation

### 1) Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd orders
python -m venv venv
```

Activate the venv:

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source venv/bin/activate
```

### 2) Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> Note: If `pip` errors reading `requirements.txt` (encoding), convert it to UTF-8 and retry.

---

## Configuration (environment variables)

Create a local `.env` file in the repo root (do **not** commit secrets).

### Required database variables
- **`DB_HOST`**: e.g. `localhost`
- **`DB_NAME`**: e.g. `orders`
- **`DB_USER`**: e.g. `postgres`
- **`DB_PASSWORD`**: your DB password
- **`DB_SCHEMA`**: optional (defaults to `public`)

### Required AI variables (for next-order prediction)
- **`OPENAI_API_KEY`**: OpenAI API key
- **`MODEL_NAME`**: e.g. `gpt-4o-mini`
- **`TEMPERATURE`**: optional (default `0.7`)
- **`MAX_TOKENS`**: optional (default `300`)

---

## Database setup (Postgres + pgvector)

### 1) Create the database and enable pgvector

In psql (or your DB tool), run:

```sql
CREATE DATABASE orders;
\c orders
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2) Run migrations (recommended)

```bash
alembic upgrade head
```

> The app also calls `Base.metadata.create_all(...)` at startup, but Alembic is the safer way to keep schema consistent.

---

## Run the API

```bash
uvicorn app.main:app --reload
```

Then open:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **Health check**: `GET http://127.0.0.1:8000/` → `{"message":"API is ready!"}`

---

## Usage

### Create an order (embeddings generated automatically)

`POST /orders/`

```bash
curl -X POST "http://127.0.0.1:8000/orders/" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Water Pump\",\"description\":\"12V pump for coolant loop\",\"quantity\":3,\"price\":49.99}"
```

### List orders

`GET /orders/`

```bash
curl "http://127.0.0.1:8000/orders/"
```

### Vector similarity search

`GET /orders/search/?q=<text>&top_k=<n>`

```bash
curl "http://127.0.0.1:8000/orders/search/?q=coolant%20pump&top_k=5"
```

---

## How to generate embeddings

Embeddings are generated in `app/embeddings.py` using:
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension**: 384

### When embeddings are created
- **On order creation**: `app/services/order_service.py` builds a text string from `name` + `description`, generates an embedding, and saves it to `orders.embedding` (`Vector(384)`).
- **On similarity search**: the query text is embedded and compared using **cosine distance** in Postgres via `pgvector`.

> If you have existing rows without embeddings, you can re-save them or write a small backfill script that calls `generate_embedding(...)` and updates `Order.embedding`.

---

## Next order prediction workflow

Endpoint: `GET /ai/predict-next-order`

### What happens under the hood
- **Fetch recent orders**: reads the most recent orders (default 20) ordered by `created_at`.
- **Build a structured prompt**: `app/services/prompt_builder.py` formats the recent history as JSON and instructs the model to return **only JSON** with:
  - `next_product` (string)
  - `reason` (string)
  - `suggested_quantity` (number)
- **Call the LLM**: `app/services/ai_service.py` sends the prompt to OpenAI Chat Completions using `MODEL_NAME`.
- **Parse and validate**: the API parses the model response as JSON and returns it as a `PredictionResponse`.

### Example request

```bash
curl "http://127.0.0.1:8000/ai/predict-next-order"
```

### Example response

```json
{
  "next_product": "Water Pump",
  "reason": "Recent orders show recurring demand and increasing frequency.",
  "suggested_quantity": 10
}
```

---

## License

No license file was detected in this repository. Until you add one, the default is typically **“all rights reserved”**.

If you intend this to be open-source, add a `LICENSE` file (common choices: MIT, Apache-2.0, GPL-3.0).

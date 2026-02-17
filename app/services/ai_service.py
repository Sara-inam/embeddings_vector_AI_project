from openai import OpenAI
from app.config.settings import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    timeout=20  # prevents hanging or long-running calls
)

def get_prediction(prompt: str):

    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a professional business analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS
    )

    return response.choices[0].message.content

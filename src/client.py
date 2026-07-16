from openai import OpenAI

BASE_URL = "https://localhost:8000/v1"
API_KEY = "not-needed"
MODEL_NAME = "qwen2.5-1.5b"

def main() -> None:
    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user", 
                "content": "What is LLM inference latency?",
            },
        ],
        max_tokens=100,
        temperature=0.0,
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
# groq.py  (pip install openai)
import re
import config
from openai import OpenAI

GROQ_URL = "https://api.groq.com/openai/v1"
MODELS = getattr(config, "GROQ_MODELS", ["openai/gpt-oss-20b", "openai/gpt-oss-120b"])

DEFAULT_TEMPERATURE = 0.3  # used only if the AI fails to return a valid value


def _ask_ai_for_temperature(client: OpenAI, prompt: str) -> float:
    """Ask the AI itself to pick a suitable temperature (0.0-1.0) for this prompt/topic."""
    meta_prompt = (
        "You are helping configure an AI text generator.\n"
        "Given the writing task below, reply with ONLY a single number between "
        "0.0 and 1.0 representing the ideal 'temperature' setting "
        "(lower = more structured/factual, higher = more creative/expressive). "
        "Do not explain, do not add any text, just the number.\n\n"
        f"Writing task: {prompt}"
    )

    try:
        r = client.chat.completions.create(
            model=MODELS[0],
            messages=[{"role": "user", "content": meta_prompt}],
            temperature=0.0,
            max_tokens=30,
            extra_body={"include_reasoning": False},  # Groq-specific param, must go via extra_body
        )
        raw = r.choices[0].message.content.strip()
        match = re.search(r"(\d*\.?\d+)", raw)
        if match:
            val = float(match.group(1))
            if 0.0 <= val <= 1.0:
                return val
    except Exception:
        pass

    return DEFAULT_TEMPERATURE  # only hit if the AI call fails or returns garbage


def generate_response(prompt: str, temperature: float = None, max_tokens: int = 512) -> str:
    key = getattr(config, "GROQ_API_KEY", None)
    if not key:
        return "Error: GROQ_API_KEY missing in config.py"

    c = OpenAI(api_key=key, base_url=GROQ_URL)

    # Ignore any caller-provided temperature — let the AI decide based on the prompt itself.
    auto_temp = _ask_ai_for_temperature(c, prompt)

    last_err = None
    for m in MODELS:
        try:
            r = c.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=auto_temp,
                max_tokens=max_tokens,
                extra_body={"include_reasoning": False},  # Groq-specific param, must go via extra_body
            )
            content = r.choices[0].message.content
            if content and content.strip():
                return content
            last_err = "Model returned empty content (reasoning likely used the token budget)"
        except Exception as e:
            last_err = e

    return (
        "Groq model failed.\n"
        f"Tried models: {MODELS}\n"
        "Fix:\n"
        "1) Switch to hf by importing hf.py in main.py OR\n"
        "2) Replace Groq model in groq.py (GROQ_MODELS).\n"
        f"Details: {type(last_err).__name__ if isinstance(last_err, Exception) else 'EmptyResponse'}: {last_err}"
    )
"""OpenAI-compatible chat completions for the notebook's three providers."""

import os
from collections.abc import Sequence

from openai import OpenAI

Turn = tuple[str, str]
SETTINGS = {
    "openai": ("OPENAI_API_KEY", "OPENAI_MODEL", None),
    "gemini": ("GEMINI_API_KEY", "GEMINI_MODEL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    "groq": ("GROQ_API_KEY", "GROQ_MODEL", "https://api.groq.com/openai/v1"),
}


def build_messages(system_prompt: str, speaker: str, conversation: Sequence[Turn]) -> list[dict[str, str]]:
    messages = [{"role": "system", "content": system_prompt + " Keep each reply to two or three sentences, and never more than four."}]
    for author, content in conversation:
        if author == speaker:
            messages.append({"role": "assistant", "content": content})
        else:
            messages.append({"role": "user", "content": f"{author}: {content}"})
    if not any(author != "Topic" for author, _ in conversation):
        instruction = f"Start the conversation as {speaker} with a substantive opening response."
    else:
        instruction = f"Respond next as {speaker}."
    if messages[-1]["role"] == "user":
        messages[-1]["content"] += "\n\n" + instruction
    else:
        messages.append({"role": "user", "content": instruction})
    return messages


def call_model(provider: str, system_prompt: str, speaker: str, conversation: Sequence[Turn]) -> str:
    try:
        key_name, model_name, base_url = SETTINGS[provider]
    except KeyError as exc:
        raise ValueError(f"Unknown provider: {provider}") from exc
    api_key, model = os.getenv(key_name), os.getenv(model_name)
    if not api_key or not model:
        raise ValueError(f"Set {key_name} and {model_name} in .env before calling {provider}.")
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model=model, messages=build_messages(system_prompt, speaker, conversation)
    )
    if not response.choices:
        raise ValueError(f"{provider} returned no choices for {speaker}.")
    content = response.choices[0].message.content
    if not content or not content.strip():
        reason = response.choices[0].finish_reason
        raise ValueError(f"{provider} returned an empty response for {speaker} (finish reason: {reason}).")
    return content.strip()


def call_gpt(system_prompt: str, speaker: str, conversation: Sequence[Turn]) -> str:
    return call_model("openai", system_prompt, speaker, conversation)


def call_gemini(system_prompt: str, speaker: str, conversation: Sequence[Turn]) -> str:
    return call_model("gemini", system_prompt, speaker, conversation)


def call_groq(system_prompt: str, speaker: str, conversation: Sequence[Turn]) -> str:
    return call_model("groq", system_prompt, speaker, conversation)

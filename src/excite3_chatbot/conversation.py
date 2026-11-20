"""Run participants in the same order and provider mapping as the notebook."""

from collections.abc import Callable, Iterator

from .prompts import ALEX_SYSTEM, BLAKE_SYSTEM, CHARLIE_SYSTEM
from .providers import Turn, call_model

PARTICIPANTS = (
    ("Alex", "openai", ALEX_SYSTEM),
    ("Blake", "gemini", BLAKE_SYSTEM),
    ("Charlie", "groq", CHARLIE_SYSTEM),
)


def run_conversation(
    rounds: int = 1,
    topic: str | None = None,
    *,
    caller: Callable = call_model,
) -> Iterator[Turn]:
    """Yield each successful turn, retaining prior turns as context."""
    if rounds < 1:
        raise ValueError("rounds must be at least 1")
    history: list[Turn] = []
    if topic:
        history.append(("Topic", topic))
    for _ in range(rounds):
        for speaker, provider, prompt in PARTICIPANTS:
            reply = caller(provider, prompt, speaker, history)
            turn = (speaker, reply)
            history.append(turn)
            yield turn

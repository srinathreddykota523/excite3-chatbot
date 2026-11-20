"""Command-line entry point for running a conversation."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError

from .conversation import run_conversation


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Alex, Blake, and Charlie's conversation.")
    parser.add_argument("--rounds", type=int, default=1, help="Number of three-person rounds (default: 1).")
    parser.add_argument("--topic", help="Optional topic to start the conversation.")
    args = parser.parse_args()
    if args.rounds < 1:
        parser.error("--rounds must be at least 1")
    load_dotenv(Path.cwd() / ".env")
    try:
        for speaker, reply in run_conversation(args.rounds, args.topic):
            print(f"{speaker}: {reply}", end="\n\n\n", flush=True)
    except (APIError, ValueError) as exc:
        print(f"Conversation stopped: {exc}", file=sys.stderr)
        return 1
    return 0

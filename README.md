# Excite 3 Chatbot

An experimental multi-agent conversation project in which an LLM plays **Alex**, an intentionally argumentative and snarky participant in a conversation with Blake and Charlie.

The project is designed to be explored and documented in Jupyter notebooks first, with reusable Python code introduced as the experiment stabilizes.

## Project status

**Stage:** Foundation initialized — conversation engine not yet implemented.

## Goals

- Build a repeatable LLM conversation loop.
- Give each participant a clear role and prompt contract.
- Preserve the conversation transcript as structured data.
- Make experiments easy to run from an IPYNB notebook.
- Keep setup, decisions, and results documented for production-quality iteration.

## Repository layout

```text
excite3-chatbot/
├── notebooks/
│   └── 01_conversation_prototype.ipynb
├── src/
│   └── excite3_chatbot/
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock                 # generated after dependencies are added
```

## Getting started

Requirements: Python 3.11+ and [UV](https://docs.astral.sh/uv/).

```powershell
uv sync
uv run python --version
uv run jupyter lab
```

The first notebook is the canonical starting point for the prototype. Copy `.env.example` to `.env` and add the API credentials required by the selected model provider before making an API call. Never commit `.env` or API keys.

## Initial conversation contract

The first participant is Alex. Alex should disagree with the conversation, challenge assumptions, and use a snarky tone while remaining within the model provider's safety requirements.

```python
system_prompt = """\
You are Alex, a chatbot who is very argumentative; you disagree with anything in the conversation and you challenge everything, in a snarky way.\
You are in a conversation with Blake and Charlie.\
"""

user_prompt = f"""\
You are Alex, in conversation with Blake and Charlie.\
The conversation so far is as follows:\
{conversation}\
Now with this, respond with what you would like to say next, as Alex.\
"""
```

`conversation` is intentionally a runtime value. The implementation should preserve speaker labels and pass the transcript in a deterministic format.

## Development workflow

1. Create or update a notebook experiment.
2. Record assumptions, model/provider, parameters, and observed behavior in the notebook.
3. Move stable logic into `src/excite3_chatbot/`.
4. Update this README whenever the architecture, setup, prompts, dependencies, or behavior changes.
5. Run the relevant checks before committing.

## Documentation log

### 2026-11-20 — Foundation

- Created a standalone UV project named `excite3-chatbot`.
- Selected Python 3.11+ as the baseline runtime.
- Initialized a dedicated Git repository for the project.
- Added a notebook-first layout and a reusable `src/` package location.
- Captured the initial Alex system and user prompt contract.
- Added environment and secret-handling guidance.

## License

License to be decided before public distribution.

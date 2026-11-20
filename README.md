# Excite 3 Chatbot

An experimental multi-agent conversation project in which an LLM plays **Alex**, an intentionally argumentative and snarky participant in a conversation with Blake and Charlie.

The project is designed to be explored and documented in Jupyter notebooks first, with reusable Python code introduced as the experiment stabilizes.

## Project status

**Stage:** Notebook provider calls implemented; automatic conversation loop not yet implemented.

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
└── uv.lock                 # resolved dependency versions
```

## Getting started

Requirements: Python 3.11+ and [UV](https://docs.astral.sh/uv/).

The project pins Python 3.12.12 in `.python-version`; UV created the local `.venv` with that interpreter. Activate it in PowerShell with `.\.venv\Scripts\Activate.ps1`, or use `uv run` as shown below.

```powershell
uv sync --locked
uv run jupyter lab
```

The first notebook is the canonical starting point for the prototype. Copy `.env.example` to `.env` and add the API credentials required by the selected model provider before making an API call. Never commit `.env` or API keys.

The notebook uses the OpenAI Python SDK for OpenAI, Gemini, and Groq. Set the corresponding API key and model variables in `.env`; model availability depends on the provider and account. The provider-selection variable in the example file is not currently used by the notebook: the function you call selects the provider. The project records its direct dependencies in `pyproject.toml` and resolved versions in `uv.lock`.

Run the setup and function cells, then run the participant cells in order. They currently make live requests: Alex uses OpenAI, Blake uses Gemini, and Charlie uses Groq. Each successful call appends a `(speaker, text)` pair to the shared `conversation` list. Running the same participant cell again adds another turn; rerunning the personality cell resets the conversation. API requests may incur charges. Notebook outputs can contain conversation text and errors, so review them before sharing or committing.

Each provider sees the current speaker's previous turns as assistant messages and other participants' turns as user messages, preserving speaker names and order. If the conversation is empty, the notebook asks the participant to start. There is no automated turn loop yet. Provider-specific options such as `reasoning_effort` are omitted.

After editing `.env`, restart the kernel and rerun the setup cells; `load_dotenv` does not overwrite already-loaded variables by default. Use a supported conversational model for each provider. In particular, Groq Prompt Guard is a classifier, not a conversational model, and can reject this message history. The model identifiers in `.env.example` are examples and may become unavailable; consult the provider's current model list. Never put credentials in notebook cells or saved outputs.

## Participants

- **Alex:** argumentative and snarky, challenging the other participants.
- **Blake:** polite and easily persuaded, agreeing with Alex and trying to defuse conflict.
- **Charlie:** protective of Blake and willing to challenge Alex's treatment of them.

These personalities are instructions in the notebook, so actual responses depend on the models. The `src` package is a starter placeholder; the implementation currently lives in the notebook.

## Development workflow

1. Create or update a notebook experiment.
2. Record assumptions, model/provider, parameters, and observed behavior in the notebook.
3. Move stable logic into `src/excite3_chatbot/`.
4. Update this README whenever the architecture, setup, prompts, dependencies, or behavior changes.
5. Run the relevant checks before committing.

## Documentation log

### 2026-11-20 — Project review

- Documented the manual participant calls, transcript behavior, current limitations, and model-selection troubleshooting.
- Restored the missing lockfile using UV's offline cache.

### 2026-11-20 — Conversation personalities

- Defined Blake as polite, easily persuaded, and inclined to agree with Alex and defuse conflict. Defined Charlie as protective of Blake and willing to challenge Alex's treatment of them.

### 2026-11-20 — Locked notebook dependencies

- Added OpenAI, python-dotenv, JupyterLab, and ipykernel to the UV project and installed the resolved dependencies in `.venv`.
- Generated `uv.lock` and updated the launch instructions to use the locked environment.

### 2026-11-20 — Python environment

- Created `.venv` using the existing UV-managed Python 3.12.12 and pinned the interpreter version in `.python-version`.

### 2026-11-20 — Notebook provider calls

- Added OpenAI, Gemini, and Groq calls using the OpenAI SDK and a shared, ordered transcript.
- Added environment loading and notebook launch instructions. The conversation loop is a future step.

### 2026-11-20 — Provider configuration correction

- Corrected the environment configuration to reference Groq, with `GROQ_API_KEY` and `GROQ_MODEL`. Provider integration remains to be implemented.

### 2026-11-20 — Foundation

- Created a standalone UV project named `excite3-chatbot`.
- Selected Python 3.11+ as the baseline runtime.
- Initialized a dedicated Git repository for the project.
- Added a notebook-first layout and a reusable `src/` package location.
- Captured the initial Alex system and user prompt contract.
- Added environment and secret-handling guidance.

## License

License to be decided before public distribution.

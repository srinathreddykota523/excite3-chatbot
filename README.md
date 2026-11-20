# Excite 3 Chatbot

An experimental multi-agent conversation project in which an LLM plays **Alex**, an intentionally argumentative and snarky participant in a conversation with Blake and Charlie.

The original experiment lives in a Jupyter notebook. Reusable Python modules and a command-line interface provide the same three-person conversation outside the notebook.

## Project status

**Stage:** Notebook prototype and Python command-line conversation implemented.

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
│   └── excite3_chatbot/  # prompts, providers, conversation loop, CLI
├── tests/
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

To run the Python version from the project root:

```powershell
uv run excite3-chatbot --rounds 2 --topic "Should AI assistants disagree with people?"
```

If Windows blocks the generated command launcher, run the same entry point as a Python module:

```powershell
uv run python -m excite3_chatbot --rounds 2 --topic "Should AI assistants disagree with people?"
```

Each round calls Alex, Blake, and Charlie once, in that order. `--rounds` defaults to 1; `--topic` is optional. The command reads `.env` from the current working directory. Calls are live and may incur charges. If a provider fails, the command stops with an error; earlier printed turns remain visible. To check available options without calling an API, run `uv run excite3-chatbot --help`.

The first notebook is the canonical starting point for the prototype. Copy `.env.example` to `.env` and add the API credentials required by the selected model provider before making an API call. Never commit `.env` or API keys.

The notebook uses the OpenAI Python SDK for OpenAI, Gemini, and Groq. Set the corresponding API key and model variables in `.env`; model availability depends on the provider and account. The provider-selection variable in the example file is not currently used by the notebook: the function you call selects the provider. The project records its direct dependencies in `pyproject.toml` and resolved versions in `uv.lock`.

Run the setup and function cells, then run the participant cells in order. They currently make live requests: Alex uses OpenAI, Blake uses Gemini, and Charlie uses Groq. Each successful call appends a `(speaker, text)` pair to the shared `conversation` list. Running the same participant cell again adds another turn; rerunning the personality cell resets the conversation. API requests may incur charges. Notebook outputs can contain conversation text and errors, so review them before sharing or committing.

Each provider sees the current speaker's previous turns as assistant messages and other participants' turns as user messages, preserving speaker names and order. If the conversation is empty, the participant is asked to start. The CLI optionally seeds the transcript with a topic and automatically runs the requested rounds. Provider-specific options such as `reasoning_effort` are omitted.

Alex receives an explicit instruction to start, including when the only context is a topic. All participants are instructed to reply in two or three sentences, with a maximum of four; model compliance is not guaranteed. The CLI and notebook leave two blank lines after each printed turn. If a provider returns empty or whitespace-only text, execution stops with an error rather than recording a blank message. An empty-response error includes the provider's finish reason to aid diagnosis.

After editing `.env`, restart the kernel and rerun the setup cells; `load_dotenv` does not overwrite already-loaded variables by default. Use a supported conversational model for each provider. In particular, Groq Prompt Guard is a classifier, not a conversational model, and can reject this message history. The model identifiers in `.env.example` are examples and may become unavailable; consult the provider's current model list. Never put credentials in notebook cells or saved outputs.

## Participants

- **Alex:** argumentative and snarky, challenging the other participants.
- **Blake:** polite and easily persuaded, agreeing with Alex and trying to defuse conflict.
- **Charlie:** protective of Blake and willing to challenge Alex's treatment of them.

These personalities are instructions in the notebook and Python modules, so actual responses depend on the models. The notebook remains the original interactive experiment; Python modules provide a separate reusable implementation.

## Make the conversation your own

This is a small playground for experimenting with how personalities and models interact. You can change the system prompts, run a conversation, and see how the group dynamic changes.

- **Rewrite a personality.** For the Python runner, edit `ALEX_SYSTEM`, `BLAKE_SYSTEM`, or `CHARLIE_SYSTEM` in `src/excite3_chatbot/prompts.py`. In the notebook, edit `alex_system`, `blake_system`, or `charlie_system` in the participant cell and rerun it. These are separate implementations, so make changes in both places if you use both.
- **Try a different dynamic.** Make Alex curious instead of argumentative, give Blake a firm opinion, or have Charlie act as a mediator. Give each character a different goal and see whether the conversation changes.
- **Change the topic or length.** Try `--topic "Should meetings be optional?"` and vary `--rounds`. A round contains one turn from each participant. Omit the topic to let Alex open the conversation.
- **Compare conversational models.** Choose supported model identifiers in `.env`. The Python runner's speaker-to-provider mapping and order are in `src/excite3_chatbot/conversation.py`; the notebook chooses providers in its participant cells. Restart the notebook kernel after changing `.env`.
- **Experiment interactively.** Run the notebook cells one at a time and inspect or edit the `conversation` list between turns. Rerunning the participant setup cell resets that list.
- **Adjust reply length.** The two-to-three-sentence instruction is added in `build_messages` in `src/excite3_chatbot/providers.py` and separately in the notebook's matching function. Change both if you want consistent behavior; models may not always follow the requested length.

Start with one or two rounds while experimenting: each participant turn sends a separate request, and model usage may be billed. Check the provider's current model list when choosing models, since identifiers in the example configuration can age out.

## Testing

Run `uv run python -m unittest discover -s tests -v` from the project root. The tests mock provider calls and do not use API credentials or make network requests.

## Development workflow

1. Create or update a notebook experiment.
2. Record assumptions, model/provider, parameters, and observed behavior in the notebook.
3. Move stable logic into `src/excite3_chatbot/`.
4. Update this README whenever the architecture, setup, prompts, dependencies, or behavior changes.
5. Run the relevant checks before committing.

## Documentation log

### 2026-11-20 — Experiment guide

- Added ideas for changing personalities, topics, models, conversation order, and reply length, plus the Python module command for systems that block the generated launcher.

### 2026-11-20 — Conversation readability

- Added an explicit opening request, concise-response instructions, and spacing between displayed turns in both implementations.
- Reject empty provider responses and report the finish reason; extended offline tests for message construction and presentation.

### 2026-11-20 — Python implementation

- Moved the notebook's participant prompts and OpenAI-compatible provider behavior into reusable Python modules.
- Added a command-line conversation runner with configurable rounds and an optional topic, plus offline tests for transcript construction and provider calls.

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

This project is available under the [MIT License](LICENSE).

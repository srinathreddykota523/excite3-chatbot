import unittest
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import Mock, patch

from excite3_chatbot.conversation import run_conversation
from excite3_chatbot.cli import main
from excite3_chatbot.providers import build_messages, call_model


class ConversationTests(unittest.TestCase):
    def test_messages_preserve_speakers_and_perspective(self):
        messages = build_messages("system", "Blake", [("Alex", "Hi"), ("Blake", "Hello"), ("Charlie", "Hey")])
        self.assertEqual(messages, [
            {"role": "system", "content": "system Keep each reply to two or three sentences, and never more than four."},
            {"role": "user", "content": "Alex: Hi"},
            {"role": "assistant", "content": "Hello"},
            {"role": "user", "content": "Charlie: Hey\n\nRespond next as Blake."},
        ])
        self.assertIn("Start the conversation as Alex", build_messages("system", "Alex", [])[-1]["content"])
        opening = build_messages("system", "Alex", [("Topic", "A topic")])[-1]["content"]
        self.assertIn("Topic: A topic", opening)
        self.assertIn("Start the conversation as Alex", opening)

    def test_notebook_message_builder_matches_python(self):
        notebook = json.loads(Path("notebooks/01_conversation_prototype.ipynb").read_text(encoding="utf-8"))
        cell = next(c for c in notebook["cells"] if "def build_messages(" in "".join(c.get("source", [])))
        namespace = {}
        exec("".join(cell["source"]), namespace)
        for history in ([], [("Topic", "An idea")], [("Alex", "Hello"), ("Blake", "Hi")]):
            self.assertEqual(namespace["build_messages"]("system", "Alex", history), build_messages("system", "Alex", history))

    def test_rounds_accumulate_context_in_order(self):
        calls = []

        def caller(provider, prompt, speaker, history):
            calls.append((speaker, provider, list(history)))
            return f"{speaker} reply"

        turns = list(run_conversation(2, "A topic", caller=caller))
        self.assertEqual([turn[0] for turn in turns], ["Alex", "Blake", "Charlie"] * 2)
        self.assertEqual([call[1] for call in calls[:3]], ["openai", "gemini", "groq"])
        self.assertEqual(calls[2][2], [("Topic", "A topic"), *turns[:2]])

    def test_provider_request_and_response(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test", "GEMINI_MODEL": "test-model"}), patch("excite3_chatbot.providers.OpenAI") as client:
            client.return_value.chat.completions.create.return_value.choices = [Mock(message=Mock(content="hello"))]
            self.assertEqual(call_model("gemini", "system", "Blake", []), "hello")
            self.assertEqual(client.call_args.kwargs["base_url"], "https://generativelanguage.googleapis.com/v1beta/openai/")
            self.assertEqual(client.return_value.chat.completions.create.call_args.kwargs["model"], "test-model")

    def test_invalid_rounds_and_missing_configuration(self):
        with self.assertRaises(ValueError):
            list(run_conversation(0))
        with patch.dict("os.environ", {}, clear=True), self.assertRaisesRegex(ValueError, "GROQ_API_KEY"):
            call_model("groq", "system", "Charlie", [])

    def test_empty_response_is_rejected(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test", "GEMINI_MODEL": "test-model"}), patch("excite3_chatbot.providers.OpenAI") as client:
            client.return_value.chat.completions.create.return_value.choices = [Mock(message=Mock(content="  "), finish_reason="length")]
            with self.assertRaisesRegex(ValueError, "empty response for Blake.*length"):
                call_model("gemini", "system", "Blake", [])

    def test_cli_separates_turns(self):
        output = io.StringIO()
        with patch("sys.argv", ["excite3-chatbot"]), patch("excite3_chatbot.cli.run_conversation", return_value=iter([("Alex", "Hi."), ("Blake", "Hello.")])), redirect_stdout(output):
            self.assertEqual(main(), 0)
        self.assertEqual(output.getvalue(), "Alex: Hi.\n\n\nBlake: Hello.\n\n\n")


if __name__ == "__main__":
    unittest.main()

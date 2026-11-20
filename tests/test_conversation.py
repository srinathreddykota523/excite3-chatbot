import unittest
from unittest.mock import Mock, patch

from excite3_chatbot.conversation import run_conversation
from excite3_chatbot.providers import build_messages, call_model


class ConversationTests(unittest.TestCase):
    def test_messages_preserve_speakers_and_perspective(self):
        messages = build_messages("system", "Blake", [("Alex", "Hi"), ("Blake", "Hello"), ("Charlie", "Hey")])
        self.assertEqual(messages, [
            {"role": "system", "content": "system"},
            {"role": "user", "content": "Alex: Hi"},
            {"role": "assistant", "content": "Hello"},
            {"role": "user", "content": "Charlie: Hey"},
        ])
        self.assertEqual(build_messages("system", "Alex", [])[-1]["content"], "Start the conversation as Alex.")

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


if __name__ == "__main__":
    unittest.main()

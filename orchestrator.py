from typing import Dict, Optional
from adapters.base import ModelAdapter
from conversation import Conversation

class Orchestrator:
    def __init__(self, adapters: Dict[str, ModelAdapter]):
        self.adapters = adapters
        self.conversation = Conversation()

    def get_available_models(self) -> Dict[str, ModelAdapter]:
        return self.adapters

    def process_prompt(self, model_key: str, user_input: str):
        adapter = self.adapters.get(model_key)
        if not adapter:
            print(f"Unknown model: {model_key}")
            return None

        self.conversation.add_user(user_input)
        full_response = ""
        try:
            print(f"\n🤖 {adapter.get_name()} is thinking...\n")
            for chunk in adapter.call(self.conversation.get_history()):
                print(chunk, end="", flush=True)
                full_response += chunk
            print()
            self.conversation.add_assistant(full_response)
            return full_response
        except Exception as e:
            if adapter.is_rate_limit_error(e):
                print(f"\n⚠️ Rate limit hit on {adapter.get_name()}.")
                self.conversation.messages.pop()
                fallback_model = self._prompt_fallback()
                if fallback_model:
                    print(f"🔄 Retrying with {self.adapters[fallback_model].get_name()}...")
                    return self.process_prompt(fallback_model, user_input)
                else:
                    print("❌ No fallback model available. Message lost.")
                    return None
            else:
                print(f"\n❌ Unexpected error: {e}")
                self.conversation.messages.pop()
                return None

    def _prompt_fallback(self) -> Optional[str]:
        print("\nSelect a fallback model:")
        available = list(self.adapters.keys())
        for idx, key in enumerate(available, 1):
            print(f"  {idx}. {self.adapters[key].get_name()}")
        print("  q. Quit")
        choice = input("> ").strip()
        if choice.lower() == 'q':
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                return available[idx]
        except ValueError:
            pass
        return None

import sys
from orchestrator import Orchestrator
from adapters.claude import ClaudeAdapter
from adapters.deepseek import DeepSeekAdapter
from adapters.qwen import QwenAdapter

def main():
    adapters = {
        "claude": ClaudeAdapter(),
        "deepseek": DeepSeekAdapter(),
        "qwen": QwenAdapter(),
    }

    orchestrator = Orchestrator(adapters)

    print("\n🧠 MCOL – Multi Code Orchestration Layer")
    print("Available models:")
    for key, adp in adapters.items():
        print(f"  {key}: {adp.get_name()}")
    print("Type 'quit' to exit, 'clear' to reset conversation.\n")

    while True:
        print("\nSelect model:")
        keys = list(adapters.keys())
        for i, key in enumerate(keys, 1):
            print(f"  {i}. {adapters[key].get_name()}")
        print("  q. Quit")
        choice = input("Model choice> ").strip()
        if choice.lower() == 'q':
            break
        try:
            idx = int(choice) - 1
            if not (0 <= idx < len(keys)):
                print("Invalid selection.\n")
                continue
            model_key = keys[idx]
        except ValueError:
            print("Invalid input. Enter a number.\n")
            continue

        user_input = input("\n💬 Your prompt: ").strip()
        if user_input.lower() in ('quit', 'exit'):
            break
        if user_input.lower() == 'clear':
            orchestrator.conversation.clear()
            print("Conversation cleared.\n")
            continue
        if not user_input:
            continue

        orchestrator.process_prompt(model_key, user_input)

if __name__ == "__main__":
    main()

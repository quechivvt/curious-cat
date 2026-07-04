from src.assistant import ask
from src.uploader import _get_or_create_store

def main():
    store_name = _get_or_create_store()
    print("OptiBot is ready. Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        answer = ask(question, store_name)

        print("\nOptiBot:")
        print(answer)
        print()

if __name__ == "__main__":
    main()
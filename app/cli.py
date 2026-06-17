import sys
from dotenv import load_dotenv

load_dotenv()


def main():
    from app.chain import build_chain

    print("RAG Document Chatbot — type 'exit' or Ctrl+C to quit\n")

    try:
        chain = build_chain()
    except Exception as e:
        print(f"Error initializing chain: {e}", file=sys.stderr)
        sys.exit(1)

    while True:
        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        answer = chain.invoke(question)
        print(f"\nAssistant: {answer}\n")


if __name__ == "__main__":
    main()

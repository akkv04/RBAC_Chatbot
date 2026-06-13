from engine.intent_engine import classify_intent
from engine.qa_engine import get_answer
from engine.rule_engine import diagnose
from engine.logger import log_interaction
import sys

def process_query(query: str) -> str:
    intent = classify_intent(query)

    # Use troubleshooting only when intent says troubleshooting
    if intent == "troubleshooting":
        diagnosis = diagnose(query)
        if diagnosis:
            response_lines = ["Possible Causes:"]
            for d in diagnosis:
                response_lines.append("- " + d)
            response = "\n".join(response_lines)
            log_interaction(query, intent, response)
            return response

    answer = get_answer(query)
    if answer:
        log_interaction(query, intent, answer)
        return answer

    response = " No match found"
    log_interaction(query, intent, response)
    return response


def run_bot():
    print("=== RBAC Bot CLI Mode ===")
    print("Type 'exit' to quit\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Exiting bot...")
            break

        response = process_query(query)
        print(response)
        print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(process_query(query))
    else:
        run_bot()
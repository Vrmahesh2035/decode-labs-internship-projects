"""
DecodeLabs - Project 1: Rule-Based AI Chatbot (Console Version)
Matches the exact spec: input loop, sanitization, dictionary knowledge base,
if-else/get() fallback, and a clean exit command.
"""

import random

responses = {
    "hello": "Hi there! How can I help you today?",
    "hi": "Hey! What's on your mind?",
    "how are you": "I'm just lines of code, but I'm running smoothly!",
    "name": "I'm RuleBot, your friendly rule-based assistant.",
    "help": "Try: hello, help, joke, name, thanks, bye.",
    "joke": "Why do programmers prefer dark mode? Because light attracts bugs!",
    "thanks": "You're welcome!",
}

exit_commands = {"bye", "exit", "quit"}


def get_response(user_input):
    clean_input = user_input.lower().strip()

    if clean_input in exit_commands:
        return None  # signal to stop the loop

    for key in responses:
        if key in clean_input:
            return responses[key]

    return "I do not understand that yet. Try 'help' for a list of things I know."


def main():
    print("RuleBot: Hi! I'm RuleBot. Type 'help' to see what I can do, or 'bye' to exit.")

    while True:                      # THE HEARTBEAT: infinite loop
        raw_input_ = input("You: ")
        reply = get_response(raw_input_)

        if reply is None:            # KILL COMMAND
            print("RuleBot: Goodbye!")
            break

        print(f"RuleBot: {reply}")


if __name__ == "__main__":
    main()

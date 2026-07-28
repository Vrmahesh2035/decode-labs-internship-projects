"""
DecodeLabs - Project 1: Rule-Based AI Chatbot
===============================================
A rule-based chatbot with a polished chat-app style GUI (built with Tkinter,
Python's built-in GUI toolkit -- no extra installs needed).

Core AI/CS concepts demonstrated (per the project brief):
  - Continuous input loop           -> the GUI event loop + on_send()
  - Input sanitization              -> .lower().strip()
  - Dictionary-based knowledge base -> O(1) lookup instead of if/elif ladder
  - Fallback handling                -> responses.get(key, fallback)
  - Clean exit strategy              -> 'bye' / 'exit' / 'quit' closes the app
"""

import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime
import random

# ----------------------------------------------------------------------
# 1) KNOWLEDGE BASE  (the "Logic Skeleton")
#    A dictionary is used instead of a long if-elif chain: O(1) lookup
#    that scales, instead of O(n) linear scanning through conditions.
# ----------------------------------------------------------------------
RESPONSES = {
    "hello":    ["Hi there! 👋 How can I help you today?", "Hello! Great to see you."],
    "hi":       ["Hey! What's on your mind?", "Hi! How can I assist you?"],
    "hey":      ["Hey there! 😊"],
    "how are you": ["I'm just lines of code, but I'm running smoothly! How about you?"],
    "name":     ["I'm RuleBot, your friendly rule-based assistant from DecodeLabs."],
    "who are you": ["I'm RuleBot — a simple, deterministic chatbot built for Project 1."],
    "help":     ["I can respond to greetings, tell you about myself, tell a joke, "
                 "or say goodbye. Try: hello, help, joke, name, thanks, bye."],
    "joke":     ["Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                 "Why did the AI cross the road? To avoid the local minimum."],
    "thanks":   ["You're welcome!", "Anytime! 🙌"],
    "thank you": ["You're most welcome!"],
    "what can you do": ["I match your message against a set of predefined rules "
                         "and reply instantly — no guessing, fully traceable."],
}

# Words that trigger a clean shutdown of the loop
EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "see you"}

FALLBACK_RESPONSES = [
    "I don't understand that yet — try typing 'help' to see what I can do.",
    "Hmm, that's outside my rule set. Type 'help' for a list of things I know.",
]


def get_bot_response(user_text: str) -> str:
    """
    Core decision-making logic (Phase 1 + Phase 2 of the IPO model):
      INPUT   -> sanitize (lower + strip)
      PROCESS -> dictionary lookup with .get() fallback (atomic op)
      OUTPUT  -> return the matched or fallback string
    """
    clean_input = user_text.lower().strip()

    if not clean_input:
        return "Say something — I'm listening!"

    if clean_input in EXIT_COMMANDS:
        return "__EXIT__"

    # exact match first
    if clean_input in RESPONSES:
        return random.choice(RESPONSES[clean_input])

    # soft/contains match, so "hello there" still triggers "hello"
    for key, replies in RESPONSES.items():
        if key in clean_input:
            return random.choice(replies)

    return random.choice(FALLBACK_RESPONSES)


# ----------------------------------------------------------------------
# 2) GUI  (the "White Box" interface)
# ----------------------------------------------------------------------
class ChatApp:
    BG           = "#0f172a"   # slate-900
    PANEL        = "#111827"   # gray-900
    BUBBLE_BOT   = "#1e293b"   # slate-800
    BUBBLE_USER  = "#4f46e5"   # indigo-600
    TEXT_LIGHT   = "#e5e7eb"
    TEXT_DIM     = "#94a3b8"
    ACCENT       = "#22d3ee"   # cyan-400

    def __init__(self, root):
        self.root = root
        root.title("RuleBot — DecodeLabs Project 1")
        root.geometry("460x640")
        root.minsize(380, 520)
        root.configure(bg=self.BG)

        self.msg_font = tkfont.Font(family="Segoe UI", size=11)
        self.small_font = tkfont.Font(family="Segoe UI", size=8)
        self.title_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")

        self._build_header()
        self._build_chat_area()
        self._build_input_area()

        self._bot_say("Hi! I'm RuleBot 🤖 — a rule-based chatbot. "
                       "Type 'help' to see what I can do, or 'bye' to exit.")

    # ---------- header ----------
    def _build_header(self):
        header = tk.Frame(self.root, bg=self.PANEL, height=64)
        header.pack(side="top", fill="x")
        header.pack_propagate(False)

        avatar = tk.Label(header, text="🤖", bg=self.ACCENT, fg="black",
                           font=("Segoe UI", 16), width=2, height=1)
        avatar.place(x=16, y=14, width=36, height=36)

        title = tk.Label(header, text="RuleBot", bg=self.PANEL, fg=self.TEXT_LIGHT,
                          font=self.title_font, anchor="w")
        title.place(x=64, y=10)

        subtitle = tk.Label(header, text="● Online · rule-based engine",
                             bg=self.PANEL, fg="#4ade80", font=self.small_font, anchor="w")
        subtitle.place(x=64, y=34)

    # ---------- chat area ----------
    def _build_chat_area(self):
        container = tk.Frame(self.root, bg=self.BG)
        container.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=self.BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.messages_frame = tk.Frame(self.canvas, bg=self.BG)

        self.messages_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scrollbar.pack(side="right", fill="y")

        # keep inner frame width synced to canvas width
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        # mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)      # Windows/mac
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))  # Linux
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------- input area ----------
    def _build_input_area(self):
        bar = tk.Frame(self.root, bg=self.PANEL, height=58)
        bar.pack(side="bottom", fill="x")
        bar.pack_propagate(False)

        self.entry = tk.Entry(bar, bg="#1f2937", fg=self.TEXT_LIGHT,
                               insertbackground=self.TEXT_LIGHT,
                               font=self.msg_font, relief="flat")
        self.entry.place(x=14, y=14, height=30, relwidth=1.0, width=-90)
        self.entry.bind("<Return>", lambda e: self.on_send())
        self.entry.focus_set()

        send_btn = tk.Button(bar, text="Send ➤", bg=self.ACCENT, fg="black",
                              activebackground="#67e8f9", relief="flat",
                              font=("Segoe UI", 10, "bold"),
                              command=self.on_send, cursor="hand2")
        send_btn.place(relx=1.0, x=-76, y=14, width=62, height=30)

    # ---------- message rendering ----------
    def _add_bubble(self, text, sender="bot"):
        row = tk.Frame(self.messages_frame, bg=self.BG)
        row.pack(fill="x", pady=4, padx=6, anchor="e" if sender == "user" else "w")

        bubble_bg = self.BUBBLE_USER if sender == "user" else self.BUBBLE_BOT
        fg = "white" if sender == "user" else self.TEXT_LIGHT
        anchor_side = "e" if sender == "user" else "w"
        justify = "right" if sender == "user" else "left"

        wrapper = tk.Frame(row, bg=self.BG)
        wrapper.pack(anchor=anchor_side)

        bubble = tk.Label(wrapper, text=text, bg=bubble_bg, fg=fg,
                           font=self.msg_font, wraplength=280, justify=justify,
                           padx=12, pady=8)
        bubble.pack(anchor=anchor_side)

        ts = tk.Label(wrapper, text=datetime.now().strftime("%H:%M"),
                      bg=self.BG, fg=self.TEXT_DIM, font=self.small_font)
        ts.pack(anchor=anchor_side, pady=(2, 0))

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def _bot_say(self, text):
        self._add_bubble(text, sender="bot")

    def _user_say(self, text):
        self._add_bubble(text, sender="user")

    # ---------- the loop's "heartbeat" ----------
    def on_send(self):
        user_text = self.entry.get()
        if user_text.strip() == "":
            return
        self._user_say(user_text)
        self.entry.delete(0, "end")

        reply = get_bot_response(user_text)

        if reply == "__EXIT__":
            self._bot_say("Goodbye! 👋 Closing the chat...")
            self.root.after(1200, self.root.destroy)   # clean break, like `break` in the while-loop
            return

        # tiny delay so the reply feels conversational, not instantaneous
        self.root.after(300, lambda: self._bot_say(reply))


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

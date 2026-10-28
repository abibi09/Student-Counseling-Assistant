
import re
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from collections import Counter

APP_NAME = "Student Counseling Assistant"

RESPONSES = {
    "greeting": (
        "Hello! 💙 I'm your Student Counseling Assistant.\n"
        "I can help with study planning, academic challenges, "
        "career exploration, motivation, and general stress management.\n\n"
        "What's on your mind today?"
    ),
    "study": (
        "Let's make studying more manageable! 📚\n\n"
        "• Choose one small topic to work on.\n"
        "• Study for 25 minutes, then take a 5-minute break.\n"
        "• Practise recalling what you learned without looking at your notes.\n"
        "• Take regular breaks and get enough sleep.\n\n"
        "Which subject or topic would you like to focus on?"
    ),
    "academic": (
        "Academic difficulties can feel overwhelming, but you can approach "
        "them one step at a time.\n\n"
        "1. Identify the exact topic you find difficult.\n"
        "2. Divide it into smaller sections.\n"
        "3. Ask a teacher or classmate about what you don't understand.\n"
        "4. Set one realistic goal for today.\n\n"
        "What is the main academic challenge you're facing?"
    ),
    "career": (
        "Career planning is a journey, not a one-time decision. 🌱\n\n"
        "Start by exploring:\n"
        "• Subjects and activities you enjoy.\n"
        "• Skills you want to develop.\n"
        "• Careers related to your interests.\n"
        "• Small projects, courses, or internships that let you explore.\n\n"
        "Which subjects or career areas interest you most?"
    ),
    "stress": (
        "I'm sorry things feel stressful right now. 💙 You deserve support.\n\n"
        "You could try pausing for a moment, relaxing your shoulders, "
        "taking a few slow comfortable breaths, and choosing one small "
        "thing you can manage right now.\n\n"
        "If stress continues or affects your daily life, consider speaking "
        "with a trusted person or qualified counsellor.\n\n"
        "Would you like to talk about what's making things difficult?"
    ),
    "motivation": (
        "You don't have to solve everything today. 🌟\n\n"
        "Progress can begin with one small action. Choose a task that takes "
        "just five minutes, start there, and give yourself credit for trying.\n\n"
        "What's one small thing you'd like to accomplish today?"
    ),
    "thanks": (
        "You're welcome! 💙 Remember that asking for support is a strength. "
        "I'm here to help you think through your next steps."
    ),
    "fallback": (
        "Thank you for sharing that with me. I may not fully understand yet.\n\n"
        "Could you tell me a little more? I can offer general support with "
        "study planning, academic challenges, career exploration, motivation, "
        "or stress management."
    ),
}

KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "study": ["study", "studying", "exam", "revision", "timetable", "schedule"],
    "academic": ["marks", "grades", "college", "subject", "assignment",
                 "fail", "failing", "difficult", "academic"],
    "career": ["career", "job", "internship", "future", "profession"],
    "stress": ["stress", "stressed", "anxious", "anxiety", "worried",
               "pressure", "overwhelmed", "sad", "lonely", "tired"],
    "motivation": ["motivate", "motivation", "lazy", "procrastinate",
                   "procrastination", "confidence", "give up"],
    "thanks": ["thanks", "thank you", "thankyou"],
}

POSITIVE_WORDS = {
    "happy", "good", "great", "excited", "confident", "calm",
    "motivated", "hopeful", "better", "grateful"
}
NEGATIVE_WORDS = {
    "sad", "bad", "stressed", "worried", "anxious", "angry",
    "lonely", "tired", "hopeless", "upset", "afraid", "overwhelmed"
}


def preprocess_text(text):
    """Lowercase text and extract words for simple NLP analysis."""
    return re.findall(r"\b[a-z']+\b", text.lower())


def analyze_sentiment(text):
    """A simple lexicon-based sentiment estimate, not a clinical assessment."""
    words = preprocess_text(text)
    positive = sum(word in POSITIVE_WORDS for word in words)
    negative = sum(word in NEGATIVE_WORDS for word in words)

    if positive > negative:
        label = "Positive"
    elif negative > positive:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "label": label,
        "positive_count": positive,
        "negative_count": negative,
    }


def detect_intent(text):
    """Classify a message using keyword matching."""
    words = set(preprocess_text(text))
    normalized = text.lower().strip()

    if any(phrase in normalized for phrase in KEYWORDS["greeting"]):
        return "greeting"

    scores = {}
    for intent, keywords in KEYWORDS.items():
        scores[intent] = sum(
            1 for keyword in keywords
            if " " in keyword and keyword in normalized
            or " " not in keyword and keyword in words
        )

    best_intent = max(scores, key=scores.get)
    if scores[best_intent] > 0:
        return best_intent

    return "fallback"


def get_response(text):
    intent = detect_intent(text)
    sentiment = analyze_sentiment(text)
    return RESPONSES[intent], intent, sentiment


class CounselingAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("760x650")
        self.root.minsize(600, 500)
        self.root.configure(bg="#eef3f8")

        self.message_count = 0
        self.intent_counts = Counter()

        header = tk.Frame(root, bg="#234e70", padx=18, pady=14)
        header.pack(fill="x")

        tk.Label(
            header, text="💙 Student Counseling Assistant",
            bg="#234e70", fg="white",
            font=("Arial", 19, "bold")
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Academic guidance • Career exploration • Student well-being",
            bg="#234e70", fg="#e2edf7",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(5, 0))

        self.chat = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state="disabled",
            font=("Arial", 11), padx=12, pady=12,
            bg="white", fg="#243447"
        )
        self.chat.pack(fill="both", expand=True, padx=14, pady=12)

        self.chat.tag_config("user", foreground="#174ea6",
                             font=("Arial", 11, "bold"))
        self.chat.tag_config("assistant", foreground="#176b4d",
                             font=("Arial", 11, "bold"))
        self.chat.tag_config("notice", foreground="#6b7280",
                             font=("Arial", 9, "italic"))

        input_frame = tk.Frame(root, bg="#eef3f8", padx=14, pady=8)
        input_frame.pack(fill="x")

        self.entry = tk.Entry(input_frame, font=("Arial", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.entry.bind("<Return>", self.send_message)

        tk.Button(
            input_frame, text="Send",
            command=self.send_message,
            bg="#234e70", fg="white",
            font=("Arial", 11, "bold"),
            padx=18, pady=8
        ).pack(side="left", padx=(8, 0))

        bottom = tk.Frame(root, bg="#eef3f8", padx=14, pady=8)
        bottom.pack(fill="x")

        tk.Button(
            bottom, text="Conversation Summary",
            command=self.show_summary
        ).pack(side="left")

        tk.Button(
            bottom, text="Clear Chat",
            command=self.clear_chat
        ).pack(side="right")

        self.add_message("Assistant", RESPONSES["greeting"])
        self.add_message(
            "Notice",
            "Educational support only; not a substitute for professional "
            "counselling or emergency services."
        )
        self.entry.focus_set()

    def add_message(self, sender, message, tag=None):
        self.chat.configure(state="normal")
        if tag:
            self.chat.insert(tk.END, sender + "\n", tag)
        elif sender == "You":
            self.chat.insert(tk.END, sender + "\n", "user")
        elif sender == "Notice":
            self.chat.insert(tk.END, sender + "\n", "notice")
        else:
            self.chat.insert(tk.END, sender + "\n", "assistant")

        self.chat.insert(tk.END, message + "\n\n")
        self.chat.configure(state="disabled")
        self.chat.see(tk.END)

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return

        self.entry.delete(0, tk.END)
        self.add_message("You", text)

        response, intent, sentiment = get_response(text)
        self.message_count += 1
        self.intent_counts[intent] += 1

        self.add_message("Assistant", response)
        self.add_message(
            "Notice",
            f"Text analysis: {sentiment['label']} | "
            f"Detected topic: {intent.replace('_', ' ').title()}"
        )

    def show_summary(self):
        if not self.message_count:
            summary = "No messages have been analysed yet."
        else:
            common = self.intent_counts.most_common(3)
            topics = ", ".join(
                f"{topic.replace('_', ' ')} ({count})"
                for topic, count in common
            )
            summary = (
                f"Messages analysed: {self.message_count}\n"
                f"Most detected topics: {topics}\n\n"
                "Sentiment results are simple word-based estimates and "
                "should not be treated as a diagnosis."
            )
        self.add_message("Conversation Summary", summary)

    def clear_chat(self):
        self.chat.configure(state="normal")
        self.chat.delete("1.0", tk.END)
        self.chat.configure(state="disabled")
        self.message_count = 0
        self.intent_counts.clear()
        self.add_message("Assistant", "Chat cleared. How can I help you today?")


if __name__ == "__main__":
    root = tk.Tk()
    app = CounselingAssistant(root)
    root.mainloop()

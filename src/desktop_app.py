import customtkinter as ctk
from tkinter import filedialog
import os
import io
from pypdf import PdfReader

# Your pipeline imports
from ingest import chunk_text
from embed_store import create_or_update_vector_store
from retrieve import retrieve
from llm import ask_llm

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class IntelAssistApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧠 IntelAssist - AI Knowledge Assistant")
        self.geometry("1100x700")

        # ===== Layout =====
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ===== Sidebar =====
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.title_label = ctk.CTkLabel(
            self.sidebar,
            text="IntelAssist",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=20)

        self.upload_btn = ctk.CTkButton(
            self.sidebar,
            text="📂 Upload Documents",
            command=self.upload_files
        )
        self.upload_btn.pack(pady=10, padx=10)

        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="Status: Ready",
            wraplength=200
        )
        self.status_label.pack(pady=20, padx=10)

        # ===== Main Area =====
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Query Input
        self.query_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Ask something...",
            height=40
        )
        self.query_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.ask_btn = ctk.CTkButton(
            self.main_frame,
            text="🔍 Generate Answer",
            command=self.generate_answer
        )
        self.ask_btn.grid(row=1, column=0, padx=10, pady=5)

        # Output Tabs
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.answer_tab = self.tabview.add("Answer")
        self.sources_tab = self.tabview.add("Sources / Chunks")

        # Answer Box
        self.answer_box = ctk.CTkTextbox(self.answer_tab, wrap="word")
        self.answer_box.pack(expand=True, fill="both", padx=10, pady=10)

        # Sources Box
        self.sources_box = ctk.CTkTextbox(self.sources_tab, wrap="word")
        self.sources_box.pack(expand=True, fill="both", padx=10, pady=10)

    # ===== Upload Logic =====
    def upload_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")]
        )

        if not files:
            return

        self.status_label.configure(text="Processing documents...")

        for filepath in files:
            filename = os.path.basename(filepath)

            # TXT
            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

            # PDF
            elif filename.endswith(".pdf"):
                reader = PdfReader(filepath)
                content = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"

            else:
                continue

            chunks = chunk_text(content, filename)
            create_or_update_vector_store(chunks)

        self.status_label.configure(text="Documents indexed successfully ✅")

    # ===== Query Logic =====
    def generate_answer(self):
        query = self.query_entry.get().strip()

        if not query:
            return

        self.status_label.configure(text="Retrieving answer...")

        results = retrieve(query)
        context = "\n".join([r["text"] for r in results])

        answer = ask_llm(context, query)

        # Display Answer
        self.answer_box.delete("1.0", "end")
        self.answer_box.insert("end", answer)

        # Display Sources
        self.sources_box.delete("1.0", "end")
        for r in results:
            self.sources_box.insert(
                "end",
                f"📄 {r['source']}\n{r['text']}\n\n{'-'*60}\n\n"
            )

        self.status_label.configure(text="Done ✅")


if __name__ == "__main__":
    app = IntelAssistApp()
    app.mainloop()
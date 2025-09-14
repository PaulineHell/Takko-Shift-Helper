import tkinter as tk
from tkinter import messagebox
import datetime

tasks = [
    {"time": "08:30", "task": "Tresor zählen", 
     "info": "Zähle den Tresor und notiere den Betrag im Protokoll.", 
     "anleitung": "Führe eine Bestandsaufnahme durch und dokumentiere die Ergebnisse."},
    {"time": "08:45", "task": "Kasse anmelden", 
     "info": "Melde dich an der Kasse an und prüfe die Reservierungsliste.", 
     "anleitung": "Nutze deine Personalkarte, öffne das Kassensystem und prüfe Reservierungen."},
    {"time": "08:55", "task": "Außenelemente aufbauen", 
     "info": "Werbefahnen und Aufsteller vor den Store stellen.", 
     "anleitung": "Platziere Werbefahnen links und rechts des Eingangs, Aufsteller mittig vor der Tür."}
]

spontane_aufgaben = {
    "📦 Ware kommt": {
        "Postpaket": "Nimm das Paket an, prüfe Absender und drucke die Belege.",
        "Trolli mit Return": "Prüfe Ware anhand des Lieferscheins, und übergieb den alten Trolli.",
        "Trolli ohne Return": "Prüfe Ware anhand des Lieferscheins, sortiere direkt ins Lager ein."
    },
    "💰 Geldtransport": {
        "Standard": "Bereite das Geld vor, dokumentiere den Betrag, übergib an Transporteur."
    },
    "🔄 Umtausch": {
        "Standard": "Scanne den Bon, prüfe Artikelzustand, biete Ersatz oder Rückzahlung an."
    },
    "🎫 Gutschein": {
        "Einlösen": "Scanne Gutschein, prüfe Betrag, bestätige im Kassensystem.",
        "Verkaufen": "Wähle Gutscheinverkauf, Betrag eingeben, kassieren."
    }
}

class ShiftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Takko Shift Helper 🧸")

        self.current_task = None
        self.done_tasks = []
        self.pending_tasks = tasks.copy()

        self.time_label = tk.Label(root, font=("Helvetica", 16))
        self.time_label.pack(pady=5)

        self.task_label = tk.Label(root, text="Keine aktuelle Aufgabe 💤", font=("Helvetica", 14))
        self.task_label.pack(pady=5)

        self.button_frame = tk.Frame(root)
        self.done_button = tk.Button(self.button_frame, text="✅ Erledigt", command=self.complete_task)
        self.help_button = tk.Button(self.button_frame, text="❓ Anleitung", command=self.show_instruction)
        self.done_button.pack(side="left", padx=5)
        self.help_button.pack(side="left", padx=5)

        self.idle_frame = tk.Frame(root)
        self.idle_label = tk.Label(self.idle_frame, text="🧸 Chill-Modus – keine aktuellen Aufgaben.", font=("Helvetica", 12))
        self.idle_label.pack(pady=2)
        self.next_task_label = tk.Label(self.idle_frame, text="", font=("Helvetica", 10), fg="gray")
        self.next_task_label.pack()

        self.done_label = tk.Label(root, text="Erledigte Aufgaben:", font=("Helvetica", 12, "bold"))
        self.done_listbox = tk.Listbox(root, width=60)

        self.spontan_button = tk.Button(root, text="📌 Spontane Aufgaben", command=self.open_spontane_aufgaben)
        self.spontan_button.pack(pady=5)

        self.update_time()

    def update_time(self):
        now = datetime.datetime.now().strftime("%H:%M")
        self.time_label.config(text=f"Uhrzeit: {now}")

        for task in self.pending_tasks:
            if now >= task["time"]:
                self.show_task(task)
                break
        else:
            self.show_idle()

        self.root.after(1000, self.update_time)

    def show_task(self, task):
        self.current_task = task
        self.task_label.config(text=f"⏰ {task['task']}")
        self.button_frame.pack(pady=5)
        self.idle_frame.pack_forget()
        self.done_label.pack_forget()
        self.done_listbox.pack_forget()

    def show_idle(self):
        self.current_task = None
        self.task_label.config(text="Keine aktuelle Aufgabe 💤")
        self.button_frame.pack_forget()

        future_tasks = [t for t in self.pending_tasks if t["time"] > datetime.datetime.now().strftime("%H:%M")]
        if future_tasks:
            next_task = min(future_tasks, key=lambda t: t["time"])
            self.next_task_label.config(text=f"Nächste Aufgabe: {next_task['time']} – {next_task['task']}")
        else:
            self.next_task_label.config(text="")

        self.idle_frame.pack(pady=5)
        self.done_label.pack(pady=2)
        self.done_listbox.pack(pady=2)

    def complete_task(self):
        if self.current_task:
            self.done_tasks.append(f"{self.current_task['time']} – {self.current_task['task']}")
            self.pending_tasks.remove(self.current_task)
            self.done_listbox.insert(tk.END, self.done_tasks[-1])
            self.current_task = None

    def show_instruction(self):
        if self.current_task:
            messagebox.showinfo("Anleitung", self.current_task["anleitung"])

    def open_spontane_aufgaben(self):
        win = tk.Toplevel(self.root)
        win.title("Spontane Aufgaben")

        tk.Label(win, text="Wähle eine Kategorie:", font=("Helvetica", 12, "bold")).pack(pady=5)

        for cat, sub in spontane_aufgaben.items():
            btn = tk.Button(win, text=cat, width=30, command=lambda c=cat: self.open_subtasks(win, c))
            btn.pack(pady=2)

    def open_subtasks(self, parent, category):
        for widget in parent.winfo_children():
            widget.destroy()

        tk.Label(parent, text=f"{category} – wähle eine Option:", font=("Helvetica", 12, "bold")).pack(pady=5)

        for sub_name, info in spontane_aufgaben[category].items():
            frame = tk.Frame(parent)
            tk.Label(frame, text=sub_name, font=("Helvetica", 11)).pack(side="left", padx=5)
            tk.Button(frame, text="📄 Anleitung", command=lambda i=info: messagebox.showinfo("Anleitung", i)).pack(side="left", padx=2)
            tk.Button(frame, text="✅ Erledigt", command=lambda s=sub_name, i=info: self.add_spontan_done(parent, s)).pack(side="left", padx=2)
            frame.pack(pady=2)

        tk.Button(parent, text="⬅ Zurück", command=lambda: self.back_to_main_spontan(parent)).pack(pady=5)

    def add_spontan_done(self, win, sub_name):
        time_now = datetime.datetime.now().strftime("%H:%M")
        self.done_tasks.append(f"{time_now} – {sub_name} (Spontan)")
        self.done_listbox.insert(tk.END, self.done_tasks[-1])

    def back_to_main_spontan(self, win):
        for widget in win.winfo_children():
            widget.destroy()
        self.open_spontane_aufgaben()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShiftApp(root)
    root.mainloop()
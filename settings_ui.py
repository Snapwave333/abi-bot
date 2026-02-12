import customtkinter as ctk
import os
from tkinter import messagebox
from dotenv import load_dotenv

# Set Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")

class SettingsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ABI Bot Settings")
        self.geometry("500x550")
        self.resizable(False, False)

        # Load current settings
        self.settings = self.load_settings()

        # Main Container (No Scrollbar)
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Configuration", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))

        self.entries = {}
        fields = [
            ("ESS_VENUE_ID", "Venue ID"),
            ("ESS_USERNAME", "ESS Username"),
            ("ESS_PASSWORD", "ESS Password"),
            ("GOOGLE_EMAIL", "Google Email"),
            ("GOOGLE_PASSWORD", "Google Password"),
            ("SYNC_INTERVAL_HOURS", "Sync Interval (Hours)"),
        ]

        # Field Container
        self.field_container = ctk.CTkFrame(self.main_frame)
        self.field_container.pack(fill="both", expand=True, pady=10, padx=5)

        for i, (key, display_name) in enumerate(fields):
            self.create_input_field(key, display_name, i == len(fields) - 1)

        # Buttons
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(pady=20, fill="x")

        # "2.5D" Style: Thick border, bold font, distinct colors
        self.save_btn = ctk.CTkButton(
            self.btn_frame, 
            text="SAVE SETTINGS", 
            command=self.save_settings, 
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            border_width=2,
            border_color="#2E86C1",
            fg_color="#3498DB",
            hover_color="#2980B9",
            corner_radius=25
        )
        self.save_btn.pack(side="left", padx=10, fill="x", expand=True)

        self.cancel_btn = ctk.CTkButton(
            self.btn_frame, 
            text="CANCEL", 
            command=self.destroy, 
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            border_width=2,
            border_color="#C0392B",
            fg_color="#E74C3C",
            hover_color="#C0392B",
            corner_radius=25
        )
        self.cancel_btn.pack(side="right", padx=10, fill="x", expand=True)

    def create_input_field(self, key, display_name, is_last):
        # Container
        row = ctk.CTkFrame(self.field_container, fg_color="transparent")
        row.pack(fill="x", pady=8, padx=10)

        # Label
        lbl = ctk.CTkLabel(row, text=display_name, anchor="w", width=140, font=ctk.CTkFont(size=14))
        lbl.pack(side="left", padx=5)

        # Entry
        ent = ctk.CTkEntry(row, placeholder_text=f"Enter {display_name}", height=35)
        ent.insert(0, self.settings.get(key, ""))
        
        if "PASSWORD" in key:
            ent.configure(show="*")
            
        ent.pack(side="right", fill="x", expand=True, padx=5)
        self.entries[key] = ent

    def load_settings(self):
        settings = {}
        if os.path.exists(ENV_PATH):
            with open(ENV_PATH, "r") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        settings[k] = v
        return settings

    def save_settings(self):
        new_content = ""
        for key, entry in self.entries.items():
            new_content += f"{key}={entry.get()}\n"
        
        try:
            with open(ENV_PATH, "w") as f:
                f.write(new_content)
            messagebox.showinfo("Success", "Settings saved successfully!\nRestart bot to apply changes.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

if __name__ == "__main__":
    app = SettingsApp()
    app.mainloop()

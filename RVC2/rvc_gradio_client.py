import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gradio_client import Client, handle_file
import threading
import webbrowser
import time
import os

class RVC_Ultimate_Studio:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate RVC Studio")
        self.root.geometry("650x750")
        
        self.server_url = "http://192.168.0.163:7860"
        self.client = None
        self.audio_url = ""
        self.voice_models = []
        
        self.create_widgets()
        self.root.after(500, self.connect_to_server)

    def create_widgets(self):
        main = ttk.Frame(self.root, padding="15")
        main.pack(fill="both", expand=True)
        
        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 10))
        self.status_label = ttk.Label(header, text="📡 Connecting...", font=("Arial", 10))
        self.status_label.pack(side="left")
        ttk.Button(header, text="🔄 Refresh Models", command=self.sync_models).pack(side="right")
        
        ttk.Separator(main, orient='horizontal').pack(fill="x", pady=10)

        # LOCAL FILE PICKER
        file_frame = ttk.LabelFrame(main, text="Select Local Audio File", padding="10")
        file_frame.pack(fill="x", pady=5)
        
        self.file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path, state="readonly").pack(fill="x", pady=5)
        ttk.Button(file_frame, text="📁 Browse", command=self.select_file).pack(pady=5)
        
        ttk.Separator(main, orient='horizontal').pack(fill="x", pady=10)

        # Voice Model Selection
        ttk.Label(main, text="Voice Model:", font=("Arial", 10)).pack(anchor="w", pady=(10,0))
        self.model_combo = ttk.Combobox(main, state="readonly")
        self.model_combo.pack(fill="x", pady=5)

        # Settings
        settings = ttk.LabelFrame(main, text="Settings", padding="10")
        settings.pack(fill="x", pady=10)
        
        pitch_frame = ttk.Frame(settings)
        pitch_frame.pack(fill="x", pady=5)
        ttk.Label(pitch_frame, text="Pitch Shift:").pack(side="left")
        self.pitch_var = tk.IntVar(value=0)
        ttk.Spinbox(pitch_frame, from_=-12, to=12, increment=1, textvariable=self.pitch_var, width=8).pack(side="left", padx=10)
        
        method_frame = ttk.Frame(settings)
        method_frame.pack(fill="x", pady=5)
        ttk.Label(method_frame, text="Pitch Method:").pack(side="left")
        self.algo_combo = ttk.Combobox(method_frame, values=["rmvpe", "crepe", "crepe-tiny", "fcpe"], width=12, state="readonly")
        self.algo_combo.set("rmvpe")
        self.algo_combo.pack(side="left", padx=10)
        
        format_frame = ttk.Frame(settings)
        format_frame.pack(fill="x", pady=5)
        ttk.Label(format_frame, text="Output Format:").pack(side="left")
        self.format_combo = ttk.Combobox(format_frame, values=["mp3", "wav", "flac"], width=8, state="readonly")
        self.format_combo.set("mp3")
        self.format_combo.pack(side="left", padx=10)

        self.generate_btn = ttk.Button(main, text="🎤 CONVERT", command=self.start_conversion)
        self.generate_btn.pack(fill="x", pady=10)

        self.progress = ttk.Progressbar(main, mode="indeterminate")
        self.progress.pack(fill="x", pady=5)

        self.log_text = tk.Text(main, height=12, bg="#1a1a1a", fg="#00FF41", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True, pady=5)

        self.audio_link = tk.Label(main, text="", fg="blue", cursor="hand2", font=("Arial", 9))
        self.audio_link.pack(pady=5)
        self.audio_link.bind("<Button-1>", lambda e: webbrowser.open(self.audio_url) if self.audio_url else None)

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Audio", "*.wav *.mp3 *.flac *.ogg")])
        if path:
            self.file_path.set(path)

    def log(self, msg):
        self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")
        self.root.update()

    def connect_to_server(self):
        def _connect():
            try:
                self.log(f"Connecting...")
                self.client = Client(self.server_url)
                self.log("✅ Connected!")
                self.sync_models()
            except Exception as e:
                self.log(f"❌ Connection error: {e}")
        threading.Thread(target=_connect, daemon=True).start()

    def sync_models(self):
        def _sync():
            try:
                self.log("Fetching models...")
                result = self.client.predict(api_name="/_init_dropdowns")
                
                self.voice_models = []
                if isinstance(result, tuple) and len(result) > 2:
                    third_item = result[2]
                    if isinstance(third_item, dict) and 'choices' in third_item:
                        for choice in third_item['choices']:
                            if isinstance(choice, list) and len(choice) > 0:
                                self.voice_models.append(choice[0])
                
                self.root.after(0, self._update_models)
                self.log(f"✅ Loaded {len(self.voice_models)} models")
                self.status_label.config(text="✅ Ready")
                    
            except Exception as e:
                self.log(f"❌ Sync error: {e}")
        
        threading.Thread(target=_sync, daemon=True).start()

    def _update_models(self):
        if self.voice_models:
            self.model_combo['values'] = self.voice_models
            self.model_combo.set(self.voice_models[0])

    def start_conversion(self):
        audio_path = self.file_path.get().strip()
        
        if not audio_path or not os.path.exists(audio_path):
            messagebox.showwarning("", "Please select a valid audio file")
            return
        
        if not self.model_combo.get():
            messagebox.showwarning("", "No model selected")
            return
        
        self.generate_btn.config(state="disabled", text="⏳ CONVERTING...")
        self.progress.start()
        threading.Thread(target=self.do_convert, daemon=True).start()

    def do_convert(self):
        try:
            audio_path = self.file_path.get().strip()
            model = self.model_combo.get()
            
            self.log(f"File: {os.path.basename(audio_path)}")
            self.log(f"Model: {model}")
            
            # Step 1: Set source type
            self.client.predict(visible_index="Local file", api_name="/partial")
            
            # Step 2: Upload file
            self.client.predict(x=handle_file(audio_path), api_name="/update_value")
            self.client.predict(x=handle_file(audio_path), api_name="/update_value")
            self.log("✅ File uploaded")
            
            # Step 3: Run conversion - THIS RETURNS 12 AUDIO FILES
            self.log("Converting...")
            result = self.client.predict(
                param_0=audio_path,
                param_1=model,
                param_2=int(self.pitch_var.get()),
                param_3=0,
                param_4=self.algo_combo.get(),
                param_5=0.3,
                param_6=1,
                param_7=0.33,
                param_8=False,
                param_9=False,
                param_10=1,
                param_11=False,
                param_12=155,
                param_13=False,
                param_14=0.7,
                param_15="contentvec",
                param_16=None,
                param_17=0,
                param_18=0.15,
                param_19=0.2,
                param_20=0.8,
                param_21=0.7,
                param_22=0,
                param_23=0,
                param_24=0,
                param_25=44100,
                param_26=self.format_combo.get(),
                param_27="",
                api_name="/partial_6"
            )
            
            # Step 4: Get partial_7 and partial_8 (may not be needed)
            self.client.predict(api_name="/partial_7")
            self.client.predict(api_name="/partial_8")
            
            # The result is a tuple of 12 audio file paths
            # Index 8 is "Converted vocals" according to API docs
            if result and isinstance(result, (list, tuple)) and len(result) > 8:
                output_file = result[8]  # Converted vocals
                if output_file and os.path.exists(output_file):
                    file_url = output_file.replace('\\', '/')
                    self.audio_url = "file:///" + file_url
                    self.log(f"✅ Conversion complete!")
                    self.root.after(0, lambda: self.audio_link.config(text="🎵 Click to play"))
                    webbrowser.open(self.audio_url)
                    return
            
            self.log(f"❌ Could not find output audio in result")
            if result:
                self.log(f"Result has {len(result) if isinstance(result, (list, tuple)) else 'unknown'} items")
            
        except Exception as e:
            self.log(f"❌ Error: {e}")
            import traceback
            self.log(traceback.format_exc())
        finally:
            self.root.after(0, lambda: self.generate_btn.config(state="normal", text="🎤 CONVERT"))
            self.root.after(0, lambda: self.progress.stop())

if __name__ == "__main__":
    root = tk.Tk()
    app = RVC_Ultimate_Studio(root)
    root.mainloop()
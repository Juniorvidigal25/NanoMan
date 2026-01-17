"""
NanoMan - UI Module
CustomTkinter user interface for API testing.
Part of the Nano Product Family.
"""

import customtkinter as ctk
import threading
import logging

from src.logic import validate_url, send_api_request, format_json, parse_headers

logger = logging.getLogger(__name__)

# Nano Design System
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

VERSION = "1.0.0"


class NanoManApp(ctk.CTk):
    """Main application window for NanoMan API client."""
    
    def __init__(self):
        super().__init__()
        
        # Window settings
        self.title(f"NanoMan v{VERSION} - Offline API Client")
        self.geometry("950x750")
        self.minsize(800, 600)
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.create_widgets()
        
        logger.info(f"NanoMan v{VERSION} started")
    
    def create_widgets(self):
        """Create all UI widgets."""
        
        # 1. Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        
        self.lbl_title = ctk.CTkLabel(
            self.header_frame, 
            text="NanoMan", 
            font=("Roboto", 24, "bold")
        )
        self.lbl_title.pack(side="left")
        
        self.lbl_subtitle = ctk.CTkLabel(
            self.header_frame, 
            text="No Cloud. No Bloat. Just Requests.",
            text_color="gray"
        )
        self.lbl_subtitle.pack(side="left", padx=15)
        
        self.lbl_family = ctk.CTkLabel(
            self.header_frame, 
            text="Nano Product Family",
            font=("Roboto", 10),
            text_color="#00CED1"
        )
        self.lbl_family.pack(side="right")
        
        # 2. Control bar (Method + URL + Send)
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, padx=20, pady=15, sticky="ew")
        self.control_frame.grid_columnconfigure(1, weight=1)
        
        # Method selector
        self.method_var = ctk.StringVar(value="GET")
        self.opt_method = ctk.CTkOptionMenu(
            self.control_frame, 
            values=["GET", "POST", "PUT", "PATCH", "DELETE"],
            variable=self.method_var, 
            width=100, 
            fg_color="#2c3e50",
            button_color="#34495e",
            button_hover_color="#3d566e"
        )
        self.opt_method.grid(row=0, column=0, padx=10, pady=10)
        
        # URL entry
        self.entry_url = ctk.CTkEntry(
            self.control_frame, 
            placeholder_text="Enter API URL (e.g., https://api.example.com/data)",
            height=40,
            font=("Consolas", 13)
        )
        self.entry_url.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry_url.insert(0, "https://chseets.com/api/meta.json")
        
        # Bind Enter key to send
        self.entry_url.bind("<Return>", lambda e: self.send_request_thread())
        
        # Send button
        self.btn_send = ctk.CTkButton(
            self.control_frame, 
            text="SEND",
            width=120,
            height=40,
            fg_color="#27ae60", 
            hover_color="#2ecc71",
            font=("Roboto", 14, "bold"),
            command=self.send_request_thread
        )
        self.btn_send.grid(row=0, column=2, padx=10, pady=10)
        
        # 3. Tabview for Request/Response
        self.tabview = ctk.CTkTabview(self, anchor="nw")
        self.tabview.grid(row=2, column=0, padx=20, pady=(5, 10), sticky="nsew")
        
        # Create tabs
        self.tab_response = self.tabview.add("Response")
        self.tab_body = self.tabview.add("Request Body")
        self.tab_headers = self.tabview.add("Headers")
        
        # Configure tab grids
        self.tab_response.grid_columnconfigure(0, weight=1)
        self.tab_response.grid_rowconfigure(0, weight=1)
        self.tab_body.grid_columnconfigure(0, weight=1)
        self.tab_body.grid_rowconfigure(0, weight=1)
        self.tab_headers.grid_columnconfigure(0, weight=1)
        self.tab_headers.grid_rowconfigure(0, weight=1)
        
        # Response tab
        self.txt_response = ctk.CTkTextbox(
            self.tab_response, 
            font=("Consolas", 13),
            wrap="word"
        )
        self.txt_response.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_response.insert("0.0", "// Response will appear here\n// Press SEND or Enter to make a request")
        
        # Request body tab
        self.txt_body = ctk.CTkTextbox(
            self.tab_body, 
            font=("Consolas", 13)
        )
        self.txt_body.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_body.insert("0.0", '{\n    "key": "value"\n}')
        
        # Headers tab
        self.txt_headers = ctk.CTkTextbox(
            self.tab_headers, 
            font=("Consolas", 13)
        )
        self.txt_headers.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.txt_headers.insert("0.0", "Content-Type: application/json")
        
        # 4. Status bar
        self.status_frame = ctk.CTkFrame(self, height=35, fg_color="transparent")
        self.status_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.lbl_status = ctk.CTkLabel(
            self.status_frame, 
            text="Ready. Enter a URL and press SEND.",
            anchor="w",
            font=("Roboto", 12)
        )
        self.lbl_status.pack(side="left", fill="x")
    
    def send_request_thread(self):
        """Start request in a separate thread to avoid UI freeze."""
        self.lbl_status.configure(text="Sending request...", text_color="orange")
        self.btn_send.configure(state="disabled", text="...")
        threading.Thread(target=self._execute_request, daemon=True).start()
    
    def _execute_request(self):
        """Execute the API request (runs in background thread)."""
        method = self.method_var.get()
        url = self.entry_url.get().strip()
        payload = self.txt_body.get("0.0", "end").strip()
        headers_text = self.txt_headers.get("0.0", "end").strip()
        
        # Parse headers
        headers = parse_headers(headers_text)
        
        # Only send payload for methods that support it
        if method == "GET":
            payload = None
        
        # Make request
        result = send_api_request(method, url, payload, headers)
        
        # Update UI (thread-safe via after)
        self.after(0, lambda: self._update_ui(result))
    
    def _update_ui(self, result: dict):
        """Update UI with request result."""
        self.btn_send.configure(state="normal", text="SEND")
        
        if result.get("success"):
            status_code = result["status_code"]
            reason = result["reason"]
            elapsed = result["elapsed_seconds"]
            
            # Color based on status
            if 200 <= status_code < 300:
                color = "#27ae60"  # Green
            elif 300 <= status_code < 400:
                color = "#f39c12"  # Orange
            else:
                color = "#e74c3c"  # Red
            
            self.lbl_status.configure(
                text=f"Status: {status_code} {reason} | Time: {elapsed:.3f}s",
                text_color=color
            )
            
            # Show response
            self.txt_response.delete("0.0", "end")
            self.txt_response.insert("0.0", result["body"])
            
            # Switch to response tab
            self.tabview.set("Response")
        else:
            # Error
            self.lbl_status.configure(
                text=f"Error: {result['error'][:80]}...",
                text_color="#e74c3c"
            )
            self.txt_response.delete("0.0", "end")
            self.txt_response.insert("0.0", f"Error:\n{result['error']}")
            self.tabview.set("Response")


def main():
    """Application entry point."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app = NanoManApp()
    app.mainloop()


if __name__ == "__main__":
    main()

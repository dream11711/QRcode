import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk

# Function to generate QR code dynamically
def generate_qr_code():
    data = entry.get().strip()
    if not data:
        panel.config(image="", bg=preview_bg)  # Clear preview
        save_button.config(state=tk.DISABLED)
        return

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=8,  # Adjusted box size for a smaller QR Code
            border=2,    # Reduced border for compactness
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.thumbnail((250, 250))  # Reduced QR Code preview size
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk, bg=preview_bg)
        panel.image = img_tk
        save_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate QR code:\n{e}")

# Function to save QR code
def save_qr_code():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
        title="Save QR Code"
    )
    if save_path:
        try:
            img = panel.image
            img._PhotoImage__photo.write(save_path)
            save_label.config(text=f"Saved at: {save_path}", fg=accent_color)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code:\n{e}")

# Function to reset app
def reset_app():
    entry.delete(0, tk.END)
    panel.config(image="", bg=preview_bg)
    save_button.config(state=tk.DISABLED)
    save_label.config(text="")

# Initialize the app
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("500x700")
root.configure(bg="#202124")

# Add scrollbar support
canvas = tk.Canvas(root, bg="#202124", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

scrollable_frame = tk.Frame(canvas, bg="#202124")
scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

canvas.configure(yscrollcommand=scrollbar.set)

# Update scroll region and center content
def update_scroll_region(event=None):
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas_width = canvas.winfo_width()
    canvas.itemconfig(scrollable_window, width=canvas_width)

scrollable_frame.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", update_scroll_region)

# Color Palette
bg_color = "#202124"
card_bg = "#202124"
accent_color = "#00FFD1"
preview_bg = "#202124"
button_hover_color = "#3B4048"
text_color = "#FFFFFF"
font_family = "Segoe UI"

# Header
header = tk.Label(
    scrollable_frame,
    text="QR Code Generator",
    font=(font_family, 18, "bold"),
    fg=accent_color,
    bg=bg_color,
)
header.pack(pady=10)

# Input Section
input_frame = tk.Frame(scrollable_frame, bg=card_bg, relief="flat", bd=5)
input_frame.pack(pady=10, padx=20, fill="x")

entry_label = tk.Label(
    input_frame,
    text="Enter Text or URL:",
    font=(font_family, 12),
    fg=text_color,
    bg=card_bg,
)
entry_label.pack(pady=5)

entry = tk.Entry(
    input_frame,
    font=(font_family, 12),
    width=30,
    relief="flat",
    bg=preview_bg,
    fg=text_color,
    insertbackground=text_color,
    highlightthickness=1,
    highlightcolor=accent_color,
    highlightbackground=card_bg
)
entry.pack(pady=5)
entry.bind("<KeyRelease>", lambda event: generate_qr_code())

# Buttons Section
button_frame = tk.Frame(scrollable_frame, bg=bg_color)
button_frame.pack(pady=10)

def on_hover(button):
    button.config(bg=button_hover_color)

def off_hover(button):
    button.config(bg=card_bg)

save_button = tk.Button(
    button_frame,
    text="Save QR Code",
    font=(font_family, 12, "bold"),
    bg=card_bg,
    fg=text_color,
    width=12,
    relief="flat",
    cursor="hand2",
    state=tk.DISABLED,
    command=save_qr_code,
)
save_button.grid(row=0, column=0, padx=10)
save_button.bind("<Enter>", lambda e: on_hover(save_button))
save_button.bind("<Leave>", lambda e: off_hover(save_button))

reset_button = tk.Button(
    button_frame,
    text="Reset",
    font=(font_family, 12, "bold"),
    bg="#D32F2F",
    fg=text_color,
    width=12,
    relief="flat",
    cursor="hand2",
    command=reset_app,
)
reset_button.grid(row=0, column=1, padx=10)

# QR Code Preview Section
preview_label = tk.Label(
    scrollable_frame,
    text="QR Code Preview",
    font=(font_family, 14, "bold"),
    fg=accent_color,
    bg=bg_color,
)
preview_label.pack(pady=5)

panel = tk.Label(scrollable_frame, bg=preview_bg, width=250, height=250, relief="flat", bd=5)
panel.pack(pady=5)

# Save Status
save_label = tk.Label(
    scrollable_frame,
    text="",
    font=(font_family, 10),
    fg=text_color,
    bg=bg_color,
)
save_label.pack(pady=5)

# Footer with Branding
footer = tk.Label(
    scrollable_frame,
    text="© 2025 | QR Code Generator | Designed by Abdulaziz Alrabiah",
    font=(font_family, 10, "italic"),
    fg=accent_color,
    bg=bg_color,
)
footer.pack(pady=10)

# Run the App
root.mainloop()

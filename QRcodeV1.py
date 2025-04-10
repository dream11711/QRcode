import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import qrcode
from PIL import Image, ImageTk


class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root

        # Initial language setting: 'ar' for Arabic, 'en' for English
        self.language = 'ar'

        # Set a slightly smaller fixed window size
        self.root.geometry("650x900")
        self.root.resizable(False, False)

        # Dark theme only
        self.bg_color = "#202124"
        self.card_bg = "#202124"
        self.text_color = "#FFFFFF"
        self.accent_color = "#00FFD1"
        self.preview_bg = "#202124"
        self.button_hover_color = "#3B4048"
        self.root.configure(bg=self.bg_color)

        # Default customization
        self.fill_color = "black"
        self.back_color = "white"
        self.logo = None  # PIL image for the logo
        self.after_id = None  # For debouncing
        self.qr_image = None  # The generated QR image

        # Translations for Arabic and English
        # You can tweak these texts as needed
        self.translations = {
            'ar': {
                'app_title': "مولد رمز الاستجابة السريعة",
                'header': "مولد رمز الاستجابة السريعة",
                'entry_label': "أدخل النص أو الرابط:",
                'custom_title': "خيارات التخصيص:",
                'ec_label': "تصحيح الخطأ:",
                'ec_info_btn': "معلومات تصحيح الخطأ",
                'fill_color_label': "لون التعبئة:",
                'back_color_label': "لون الخلفية:",
                'logo_label': "إدراج شعار (اختياري):",
                'logo_btn': "اختيار شعار",
                'logo_clear_btn': "إزالة الشعار",
                'save_btn': "حفظ رمز QR",
                'reset_btn': "إعادة تعيين",
                'preview_title': "معاينة رمز QR:",
                'save_status': "",
                'footer': "© 2025 | مولد رمز الاستجابة السريعة | تصميم: عبدالعزيز الربيعه",
                'ec_info_title': "مستويات تصحيح الخطأ",
                'ec_info_text': (
                    "هناك أربعة مستويات لتصحيح الأخطاء في رموز QR:\n\n"
                    "• L (منخفض): يحمي حوالي 7% من البيانات\n"
                    "• M (متوسط): يحمي حوالي 15% من البيانات\n"
                    "• Q (عالي): يحمي حوالي 25% من البيانات\n"
                    "• H (عالي جدًا): يحمي حوالي 30% من البيانات\n\n"
                    "ملاحظة: كلما زاد مستوى الحماية زاد حجم الرمز."
                ),
                'choose_fill_color': "اختر لون التعبئة",
                'choose_back_color': "اختر لون الخلفية",
                'choose_logo_error': "فشل في تحميل الشعار",
                'generate_error': "فشل في إنشاء رمز QR",
                'embed_logo_error': "فشل في إدراج الشعار",
                'save_dialog_title': "حفظ رمز QR",
                'save_dialog_png': "ملفات PNG",
                'save_failed': "فشل في حفظ رمز QR",
                'logo_chosen': "تم اختيار الشعار",
                'logo_cleared': "تم إزالة الشعار",
                'reset_text': "",
                'ec_explain_btn': "تغيير اللغة",
            },
            'en': {
                'app_title': "QR Code Generator",
                'header': "QR Code Generator",
                'entry_label': "Enter text or URL:",
                'custom_title': "Customization Options:",
                'ec_label': "Error Correction:",
                'ec_info_btn': "EC Info",
                'fill_color_label': "Fill Color:",
                'back_color_label': "Background Color:",
                'logo_label': "Embed Logo (optional):",
                'logo_btn': "Select Logo",
                'logo_clear_btn': "Clear Logo",
                'save_btn': "Save QR Code",
                'reset_btn': "Reset",
                'preview_title': "QR Code Preview:",
                'save_status': "",
                'footer': "© 2025 | QR Code Generator | Designed by Abdulaziz Alrabiah",
                'ec_info_title': "Error Correction Levels",
                'ec_info_text': (
                    "QR Codes have four error correction levels:\n\n"
                    "• L (Low): ~7% data protection\n"
                    "• M (Medium): ~15% data protection\n"
                    "• Q (Quartile): ~25% data protection\n"
                    "• H (High): ~30% data protection\n\n"
                    "Note: Higher protection means a larger QR code."
                ),
                'choose_fill_color': "Select Fill Color",
                'choose_back_color': "Select Background Color",
                'choose_logo_error': "Failed to load logo",
                'generate_error': "Failed to generate QR code",
                'embed_logo_error': "Failed to embed logo",
                'save_dialog_title': "Save QR Code",
                'save_dialog_png': "PNG Files",
                'save_failed': "Failed to save QR code",
                'logo_chosen': "Logo selected",
                'logo_cleared': "Logo cleared",
                'reset_text': "",
                'ec_explain_btn': "Switch Language",
            }
        }

        # Build the UI and set initial texts
        self.build_ui()
        self.update_texts()

    def build_ui(self):
        # Header
        self.header_label = tk.Label(
            self.root,
            font=("Segoe UI", 20, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.header_label.pack(pady=10)

        # URL/Text Entry
        self.input_frame = tk.Frame(self.root, bg=self.card_bg, bd=5)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.entry_label = tk.Label(
            self.input_frame,
            font=("Segoe UI", 12),
            fg=self.text_color,
            bg=self.card_bg
        )
        self.entry_label.pack(pady=5)

        # Updated the entry widget with 'groove' relief and a thicker border to enhance visibility
        self.entry = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 12),
            width=50,
            relief="groove",
            bd=2,
            bg=self.preview_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            highlightthickness=2,
            highlightcolor=self.accent_color,
            highlightbackground=self.card_bg
        )
        self.entry.pack(pady=5)
        self.entry.bind("<KeyRelease>", self.debounced_generate_qr_code)

        # Customization frame
        self.custom_frame = tk.Frame(self.root, bg=self.card_bg, bd=3, relief="raised")
        self.custom_frame.pack(pady=10, padx=20, fill="x")

        self.custom_title = tk.Label(
            self.custom_frame,
            font=("Segoe UI", 14, "bold"),
            fg=self.accent_color,
            bg=self.card_bg
        )
        self.custom_title.pack(pady=5)

        # Error Correction
        ec_frame = tk.Frame(self.custom_frame, bg=self.card_bg)
        ec_frame.pack(pady=5, padx=5, fill="x")
        self.ec_label = tk.Label(ec_frame, font=("Segoe UI", 12), fg=self.text_color, bg=self.card_bg)
        self.ec_label.pack(side="left", padx=5)

        self.ec_var = tk.StringVar(value="L")
        self.ec_dropdown = ttk.Combobox(
            ec_frame, textvariable=self.ec_var, values=["L", "M", "Q", "H"],
            state="readonly", width=5
        )
        self.ec_dropdown.pack(side="left", padx=5)
        self.ec_dropdown.bind("<<ComboboxSelected>>", lambda e: self.generate_qr_code())

        # Button to explain EC levels
        self.ec_info_button = tk.Button(
            ec_frame, font=("Segoe UI", 10), bg=self.card_bg,
            fg=self.text_color, relief="flat", cursor="hand2",
            command=self.show_ec_info
        )
        self.ec_info_button.pack(side="left", padx=10)

        # Fill Color
        fc_frame = tk.Frame(self.custom_frame, bg=self.card_bg)
        fc_frame.pack(pady=5, padx=5, fill="x")
        self.fill_color_label = tk.Label(fc_frame, font=("Segoe UI", 12), fg=self.text_color, bg=self.card_bg)
        self.fill_color_label.pack(side="left", padx=5)

        self.fill_color_button = tk.Button(
            fc_frame, font=("Segoe UI", 12),
            bg=self.card_bg, fg=self.text_color, relief="flat",
            cursor="hand2", command=self.choose_fill_color
        )
        self.fill_color_button.pack(side="left", padx=5)

        # Background Color
        bc_frame = tk.Frame(self.custom_frame, bg=self.card_bg)
        bc_frame.pack(pady=5, padx=5, fill="x")
        self.back_color_label = tk.Label(bc_frame, font=("Segoe UI", 12), fg=self.text_color, bg=self.card_bg)
        self.back_color_label.pack(side="left", padx=5)

        self.back_color_button = tk.Button(
            bc_frame, font=("Segoe UI", 12), bg=self.card_bg,
            fg=self.text_color, relief="flat", cursor="hand2",
            command=self.choose_back_color
        )
        self.back_color_button.pack(side="left", padx=5)

        # Logo Selection
        logo_frame = tk.Frame(self.custom_frame, bg=self.card_bg)
        logo_frame.pack(pady=5, padx=5, fill="x")
        self.logo_label = tk.Label(logo_frame, font=("Segoe UI", 12), fg=self.text_color, bg=self.card_bg)
        self.logo_label.pack(side="left", padx=5)

        self.logo_button = tk.Button(
            logo_frame, font=("Segoe UI", 12), bg=self.card_bg,
            fg=self.text_color, relief="flat", cursor="hand2",
            command=self.select_logo
        )
        self.logo_button.pack(side="left", padx=5)

        self.clear_logo_button = tk.Button(
            logo_frame, font=("Segoe UI", 12), bg=self.card_bg,
            fg=self.text_color, relief="flat", cursor="hand2",
            command=self.clear_logo
        )
        self.clear_logo_button.pack(side="left", padx=5)

        # Action Buttons (Save, Reset, Language Toggle)
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        self.save_button = tk.Button(
            self.button_frame, font=("Segoe UI", 12, "bold"),
            bg=self.card_bg, fg=self.text_color, width=14,
            relief="flat", cursor="hand2", state=tk.DISABLED,
            command=self.save_qr_code
        )
        self.save_button.grid(row=0, column=0, padx=10)
        self.save_button.bind("<Enter>", lambda e: self.on_hover(self.save_button))
        self.save_button.bind("<Leave>", lambda e: self.off_hover(self.save_button))

        self.reset_button = tk.Button(
            self.button_frame, font=("Segoe UI", 12, "bold"),
            bg="#D32F2F", fg=self.text_color, width=14,
            relief="flat", cursor="hand2", command=self.reset_app
        )
        self.reset_button.grid(row=0, column=1, padx=10)

        # Enhanced Language Toggle Button (New Button) - make it more visible
        self.language_button = tk.Button(
            self.button_frame, font=("Segoe UI", 12, "bold"),
            bg=self.accent_color, fg=self.bg_color, width=14,
            relief="flat", cursor="hand2", command=self.toggle_language
        )
        self.language_button.grid(row=0, column=2, padx=10)

        # QR Code Preview
        self.preview_title = tk.Label(
            self.root,
            font=("Segoe UI", 14, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.preview_title.pack(pady=5)

        self.preview_panel = tk.Label(
            self.root,
            bg=self.preview_bg,
            width=250,
            height=250,
            relief="flat",
            bd=5
        )
        self.preview_panel.pack(pady=5)

        # Save Status
        self.save_status_label = tk.Label(
            self.root,
            font=("Segoe UI", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.save_status_label.pack(pady=5)

        # Footer
        self.footer_label = tk.Label(
            self.root,
            font=("Segoe UI", 10, "italic"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.footer_label.pack(pady=10)

    def update_texts(self):
        """Update all labels, buttons, etc. based on the current language."""
        t = self.translations[self.language]

        # Window title
        self.root.title(t['app_title'])

        # Header
        self.header_label.config(text=t['header'])

        # Entry label
        self.entry_label.config(text=t['entry_label'])

        # Custom frame title
        self.custom_title.config(text=t['custom_title'])

        # Error Correction
        self.ec_label.config(text=t['ec_label'])
        self.ec_info_button.config(text=t['ec_info_btn'])

        # Fill Color
        self.fill_color_label.config(text=t['fill_color_label'])
        self.fill_color_button.config(text=self.fill_color)

        # Back Color
        self.back_color_label.config(text=t['back_color_label'])
        self.back_color_button.config(text=self.back_color)

        # Logo section
        self.logo_label.config(text=t['logo_label'])
        self.logo_button.config(text=t['logo_btn'])
        self.clear_logo_button.config(text=t['logo_clear_btn'])

        # Save and Reset buttons
        self.save_button.config(text=t['save_btn'])
        self.reset_button.config(text=t['reset_btn'])

        # Language toggle button (its text remains from translation toggle)
        self.language_button.config(text=t['ec_explain_btn'])

        # Preview title
        self.preview_title.config(text=t['preview_title'])

        # Save status
        self.save_status_label.config(text=t['save_status'])

        # Footer
        self.footer_label.config(text=t['footer'])

    def on_hover(self, button):
        button.config(bg=self.button_hover_color)

    def off_hover(self, button):
        button.config(bg=self.card_bg)

    def toggle_language(self):
        """Toggle between Arabic and English."""
        self.language = 'en' if self.language == 'ar' else 'ar'
        self.update_texts()
        # Regenerate QR if there is data
        if self.entry.get().strip():
            self.generate_qr_code()

    def show_ec_info(self):
        """Show a popup explaining the EC levels in the current language."""
        t = self.translations[self.language]
        messagebox.showinfo(t['ec_info_title'], t['ec_info_text'])

    def choose_fill_color(self):
        t = self.translations[self.language]
        color_tuple = colorchooser.askcolor(title=t['choose_fill_color'], initialcolor=self.fill_color)
        if color_tuple[1]:
            self.fill_color = color_tuple[1]
            self.fill_color_button.config(text=self.fill_color)
            self.generate_qr_code()

    def choose_back_color(self):
        t = self.translations[self.language]
        color_tuple = colorchooser.askcolor(title=t['choose_back_color'], initialcolor=self.back_color)
        if color_tuple[1]:
            self.back_color = color_tuple[1]
            self.back_color_button.config(text=self.back_color)
            self.generate_qr_code()

    def select_logo(self):
        t = self.translations[self.language]
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.logo = Image.open(file_path).convert("RGBA")
                self.save_status_label.config(text=t['logo_chosen'], fg=self.accent_color)
                self.generate_qr_code()
            except Exception as e:
                messagebox.showerror("Error", f"{t['choose_logo_error']}:\n{e}")
                self.logo = None

    def clear_logo(self):
        t = self.translations[self.language]
        self.logo = None
        self.save_status_label.config(text=t['logo_cleared'], fg=self.accent_color)
        self.generate_qr_code()

    def debounced_generate_qr_code(self, event):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.after_id = self.root.after(300, self.generate_qr_code)

    def generate_qr_code(self):
        data = self.entry.get().strip()
        if not data:
            self.clear_preview()
            return
        t = self.translations[self.language]
        try:
            ec_mapping = {
                "L": qrcode.constants.ERROR_CORRECT_L,
                "M": qrcode.constants.ERROR_CORRECT_M,
                "Q": qrcode.constants.ERROR_CORRECT_Q,
                "H": qrcode.constants.ERROR_CORRECT_H
            }
            error_correction = ec_mapping.get(self.ec_var.get(), qrcode.constants.ERROR_CORRECT_L)
            qr = qrcode.QRCode(
                version=1,
                error_correction=error_correction,
                box_size=10,
                border=2,
            )
            qr.add_data(data)
            qr.make(fit=True)
            self.qr_image = qr.make_image(fill_color=self.fill_color, back_color=self.back_color).convert("RGBA")
            if self.logo:
                self.qr_image = self.embed_logo(self.qr_image)
            preview_image = self.qr_image.copy()
            preview_image.thumbnail((250, 250))
            self.img_tk = ImageTk.PhotoImage(preview_image)
            self.preview_panel.config(image=self.img_tk)
            self.preview_panel.image = self.img_tk
            self.save_button.config(state=tk.NORMAL)
            self.save_status_label.config(text="")
        except Exception as e:
            messagebox.showerror("Error", f"{t['generate_error']}:\n{e}")
            self.clear_preview()

    def embed_logo(self, qr_img):
        t = self.translations[self.language]
        if not self.logo:
            return qr_img
        try:
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width * 0.2)
            logo = self.logo.copy()
            try:
                from PIL import Resampling
                RESAMPLE_MODE = Resampling.LANCZOS
            except ImportError:
                try:
                    RESAMPLE_MODE = Image.LANCZOS
                except AttributeError:
                    RESAMPLE_MODE = Image.BICUBIC
            logo.thumbnail((logo_size, logo_size), RESAMPLE_MODE)
            pos = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)
            qr_img.paste(logo, pos, logo)
        except Exception as e:
            messagebox.showerror("Error", f"{t['embed_logo_error']}:\n{e}")
        return qr_img

    def save_qr_code(self):
        t = self.translations[self.language]
        if self.qr_image is None:
            return
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[(t['save_dialog_png'], "*.png"), ("All Files", "*.*")],
            title=t['save_dialog_title']
        )
        if save_path:
            try:
                self.qr_image.save(save_path)
                self.save_status_label.config(text=f"{t['save_status']} {save_path}", fg=self.accent_color)
            except Exception as e:
                messagebox.showerror("Error", f"{t['save_failed']}:\n{e}")

    def reset_app(self):
        t = self.translations[self.language]
        self.entry.delete(0, tk.END)
        self.ec_var.set("L")
        self.fill_color = "black"
        self.back_color = "white"
        self.fill_color_button.config(text=self.fill_color)
        self.back_color_button.config(text=self.back_color)
        self.logo = None
        self.clear_preview()
        self.save_status_label.config(text=t['reset_text'])

    def clear_preview(self):
        self.preview_panel.config(image="", bg=self.preview_bg)
        self.save_button.config(state=tk.DISABLED)
        self.qr_image = None


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()

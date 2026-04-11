import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

qr_img = None

def generate_qr():
    global qr_img

    data = text.get("1.0", "end").strip()
    if not data:
        return messagebox.showerror("Error", "Enter text or URL!")

    try:
        # 🔥 Advanced QR settings (important fix)
        qr = qrcode.QRCode(
            version=None,  # auto size
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # high correction
            box_size=10,  # quality
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Preview resize (display only)
        preview_img = qr_img.resize((250, 250), Image.LANCZOS)
        img = ImageTk.PhotoImage(preview_img)

        preview.config(image=img, text="")
        preview.image = img

        status.config(text="QR Generated ✔", fg="green")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def save_qr():
    if not qr_img:
        return messagebox.showwarning("Warning", "Generate QR first!")

    path = filedialog.asksaveasfilename(defaultextension=".png")
    if path:
        qr_img.save(path)
        status.config(text="Saved ✔", fg="blue")


def clear():
    global qr_img
    qr_img = None
    text.delete("1.0", "end")
    preview.config(image="", text="Preview")
    status.config(text="Cleared", fg="orange")


# UI
root = tk.Tk()
root.title("QR Generator")
root.geometry("700x450")

tk.Label(root, text="QR Code Generator", font=("Arial", 16, "bold")).pack(pady=10)

text = tk.Text(root, height=5, width=40)
text.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack()

for t, c, f in [
    ("Generate", "#2563eb", generate_qr),
    ("Save", "#16a34a", save_qr),
    ("Clear", "#dc2626", clear)
]:
    tk.Button(btn_frame, text=t, bg=c, fg="white", width=12, command=f).pack(side="left", padx=5)

preview = tk.Label(root, text="Preview", bg="#ddd", width=30, height=10)
preview.pack(pady=15)

status = tk.Label(root, text="Ready", fg="gray")
status.pack()

root.mainloop()
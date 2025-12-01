import tkinter as tk
from tkinter import filedialog, messagebox
from crypto import aes_encrypt, aes_decrypt, rsa_encrypt, rsa_decrypt, rsa_generate_keys
from steg import hide_data_random, extract_data_random
from utils import generate_aes_key, decode_aes_key
from qr_gen import generate_qr
import base64
import os

class CryptoStegApp:
    def __init__(self, master):
        self.master = master
        master.title("CryptoSteg Enhanced")
        master.geometry("600x500")
        master.configure(bg="#2e2e2e")

        tk.Label(master, text="CryptoSteg Enhanced Secure Messenger", font=("Arial", 18), fg="white", bg="#2e2e2e").pack(pady=10)

        tk.Label(master, text="Message or Text File:", fg="white", bg="#2e2e2e").pack()
        self.message_entry = tk.Text(master, height=4, bg="#3e3e3e", fg="white")
        self.message_entry.pack(pady=5)

        tk.Button(master, text="Select Image", bg="#555555", fg="white", command=self.select_image).pack(pady=5)
        tk.Button(master, text="Encrypt + Hide (AES)", bg="#1f7a1f", fg="white", command=lambda: self.encrypt_hide("AES")).pack(pady=5)
        tk.Button(master, text="Encrypt + Hide (RSA)", bg="#1f7a1f", fg="white", command=lambda: self.encrypt_hide("RSA")).pack(pady=5)
        tk.Button(master, text="Extract + Decrypt", bg="#7a1f1f", fg="white", command=self.extract_decrypt).pack(pady=5)

        tk.Label(master, text="Key / Private Key:", fg="white", bg="#2e2e2e").pack(pady=5)
        self.key_entry = tk.Entry(master, width=70, bg="#3e3e3e", fg="white")
        self.key_entry.pack(pady=5)

        self.image_path = ""

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        messagebox.showinfo("Selected", f"Image Selected:\n{self.image_path}")

    def encrypt_hide(self, method):
        if not self.image_path:
            messagebox.showwarning("Error", "Select an image first!")
            return
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Error", "Enter a message!")
            return
        if method == "AES":
            key_str = generate_aes_key()
            key = decode_aes_key(key_str)
            encrypted = aes_encrypt(message, key)
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key_str)
        else:  # RSA
            private_key, public_key = rsa_generate_keys()
            encrypted = rsa_encrypt(message, public_key)
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, private_key.decode())

        out_image = "encoded_image.png"
        hide_data_random(self.image_path, out_image, encrypted, self.key_entry.get())
        generate_qr(self.key_entry.get(), "qr_code.png")
        messagebox.showinfo("Success", f"Message hidden in {out_image}\nQR code saved as qr_code.png")

    def extract_decrypt(self):
        if not self.image_path:
            messagebox.showwarning("Error", "Select an image first!")
            return
        key_str = self.key_entry.get().strip()
        if not key_str:
            messagebox.showwarning("Error", "Enter the key!")
            return

        encrypted = extract_data_random(self.image_path, key_str)
        if not encrypted:
            messagebox.showerror("Error", "No hidden message found!")
            return

        # Decide AES or RSA based on key format
        if "PRIVATE KEY" in key_str or "BEGIN" in key_str:
            decrypted = rsa_decrypt(encrypted, key_str)
        else:
            decrypted = aes_decrypt(encrypted, decode_aes_key(key_str))

        messagebox.showinfo("Decrypted Message", decrypted)

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoStegApp(root)
    root.mainloop()

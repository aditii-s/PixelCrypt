# 🔐 PixelCrypt
A simple Flask-based web application that allows you to:

✔ Encrypt a message using **AES** or **RSA**  
✔ Hide the encrypted message inside a **PNG image**  
✔ Extract & decrypt hidden messages  
✔ Generate a **QR code of the key**  
✔ Do everything through a clean, basic interface

This is a web version of the original Python desktop application you built.

---

## 🚀 Features
- **AES-256 encryption** (auto key generation)
- **RSA encryption** (private key returned to user)
- Message → Encrypt → Hide inside PNG
- Extract hidden data with correct key
- PNG output saves encoded image
- QR code generation for easy key sharing
- Simple, basic Flask HTML UI

---

## 🛠️ Technologies Used
### Backend
- Flask
- PyCryptodome
- Pillow (PIL)
- qrcode
- Randomized steganography based on key

### Frontend (Basic)
- HTML (Jinja templates)
- Bootstrap (optional)
- Simple file input + textarea forms

---

## ▶️ Running the Project

### 1. Install virtual environment (optional)
python -m venv venv

### 2. Activate it
Windows: venv\Scripts\activate

### 3. Install all dependencies:
pip install -r requirements.txt

### 4. Run the Flask app:
python app.py

### 5. Open in browser
Visit: http://127.0.0.1:5000

## 🖥️ How to Use

### Encrypt & Hide
-> Upload a PNG image
-> Enter message
-> Choose AES or RSA
-> Click Encrypt & Hide

### App returns:
-> Encoded PNG (download)
-> Key (text)
-> QR code (download)

### Extract & Decrypt:
-> Upload encoded PNG
-> Paste the key (AES Base64 or RSA private key)
-> Click Extract & Decrypt

The hidden message is revealed

---

## 🔧 Requirements
🔹 Flask
🔹 pycryptodome
🔹 Pillow
🔹 qrcode
🔹 flask-cors (optional)

---

⚠️ Notes

Only PNG images are supported (lossless)

Steganography uses randomized pixel positions derived from the key

Without the correct key, extraction fails or gives garbage

Keys are not stored — user must save them

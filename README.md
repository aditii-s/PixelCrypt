# CryptoSteg — A Hybrid Cryptography and Steganography Secure Message Encryptor 🔐🖼️

CryptoSteg is a secure communication application that combines 
**AES/RSA cryptography**, **randomized LSB image steganography**, and **QR-based key sharing** 
to provide a highly secure way to hide and transmit confidential messages inside images.

This project allows users to:
- Encrypt messages using AES-256 or RSA-2048
- Randomly embed encrypted data inside images (LSB Steganography)
- Generate QR codes for key sharing
- Extract & decrypt hidden messages securely

---

## 🚀 Features

### 🔒 Dual-Layer Security
- **AES-256 Encryption** for fast, secure symmetric encryption  
- **RSA-2048 Encryption** for asymmetric public/private key security  
- **Integrity Verification (SHA-256 HMAC)** to detect tampering  

### 🖼️ Powerful Steganography
- Randomized pixel embedding based on key seed  
- LSB (Least Significant Bit) modification  
- Anti-pattern extraction (shuffled pixel mapping)

### 📱 QR Code Key Sharing
- Auto-generate QR code of AES key or RSA private key  
- Fast and secure sharing between sender & receiver  

### 🧰 User-Friendly Interface
- Clean Tkinter GUI  
- Simple Encrypt → Hide → Extract → Decrypt workflow  

---

## 🔧 Software Requirements

- Python 3.10+
- Required Libraries:
pycryptodome
Pillow
tk
qrcode

- OS Support:
- Windows
- Linux
- macOS

---

## 🧱 Hardware Requirements

- 4 GB RAM minimum  
- Dual-core CPU  
- Storage: only a few MB required  
- Camera optional (for scanning QR codes)

---

## 📸 Diagrams

### **1. System Architecture Diagram**
(Encryption + Steganography + QR Key Flow)

![Architecture](architecture.png)

### **2. Workflow Diagram (End-to-End)**  
![Workflow](workflow.png)

### **3. Encryption & Decryption Flow**  
![Enc-Dec](encdec.png)

### **4. Module Interaction Diagram**  
![Modules](modules.png)

---

## 📝 How It Works

### **Encryption & Hiding Phase**
1. User inputs a message  
2. Chooses AES or RSA  
3. Message gets encrypted  
4. Encryption key is displayed + saved as QR  
5. Encrypted text is hidden inside a PNG using randomized LSB technique  
6. Output → `encoded_image.png` is obtained.

### **Decryption & Extraction Phase**
1. Select stego-image  
2. Enter (or scan) the key  
3. Extract hidden bits  
4. System identifies AES or RSA and decrypts  
5. Display original message  

---

## ▶️ Running the Application

python main_gui.py

---

## 🧪 Testing & Validation

- Verified AES data integrity using SHA-256 HMAC  
- Verified RSA key padding using OAEP  
- Tested extraction robustness on:
  - Large images
  - Noisy images
  - Modified pixel patterns

---

## 🤝 Contributing

Pull requests are welcome — improvements to cryptography, GUI, or steganography are highly appreciated.

---

## 📜 License

MIT License © 2025

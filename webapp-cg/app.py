from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os, uuid
from werkzeug.utils import secure_filename
from crypto import aes_encrypt, aes_decrypt, rsa_encrypt, rsa_decrypt, rsa_generate_keys
from steg import hide_data_random, extract_data_random
from utils import generate_aes_key, decode_aes_key
from qr_gen import generate_qr

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
ALLOWED_EXTENSIONS = {"png"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encrypt_hide", methods=["POST"])
def encrypt_hide():
    if "image" not in request.files:
        flash("No image part")
        return redirect(url_for("index"))

    image = request.files["image"]
    if image.filename == "" or not allowed_file(image.filename):
        flash("Please upload a PNG image.")
        return redirect(url_for("index"))

    message = request.form.get("message", "").strip()
    method = request.form.get("method", "AES")
    if not message:
        flash("Enter a message to hide.")
        return redirect(url_for("index"))

    # save uploaded image
    img_filename = secure_filename(f"{uuid.uuid4().hex}_{image.filename}")
    img_path = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
    image.save(img_path)

    if method == "AES":
        key_str = generate_aes_key()  # base64 string
        key = decode_aes_key(key_str)
        encrypted = aes_encrypt(message, key)
        display_key = key_str
    else:  # RSA
        private_key, public_key = rsa_generate_keys()
        # private_key, public_key are bytes
        private_key_str = private_key.decode()
        encrypted = rsa_encrypt(message, public_key)
        display_key = private_key_str

    out_image_name = f"encoded_{uuid.uuid4().hex}.png"
    out_image_path = os.path.join(app.config["OUTPUT_FOLDER"], out_image_name)

    # hide (steganography) using the same function you used in desktop app
    hide_data_random(img_path, out_image_path, encrypted, display_key)

    # generate QR
    qr_name = f"qr_{uuid.uuid4().hex}.png"
    qr_path = os.path.join(app.config["OUTPUT_FOLDER"], qr_name)
    generate_qr(display_key, qr_path)

    return render_template(
        "result_encrypt.html",
        out_image=out_image_name,
        qr_image=qr_name,
        key_text=display_key
    )

@app.route("/extract_decrypt", methods=["POST"])
def extract_decrypt():
    # The user can upload an image OR choose an existing file path (we'll only accept uploads for simplicity)
    if "image" not in request.files:
        flash("No image part")
        return redirect(url_for("index"))

    image = request.files["image"]
    if image.filename == "" or not allowed_file(image.filename):
        flash("Please upload a PNG image to extract from.")
        return redirect(url_for("index"))

    key_str = request.form.get("key", "").strip()
    if not key_str:
        flash("Enter the key (AES base64 or RSA private key).")
        return redirect(url_for("index"))

    img_filename = secure_filename(f"{uuid.uuid4().hex}_{image.filename}")
    img_path = os.path.join(app.config["UPLOAD_FOLDER"], img_filename)
    image.save(img_path)

    encrypted = extract_data_random(img_path, key_str)
    if not encrypted:
        flash("No hidden message found or wrong key for extraction.")
        return redirect(url_for("index"))

    # Decide AES or RSA by inspecting the key string (same heuristic as desktop)
    if "PRIVATE KEY" in key_str or "BEGIN" in key_str:
        decrypted = rsa_decrypt(encrypted, key_str)
    else:
        try:
            decrypted = aes_decrypt(encrypted, decode_aes_key(key_str))
        except Exception as e:
            decrypted = f"ERROR: {e}"

    return render_template("result_extract.html", decrypted_message=decrypted)

@app.route("/outputs/<filename>")
def outputs(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename, as_attachment=True)

@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


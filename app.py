
from flask import Flask, render_template, request
import os

from modules.ctf_helpers.decoder import decode_text
from modules.ctf_helpers.base_detector import detect_base
from modules.digital_forensics.metadata import extract_metadata
from modules.cryptography.crypto_tool import custom_encrypt, custom_decrypt

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ctf')
def ctf_main():
    return render_template('ctf_helpers.html')

@app.route('/ctf/base-detector', methods=['POST'])
def base_detector():
    encoded_text = request.form.get('encoded_text', '')
    base_result = detect_base(encoded_text)
    return render_template('ctf_helpers.html', base_result=base_result, encoded_input=encoded_text)

@app.route('/ctf/decode', methods=['POST'])
def decode_route():
    input_text = request.form.get('input_text', '')
    encoding = request.form.get('encoding', '')
    result = decode_text(input_text, encoding)
    return render_template('ctf_helpers.html', decode_result=result, input_text=input_text, selected_encoding=encoding)

@app.route('/forensics')
def forensics_main():
    return render_template('forensics.html')

@app.route('/forensics/editor', methods=['POST'])
def file_editor():
    file = request.files.get('file')
    file_content = ''
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        file_content = read_file_content(path)
    return render_template('forensics.html', file_content=file_content)

@app.route('/forensics/metadata', methods=['POST'])
def metadata_extractor():
    file = request.files.get('file')
    metadata_result = {}
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        metadata_result = extract_metadata(path)
    return render_template('forensics.html', metadata_result=metadata_result)

@app.route('/crypto')
def crypto_main():
    return render_template('cryptography.html')

@app.route('/crypto/encrypt', methods=['POST'])
def encrypt_text():
    plain_text = request.form.get('plain_text', '')
    encrypted_text = custom_encrypt(plain_text, request.form.get('key', '5'))
    return render_template('cryptography.html', plain_text=plain_text, encrypted_text=encrypted_text)

@app.route('/crypto/decrypt', methods=['POST'])
def decrypt_text():
    cipher_text = request.form.get('cipher_text', '')
    decrypted_text = custom_decrypt(cipher_text, request.form.get('key', '5'))
    return render_template('cryptography.html', cipher_text=cipher_text, decrypted_text=decrypted_text)

if __name__ == "__main__":
    app.run(debug=True)

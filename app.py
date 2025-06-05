from flask import Flask, render_template, request, redirect, url_for, send_file
from encryption_util import encrypt_file, decrypt_file, generate_key, load_key
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.config['KEY_FILE'] = 'key.key'

# Create upload and download folders if they don't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

# Ensure key.key exists or generate it
if not os.path.exists(app.config['KEY_FILE']):
    generate_key()
    print("Encryption key generated and saved as 'key.key'.")

# Load the key for the application
encryption_key = load_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file_web():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        encrypted_filepath = encrypt_file(filepath, key=encryption_key, delete_original=True)
        
        # Check if encryption was successful and file exists
        if encrypted_filepath and os.path.exists(encrypted_filepath):
            # Move the encrypted file to the downloads folder for easy access
            encrypted_filename = os.path.basename(encrypted_filepath)
            download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], encrypted_filename)
            os.rename(encrypted_filepath, download_path)
            
            return send_file(download_path, as_attachment=True)
        else:
            return "Encryption failed or file not found.", 500

@app.route('/decrypt', methods=['POST'])
def decrypt_file_web():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Ensure the filename has .encrypted extension for decryption
        if not filepath.endswith('.encrypted'):
            # You might want to handle this more gracefully, e.g., show an error
            os.remove(filepath) # Remove uploaded non-encrypted file
            return "Please upload an encrypted file (e.g., .encrypted extension).", 400

        decrypted_filepath = decrypt_file(filepath, key=encryption_key, delete_encrypted=True)
        
        if decrypted_filepath and os.path.exists(decrypted_filepath):
            # Move the decrypted file to the downloads folder for easy access
            decrypted_filename = os.path.basename(decrypted_filepath)
            download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], decrypted_filename)
            os.rename(decrypted_filepath, download_path)
            
            return send_file(download_path, as_attachment=True)
        else:
            return "Decryption failed or file not found. Ensure the correct key is used.", 500

if __name__ == '__main__':
    app.run(debug=True)

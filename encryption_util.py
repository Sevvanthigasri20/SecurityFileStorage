from cryptography.fernet import Fernet
import os

# 1. Generating and Saving the Key
def generate_key():
    """Generates a new encryption key and saves it to key.key file."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated and saved as 'key.key'.")

# 2. Loading the Key
def load_key():
    """Loads the encryption key from the key.key file."""
    # Check if key.key exists before trying to open it
    if not os.path.exists("key.key"):
        generate_key() # Generate key if it doesn't exist
    return open("key.key", "rb").read()

# 3. Encrypting a File
# Modified to accept 'key' and 'delete_original'
def encrypt_file(file_path, key, delete_original=False):
    """
    Encrypts a file and saves it with a .encrypted extension.
    Takes the encryption key as an argument.
    Optionally deletes the original file after encryption.
    """
    f = Fernet(key)

    with open(file_path, "rb") as original_file:
        original_data = original_file.read()

    encrypted_data = f.encrypt(original_data)

    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f"'{file_path}' encrypted and saved as '{encrypted_file_path}'.")

    if delete_original:
        os.remove(file_path)
        print(f"Original file '{file_path}' deleted.")
    
    return encrypted_file_path # Return the path to the newly created encrypted file

# 4. Decrypting a File
# Modified to accept 'key'
def decrypt_file(encrypted_file_path, key, delete_encrypted=False): # Added 'delete_encrypted'
    """
    Decrypts an encrypted file and saves it as the original file.
    Takes the encryption key as an argument.
    Optionally deletes the encrypted file after decryption.
    """
    f = Fernet(key)

    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    try:
        decrypted_data = f.decrypt(encrypted_data)
    except Exception as e:
        print(f"Could not decrypt file. Key might be incorrect or file corrupted: {e}")
        return None # Return None on failure

    original_file_name = os.path.basename(encrypted_file_path).replace(".encrypted", "")
    original_file_path = os.path.join(os.path.dirname(encrypted_file_path), original_file_name)
    
    with open(original_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    print(f"'{encrypted_file_path}' decrypted and saved as '{original_file_path}'.")

    # Add this logic to delete the encrypted file if delete_encrypted is True
    if delete_encrypted:
        os.remove(encrypted_file_path)
        print(f"Encrypted file '{encrypted_file_path}' deleted.")

    return original_file_path # Return the path to the newly created decrypted file

# Examples to test the code (you can run this directly to test the functions)
if __name__ == "__main__":
    # Ensure key exists for testing
    if not os.path.exists("key.key"):
        generate_key()
    loaded_key = load_key()

    # First, let's create a test file
    test_file_name = "test_document.txt"
    with open(test_file_name, "w") as f:
        f.write("This is a secret message. No one should read this!")
    print(f"Test file '{test_file_name}' created.")

    print("\n--- Encrypting ---")
    encrypted_path = encrypt_file(test_file_name, loaded_key)

    # Check if the encrypted file exists
    if encrypted_path and os.path.exists(encrypted_path):
        print(f"'{encrypted_path}' file exists.")

        # Optionally delete the original file for testing
        # os.remove(test_file_name)
        # print(f"Original file '{test_file_name}' deleted.")

        print("\n--- Decrypting ---")
        decrypted_path = decrypt_file(encrypted_path, loaded_key)

        # Read the content of the decrypted file
        if decrypted_path and os.path.exists(decrypted_path):
            with open(decrypted_path, "r") as f:
                content = f.read()
            print(f"Content of decrypted file: '{content}'")
        else:
            print("Decrypted original file not found or decryption failed.")
    else:
        print("Encrypted file was not created.")

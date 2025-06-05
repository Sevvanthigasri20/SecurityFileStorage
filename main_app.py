from encryption_util import encrypt_file, decrypt_file
import os

def run_file_operation():
    """Takes user input to encrypt or decrypt a file."""
    print("\n--- File Encryption/Decryption Tool ---")
    
    while True:
        choice = input("Enter 'e' to encrypt, 'd' to decrypt, or 'x' to exit: ").lower()

        if choice == 'x':
            print("Exiting the tool. Thank you!")
            break
        elif choice == 'e':
            file_to_encrypt = input("Enter the name of the file to encrypt: ")
            if os.path.exists(file_to_encrypt):
                encrypt_file(file_to_encrypt)
            else:
                print(f"Error: File '{file_to_encrypt}' not found.")
        elif choice == 'd':
            file_to_decrypt = input("Enter the name of the file to decrypt (e.g., my_file.txt.encrypted): ")
            if os.path.exists(file_to_decrypt):
                decrypt_file(file_to_decrypt)
            else:
                print(f"Error: File '{file_to_decrypt}' not found.")
        else:
            print("Invalid choice. Please enter 'e', 'd', or 'x'.")

if __name__ == "__main__":
    run_file_operation()

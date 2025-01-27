import streamlit as st
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode

# Helper function for navigation
def navigate_to(page):
    st.session_state.current_page = page

# Asymmetric Encryption Algorithms
def rsa_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_encrypt(public_key, message):
    encrypted = public_key.encrypt(
        message.encode(),
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return b64encode(encrypted).decode()

def rsa_decrypt(private_key, encrypted_message):
    decrypted = private_key.decrypt(
        b64decode(encrypted_message),
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# Asymmetric Encryption Page
def asymmetric_page():
    # Back button at the top of the page
    if st.button("⬅ Back"):
        navigate_to("Introduction")

    st.title("Asymmetric Encryption")
    
    action = st.radio("Select Action:", ["Generate RSA Key Pair", "Encrypt with RSA", "Decrypt with RSA"])
    
    if action == "Generate RSA Key Pair":
        if st.button("Generate"):
            private_key, public_key = rsa_key_pair()
            st.session_state.private_key = private_key
            st.session_state.public_key = public_key
            st.success("RSA Key Pair Generated!")
            
            # Displaying the public and private keys
            st.subheader("Public Key:")
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
            st.text_area("Public Key PEM Format", public_pem)
            
            st.subheader("Private Key:")
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()
            st.text_area("Private Key PEM Format", private_pem)

    elif action == "Encrypt with RSA":
        message = st.text_input("Enter message to encrypt:")
        if st.button("Encrypt"):
            encrypted_message = rsa_encrypt(st.session_state.public_key, message)
            st.success(f"Encrypted Message: {encrypted_message}")
    
    elif action == "Decrypt with RSA":
        encrypted_message = st.text_input("Enter encrypted message:")
        if st.button("Decrypt"):
            decrypted_message = rsa_decrypt(st.session_state.private_key, encrypted_message)
            st.success(f"Decrypted Message: {decrypted_message}")

# Main
if "current_page" not in st.session_state:
    st.session_state.current_page = "Introduction"

if st.session_state.current_page == "Introduction":
    introduction()
elif st.session_state.current_page == "Symmetric Encryption":
    symmetric_page()
elif st.session_state.current_page == "Asymmetric Encryption":
    asymmetric_page()
elif st.session_state.current_page == "Hashing":
    hashing_page()

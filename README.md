# 🔐 RSA-Based Encrypted Messaging Terminal

This project implements a **secure terminal-based messaging system** using **RSA encryption** and **ZeroMQ** for encrypted communication between two users: **UserA** and **UserB**. It simulates a secure communication protocol with features like **mutual authentication**, **public key distribution**, and **end-to-end encryption**.

---

## 🧩 Components

- `PKDA.py` – **Public Key Distribution Authority**: Distributes public keys securely upon request.
- `UserA.py` – Simulates **User A**, handles sending/receiving messages with encryption and nonce verification.
- `UserB.py` – Simulates **User B**, also supports secure messaging and key requests.
- `RSA.py` – Core **RSA cryptography module**, handles key generation, encryption, decryption, and utility functions.

---

## 🔐 Security Features

- **RSA Public Key Encryption**
  - Ensures that messages can only be decrypted by the intended recipient.
- **Mutual Authentication using Nonces**
  - Prevents replay attacks and validates user identity using a nonce-based challenge-response.
- **PKDA Server**
  - A simulated trusted authority to manage and distribute user public keys.

---

## ⚙️ How It Works

1. **Key Distribution**:  
   Users request each other's public keys from the PKDA server. Keys are returned encrypted using PKDA’s private key.

2. **Authentication Phase**:
   - User A sends an encrypted message containing a random nonce.
   - User B decrypts, appends their own nonce, encrypts again, and sends it back.
   - User A verifies by returning User B’s nonce.
   - Only after mutual verification is messaging allowed.

3. **Encrypted Messaging**:  
   All messages exchanged are encrypted with RSA using public/private key pairs.

---

## 🚀 Getting Started

### Requirements

- Python 3.x
- [`pyzmq`](https://pypi.org/project/pyzmq/) – ZeroMQ messaging library

# Install dependencies:  
  ```bash
  pip install pyzmq
  ```
# Running the System:
Run the following in separate terminal windows:
  ```bash
  # Terminal 1 - PKDA Server
  python PKDA.py
  
  # Terminal 2 - User A Terminal
  python UserA.py
  
  # Terminal 3 - User B Terminal
  python UserB.py
```
### Example Workflow
- Start the PKDA server.
- User A or B requests the other’s public key via the PKDA.
- User A initiates a message with a nonce.
- User B responds with nonce A and a new nonce B.
- User A returns nonce B to confirm identity.
- Encrypted messaging starts securely.

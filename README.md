# <a href="https://credlytic-minor-proj.vercel.app/">Credlytic</a>

>**Zero-Trust Academic Credentialing & Verification System Anchored on the Aptos Blockchain**

<img width="2777" height="1196" alt="image" src="https://github.com/user-attachments/assets/28b61055-1ed3-47ef-a1a4-e0b9f8237984" />

[![Aptos](https://img.shields.io/badge/Blockchain-Aptos_Testnet-2bd2a5?style=flat-square\&logo=aptos)](https://aptoslabs.com/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=flat-square\&logo=flask)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat-square\&logo=supabase)](https://supabase.com/)
[![Vercel](https://img.shields.io/badge/Hosting-Vercel-000000?style=flat-square\&logo=vercel)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Compute-Render-46E3B7?style=flat-square)](https://render.com/)



Credlytic is a decentralized application designed to eliminate academic and professional credential fraud.
It transforms traditional certificates into **immutable, publicly verifiable on-chain NFTs**, ensuring authenticity and tamper-proof validation.

This project features a fully decoupled frontend and backend architecture, custom HTTPS proxy tunnels to bypass restrictive cloud SMTP firewalls, and asynchronous transaction management for high-throughput environments.

---

## 🎯 The Problem vs. The Solution

**The Problem:** Traditional digital certificates are merely PDFs or image files. They can be photoshopped, altered, or completely fabricated in minutes. Background checks take weeks, and universities spend vast resources manually verifying alumni credentials.

**The Solution:** Credlytic mints a unique Non-Fungible Token (NFT) for every certificate issued.

- Evaluators (Employers) don't have to trust the student or the PDF — they trust the math.
- By cross-referencing a transaction hash against the Aptos ledger, a credential's authenticity, origin (University Wallet), and recipient can be mathematically proven in under 3 seconds.

---

## ✨ Core Features

* **Decentralized Minting Engine** — Issues NFTs on the Aptos Testnet for every credential.
* **Cryptographic Verification** — 3-step validation using Supabase + Aptos blockchain.
* **SMTP Bypass via HTTPS Tunnel** — Uses Google Apps Script for secure delivery.
* **Anti-Sleep Infrastructure** — Keeps backend services active with heartbeat triggers.
* **Transaction Collision Handling** — Prevents blockchain sequence conflicts.
* **Multi-Role Access** — Admin, Student, and Employer portals.

---

## 🏗️ System Architecture

```text
┌─────────────────┐       REST API        ┌─────────────────┐
│   Vercel Edge   │─────────────────────▶│  Render Backend │
│   (HTML/JS/UI)  │◀─────────────────────│  (Flask/Python) │
└─────────────────┘      CORS Secured     └─────────────────┘
         │                                         │
         │                                         │ (1) Mints NFT
         ▼                                         ▼
┌─────────────────┐                       ┌─────────────────┐
│    Employer/    │                       │  Aptos Testnet  │
│     Student     │                       │  (Blockchain)   │
└─────────────────┘                       └─────────────────┘
                                                   │
                                                   │ (2) Stores Hash
┌─────────────────┐                                ▼
│  Student Inbox  │                       ┌─────────────────┐
│   (PDF + Link)  │                       │   Supabase DB   │
└─────────────────┘                       │  (PostgreSQL)   │
         ▲                                └─────────────────┘
         │                                         │
         │ (3) Bypasses SMTP via HTTPS Proxy       │
         │                                         │
┌─────────────────┐                                │
│ Google AppScript│◀──────────────────────────────┘
│  (Smuggler/Ping)│
└─────────────────┘
```
---

## 🧠 Verification Logic

The Employer Verification portal executes a two layered security check to guarantee authenticity:

1. **Database Index Search:** The user inputs a Transaction Hash. The backend queries the database. If the hash does not exist locally, the system immediately drops the request and returns a `404 Record Not Found`.

2. **Blockhain Query:** If the hash exists in the database, the backend queries the Aptos Testnet API directly. If the transaction cannot be validated on the blockchain (indicating database tampering), the system flags it as compromised and throws a `401 Unauthorized`.

3. **Identity Cross-Referencing:** If the employer provides an optional student email, the backend cross-references the input against the immutable payload originally etched into the blockchain, returning a visual "Full Identity Match" confirmation.

---

## 📁 Project Structure

```text
Credltyic/
├── .gitignore               [Specifies intentionally untracked files to ignore]
├── backend/
│   ├── .env                 [Environment variables and cryptographic keys]
│   ├── main.py              [Flask entrypoint, dynamic port binding, and CORS configuration]
│   ├── requirements.txt     [Python dependency definitions]
│   ├── api/
│   │   ├── routes_admin.py  [Secure administrative minting and issuance endpoints]
│   │   └── routes_public.py [Employer verification logic and infrastructure keep-alive pulse]
│   ├── core/
│   │   ├── config.py        [Environment variable validation and global configuration]
│   │   └── security.py      [JWT validation, whitelist checking, and auth logic]
│   └── services/
│       ├── blockchain.py    [Aptos SDK integration, payload construction, and collision jitter]
│       ├── certificate.py   [Pillow-based PDF/image rendering and template overlay]
│       ├── database.py      [Supabase PostgreSQL client connection and pooling]
│       └── mailer.py        [Base64 PDF packaging and Google HTTPS proxy routing]
├── frontend/
│   ├── about.html           [Project details and architectural overview]
│   ├── adm_dash.html        [Main administrative control room for issuance]
│   ├── admin.html           [Administrative Google OAuth login gate]
│   ├── index.html           [Public landing page and portal selector]
│   ├── stud_dash.html       [Student credential viewer and downloader]
│   ├── student.html         [Student email lookup gate]
│   ├── vercel.json          [Vercel routing, headers, and deployment configuration]
│   ├── verification.html    [Public-facing employer cryptographic verification check]
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css    [Glassmorphism UI, variables, and multi-UI optimisation]
│   │   ├── fonts/           [Custom fonts like Inter.ttf]
│   │   └── images/          [Certificate templates, logos, etc.]
│   └── js/
│       ├── api.js           [Centralized cross-origin fetch wrappers for backend communication]
│       ├── config.js        [Frontend environment configurations and API base URLs]
│       ├── network-bg.js    [Three.js interactive particle background animation]
│       └── theme.js         [System-wide dark/light mode toggle with local storage persistence]
└── scripts/
    └── setup_collection.py  [One-time Aptos Collection initializer]
```

---

## 🔌 API Route Documentation

### 🔒 Protected Admin Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/admin/login_check` | Verifies administrative credentials and issues session state. |
| `POST` | `/api/admin/issue` | Primary minting engine. Packages student data, interacts with Aptos SDK, generates the PDF overlay, and triggers the Google Apps Script email proxy. |

### 🌍 Public Verification Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/employer/verify` | Receives `tx_hash` and `email`. Performs the 3-step cryptographic verification check against Supabase and the Aptos API. |
| `GET` | `/api/student/certificates?email=<addr>` | Retrieves an array of all validated credentials associated with a specific identity. |
| `GET` | `/api/system-pulse` | Invisible keep-alive route designed to accept automated pings, keeping Gunicorn workers and Supabase TCP connections active. |

---

## 🚀 Local Deployment & Setup Guide

### 1. Prerequisites

- Python 3.9+
- Node.js & npm *(optional, for frontend serving)*
- An Aptos Petra Wallet (funded on Testnet via Faucet)
- A Supabase Project (PostgreSQL)

### 2. Environment Configuration

Create a `.env` file in the `backend/` directory. **Never commit this file to version control.**

```env
# Supabase
SUPABASE_URL=YOUR_URL
SUPABASE_ANON_KEY=YOUR_KEY
SUPABASE_SERVICE_ROLE_KEY=YOUR_KEY

# Aptos
UNIVERSITY_PRIVATE_KEY=YOUR_PRIVATE_KEY
APTOS_NODE_URL=https://api.testnet.aptoslabs.com/v1

# Email
EMAIL_ADDRESS=your@email.com
EMAIL_PASSWORD=your_password

# Security
ADMIN_WHITELIST=email1,email2
FLASK_SECRET_KEY=your_secret
GOOGLE_CLIENT_ID=your_client_id
```

### 3. Initialize the Blockchain Collection

Before issuing any certificates, you must carve out the parent collection on the Aptos Testnet ledger. This script only needs to be executed **once**.

```bash
cd backend
python scripts/setup_collection.py
# Wait for the "SUCCESS" terminal output
```

### 4. Booting the Application

Due to the decoupled architecture, run the backend and frontend on separate ports.

**Start the Flask Backend:**

```bash
cd backend
pip install -r requirements.txt
python main.py
# Server binds to http://0.0.0.0:5000
```

**Serve the Frontend** *(open a new terminal window):*

```bash
cd frontend
python -m http.server 3000
# Access the UI at http://localhost:3000
```
---

## 🛠️ Tech Stack

| Category           | Technologies                                                     |
| ------------------ | ---------------------------------------------------------------- |
| **Frontend**       | HTML, CSS, JavaScript, Three.js, Google Identity Services        |
| **Backend**        | Flask, Aptos Python SDK, Pillow, urllib.render                   |
| **Database**       | Supabase (PostgreSQL)                                            |
| **Infrastructure** | Render, Vercel, Google Apps Script                               |

---

## 🔮 Future Roadmap & Enhancements

- **Smart Contract Expansion:** Transition from standard Aptos token scripts to fully custom Move modules for advanced credential revocation capabilities.
- **Batch Issuance:** Implement CSV parsing for universities to mint hundreds of credentials in a single bulk transaction.
- **Zero-Knowledge Proofs (ZKPs):** Allow students to prove they hold a specific credential (e.g., "Over 18" or "Has a Degree") without revealing their name or personal data to the employer.
- **IPFS Decentralized Storage:** Move PDF and template storage from centralized cloud servers to the InterPlanetary File System (IPFS) to ensure absolute permanence.

---

## 👨‍💻 Developer

**<a href="https://prabhatbhatia.netlify.app/">Prabhat Bhatia</a>**  
B.Tech CSE (Cyber Security) | Semester II

> This project is currently being used as the Minor Project for Semester II. 

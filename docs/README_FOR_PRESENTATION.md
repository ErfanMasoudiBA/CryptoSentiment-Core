# Presentation Checklist — CryptoSentiment-Core

Use this checklist before your presentation to ensure everything is ready.

---

## Before You Present

- [ ] **1. Run the Backend**
  - Open a terminal in the project root.
  - Navigate to the backend: `cd backend`
  - Start the FastAPI server: `uvicorn main:app --reload`
  - Confirm it is running at **http://127.0.0.1:8000** (check the terminal output).

- [ ] **2. Open the Android Emulator (for the Flutter app)**
  - Start your Android emulator (or connect a physical device with USB debugging).
  - From the project root: `cd mobile_app/crypto_sentiment_app`
  - Run: `flutter run`
  - Ensure the app loads and can reach the backend at `10.0.2.2:8000` (emulator’s host machine).

- [ ] **3. Open the Web Dashboard (localhost:3000)**
  - Open a terminal and go to: `cd web_dashboard/crypto-dashboard`
  - Run: `npm run dev`
  - In your browser, open **http://localhost:3000**
  - Confirm the dashboard loads and shows data from the backend.

---

## Quick Reference

| Item              | Command / URL                          |
|-------------------|----------------------------------------|
| Backend           | `cd backend && uvicorn main:app --reload` |
| Backend URL       | http://127.0.0.1:8000                  |
| Flutter app       | `cd mobile_app/crypto_sentiment_app && flutter run` |
| Web dashboard     | `cd web_dashboard/crypto-dashboard && npm run dev` |
| Dashboard URL     | http://localhost:3000                  |

---

*Good luck with your presentation.*

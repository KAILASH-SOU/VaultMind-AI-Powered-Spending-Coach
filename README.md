VaultMind/
│
├── app.py
│   → The main Streamlit application that runs the entire project.
│     It handles user input, displays interactive visualizations,
│     generates spending alerts, and uses the Gemini API to deliver
│     personalized financial coaching.
│
├── transactions.csv
│   → A synthetic dataset that stores all user transactions.
│     This file automatically updates whenever a new transaction
│     is added through the app.
│
├── requirements.txt
│   → Lists all the Python dependencies required to run the project.
│     You can install them easily using:
│     pip install -r requirements.txt
│
├── .env
│   → Stores the Gemini API key securely.
│     This file is excluded from GitHub for privacy and security reasons.
│
└── README.md
    → Contains complete project documentation, including
      an overview, setup steps, and future improvements.

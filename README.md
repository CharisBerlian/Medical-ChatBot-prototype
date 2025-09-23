HealthPal: Your AI Health Companion
HealthPal is a comprehensive health management application designed to be your trusted AI-powered health companion. It combines a medical chatbot for instant health queries, a medication reminder system, and a personal medical history log, all accessible through a user-friendly and responsive web interface.

🌟 Features
🔐 Secure User Authentication: A robust login and registration system to keep your health data private and secure.

💬 AI Medical Chatbot: Get answers to general health questions, symptom inquiries, and medication information from an intelligent chatbot powered by the DeepSeek API.

💊 Medication Reminders: A powerful scheduling tool to set up and receive timely reminders for your medications. You can customize dosages, timings, and frequency (daily/weekly).

📋 Personal Medical History: Keep a detailed log of your medical records, including conditions, allergies, surgeries, and vaccinations, all in one place.

📱 Responsive Design: A clean and intuitive interface that works seamlessly on both desktop and mobile devices.

🎥 Demonstration
Here is a video walkthrough of the HealthPal application:

(You can upload your 2025-05-20 22-09-41.mp4 video to your GitHub repository and link it here)

🛠️ Tech Stack
Backend: FastAPI, Python

Frontend: Streamlit

Database: SQLite for user authentication

AI Model: DeepSeek API

⚙️ Setup and Installation
Follow these steps to get the HealthPal application running on your local machine.

Prerequisites
Python 3.8 or higher

pip (Python package installer)

1. Clone the Repository
git clone [https://github.com/your-username/HealthPal.git](https://github.com/your-username/HealthPal.git)
cd HealthPal

2. Install Dependencies
Install all the required Python packages using the requirements.txt file.

pip install -r requirements.txt

3. Set Up Environment Variables
You'll need an API key from DeepSeek for the chatbot feature.

Create a file named .env in the root directory of the project.

Add your API key to the .env file as shown below:

DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY_HERE"

4. Run the Application
You need to run two separate processes: the FastAPI backend server and the Streamlit frontend application.

Start the FastAPI Backend:
Open a terminal and run the following command:

uvicorn main:app --reload

The backend server will be running at http://localhost:8000.

Start the Streamlit Frontend:
Open a second terminal and run:

streamlit run streamlit_app.py

The frontend application will open in your browser at http://localhost:8501.

🚀 How to Use
Register/Login: Create a new account or log in with your existing credentials.

Medical Chatbot: Navigate to the "Medical Chatbot" tab to ask health-related questions.

Medication Reminder: Go to the "Medication Reminder" tab to add new medication schedules. The app will send you notifications.

Medical History: Use the "Medical History" tab to log and view your personal medical records.

🤝 Contributing
Contributions are welcome! If you have ideas for new features or improvements, feel free to open an issue or submit a pull request.

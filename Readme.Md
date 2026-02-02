# ⚗️ Chemical Equipment Parameter Visualizer  
### A Hybrid Web + Desktop Application

The Chemical Equipment Parameter Visualizer is a hybrid analytics tool I built to make sense of chemical equipment data in a simple and visual way. Instead of staring at raw CSV files, users can upload their data and instantly see meaningful insights through charts, summaries, and downloadable reports — whether they’re using a web browser or a desktop application. 
The goal is to bridge the gap between a **portable Web Dashboard** and a **powerful Native Desktop Application**, all powered by a **single intelligent Django API**.

---

## Demo Video
```bash
https://drive.google.com/file/d/1CadII1MQU7x6Io-IsUfdpsL1q07nIrcF/view?usp=sharing
```


---

## Tech Stack — *What & Why*

The tech stack used in this project is: 

---

### 1️⃣ Backend (The Brain): Django & Django REST Framework

**Why Django?**  
Django is a *batteries-included* Python framework that handles databases, authentication, security, and CSV processing efficiently. It acts as the central hub for both web and desktop clients.

**Key Libraries**
- **Pandas** – High-performance CSV processing, averages & equipment distribution
- **ReportLab** – Programmatic PDF report generation
- **SimpleJWT** – Secure JWT-based authentication

---

### 2️⃣ Web Frontend (The Face): React.js

**Why React?**  
React enables a fast, interactive dashboard experience with real-time chart updates — no page reloads.

**Key Libraries**
- **Chart.js** – Smooth animated pie & bar charts
- **Axios** – Reliable API communication

---

### 3️⃣ Desktop Frontend (The Power): PyQt5

**Why PyQt5?**  
Native desktop applications feel more robust and are ideal for offline or high-performance use cases.

**Key Libraries**
- **Matplotlib** – Industry-standard plotting for desktop visualizations

---

## Project Flow — How It Works

1. **Authentication**  
   - User logs in via Web or Desktop  
   - Django issues a JWT token

2. **Input**  
   - User uploads CSV file

3. **Analysis**  
   - Backend processes CSV using Pandas  
   - Calculates:
     - Mean Pressure
     - Mean Temperature
     - Mean Flowrate  
   - Counts equipment types

4. **Storage**  
   - Metadata (averages & counts) stored in SQLite  
   - Used to populate **History**

5. **Output**
   - **Web App:** Interactive Chart.js visualizations  
   - **Desktop App:** Embedded Matplotlib charts  
   - **PDF Engine:** Clean one-page analysis report

---

## ⚙️ Local Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/Aditee-18/Hybrid-Application.git

```
### Step 1: The Foundation (Backend)

The Django backend must be running for **both the Web Dashboard and the Desktop Application** to work.

Navigate to the backend folder:
```bash
cd Backend

```
## Create and activate a Python virtual environment:

```bash
python -m venv .venv
```

# On Windows:

```bash
.venv\Scripts\activate
```

# On macOS / Linux:
```bash
source .venv/bin/activate
```

## Install the backend dependencies (The Engine):

```bash
pip install -r requirements.txt
```

## Prepare the database by creating tables for user accounts and equipment data:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create a superuser account. These credentials will be used to log into both the Web and Desktop applications:

```bash
python manage.py createsuperuser
```

## Start the Django development server:

```bash
python manage.py runserver
```

The backend is now live at:
http://127.0.0.1:8000/


### Step 2: The Portal (Web Frontend)

Keep the backend server running and open a new terminal window.

## Navigate to the web frontend folder:
```bash
cd frontend-web
```

## Install frontend dependencies:

```bash
npm install
```

## Start the web dashboard:

```bash
npm run dev
```

Open the URL shown in the terminal (usually http://localhost:5173
) and log in using the credentials created in Step 1.


### Step 3: The Power (Desktop Application)

Open a third terminal window.

## Navigate to the desktop application folder:
```bash
cd frontend-desktop
```

## Ensure the Python virtual environment from Step 1 is still active, then run the desktop application:

```bash
python main.py
```

## Log in using the same credentials and upload your CSV file to begin analysis.

🧪 How to Demo the System


To verify backend synchronization, upload a CSV file using the Web Dashboard, then open History in the Desktop Application.
The uploaded record will appear instantly on both platforms since they share the same backend database.

Verify the analysis by observing that values such as Average Pressure (6.11 bar) and Average Temperature (117.47°C) are calculated once by the Django backend and consistently reflected across both frontends.

Use the Generate PDF Report button on either platform to export a professionally formatted analysis report.

### Notes:

Case Sensitivity:
The system is designed to handle standard CSV headers such as Equipment Name, Type, Pressure, Temperature, and Flowrate.

Port Conflicts:
Ensure that no other software is using port 8000 (Django backend) or the React development port before starting the setup.

---


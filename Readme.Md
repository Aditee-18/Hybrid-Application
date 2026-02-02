# ⚗️ Chemical Equipment Parameter Visualizer  
### A Hybrid Web + Desktop Application

The Chemical Equipment Parameter Visualizer is a hybrid analytics tool I built to make sense of chemical equipment data in a simple and visual way. Instead of staring at raw CSV files, users can upload their data and instantly see meaningful insights through charts, summaries, and downloadable reports — whether they’re using a web browser or a desktop application. 
The goal is to bridge the gap between a **portable Web Dashboard** and a **powerful Native Desktop Application**, all powered by a **single intelligent Django API**.

---

## 🚀 Live Demo & Video

🌐 **Live Web Dashboard:**  
👉 *INSERT YOUR VERCEL LINK HERE*

📺 **Video Walkthrough (2–3 mins):**  
👉 *INSERT YOUR YOUTUBE / DRIVE LINK HERE*

---

## 🧠 Tech Stack — *What & Why*

The tech stack used in this roject is: 

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

## 🌊 Project Flow — How It Works

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

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd "HYBRID APPLICATION"

# 🚀 AI Resume Analyzer & Optimizer

> **Stop guessing why your resume gets rejected.** An AI-powered platform that scores your resume against real job descriptions, closes keyword gaps, and rewrites your bullet points using the Google XYZ formula — all in a sleek, glassmorphic dark-mode UI.

---

## ✨ Overview

**AI Resume Analyzer & Optimizer** is a modern, high-performance full-stack web application that helps job seekers understand exactly how their resume stacks up against a target job description. Powered by **Google Gemini AI**, it calculates an ATS (Applicant Tracking System) match score, surfaces missing keywords, breaks down feedback section-by-section, and offers a concrete roadmap to close skill gaps.

It also includes a standalone **Bullet Point Optimizer** — an interactive playground that rewrites weak resume bullets into high-impact statements using the **Google XYZ formula**:

> *"Accomplished [X], as measured by [Y], by doing [Z]."*

No API key? No problem — the app ships with a **Mock Fallback Mode** that uses local semantic heuristics, so the entire UI stays fully functional offline or in demo mode.

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| 📄 **Multi-Format Parser** | Upload resumes as **PDF** or **DOCX**. Extracts paragraphs, bullet points, and tables with a dual-engine PDF pipeline (`pdfplumber` → falls back to `pypdf`). |
| 🎯 **ATS Match Scoring** | AI-driven percentage match between your resume and a job description, visualized with an animated circular gauge. |
| 🔑 **Keyword Gap Analysis** | Clearly separates **matching**, **missing**, and **recommended** keywords/skills as an easy-to-scan pill layout. |
| 🧩 **Section-by-Section Breakdown** | Individual feedback for Contact, Summary, Experience, Education, and Skills sections. |
| 🧪 **Mock Fallback Mode** | Fully offline-capable — generates realistic mock analysis when no `GEMINI_API_KEY` is set. |
| ✍️ **XYZ Bullet Optimizer** | Paste a bullet point and get back an AI-optimized version following the Google XYZ formula. |
| 🗺️ **Skill Gap Roadmap** | Actionable certifications, learning resources, and next steps for missing skills. |
| 🎨 **Premium Dark UI** | Custom gradients, glassmorphism, and micro-animations — built with hand-tuned vanilla CSS. |

---

## 🛠️ Tech Stack

**Frontend**
- ⚛️ React 18
- ⚡ Vite (dev server + build tooling)
- 🎨 Vanilla CSS (dark theme, glassmorphism, custom animations)
- 🖼️ Lucide React (icons)

**Backend**
- 🐍 Python + FastAPI
- 🦄 Uvicorn (ASGI server)
- 📑 pdfplumber + pypdf (PDF text extraction, dual-engine fallback)
- 📝 python-docx (Word document parsing)
- 🤖 google-generativeai (Gemini API integration)
- 🔐 python-dotenv (environment configuration)

---

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py             # FastAPI entry point, CORS, routes
│   │                        #   /api/health
│   │                        #   /api/analyze
│   │                        #   /api/optimize-bullet
│   ├── analyzer.py         # Gemini API calls + mock analyzer heuristics
│   ├── parser.py           # PDF/DOCX text extraction logic
│   └── requirements.txt    # Python dependencies
│
└── frontend/
    ├── index.html
    ├── package.json        # Scripts: dev, build, lint, preview
    ├── vite.config.js
    └── src/
        ├── App.jsx         # App orchestration, state, layout
        ├── main.jsx
        ├── index.css       # Typography, dark theme, styling
        ├── utils/
        │   └── api.js      # Fetch helpers -> VITE_API_BASE_URL
        └── components/
            ├── FileUpload.jsx        # Drag & drop resume upload
            ├── JobDescription.jsx    # Job description text input
            ├── ScoreMeter.jsx        # Animated SVG ATS score gauge
            ├── KeywordGap.jsx        # Matching/missing keyword pills
            ├── SectionBreakdown.jsx  # Section rating/feedback tabs
            ├── BulletOptimizer.jsx   # XYZ formula optimizer UI
            ├── SkillRoadmap.jsx      # Learning roadmap tree
            └── LoadingState.jsx      # Animated loading milestones
```

---

## ⚡ Quick Start (Local Setup)

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm (or yarn/pnpm)
- (Optional) A [Google Gemini API key](https://ai.google.dev/) for live AI analysis

### 1️⃣ Backend Setup (FastAPI)

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv

# Activate it:
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your environment file
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# Run the server
uvicorn main:app --reload --port 8000
```

The backend will be live at `http://localhost:8000`.
> 💡 If you skip setting `GEMINI_API_KEY`, the app automatically runs in **Mock Fallback Mode**.

### 2️⃣ Frontend Setup (React + Vite)

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Create your environment file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# Start the dev server
npm run dev
```

The frontend will be live at `http://localhost:5173`.

### 3️⃣ Open the App
Visit `http://localhost:5173` in your browser, upload a resume, paste a job description, and hit **Analyze**.

---

## 🌐 Deployment

### Backend → Render

1. Push your code to GitHub (if not already done).
2. Go to [Render](https://render.com/) → **New +** → **Web Service**.
3. Connect your GitHub repository and select the `backend/` directory as the root.
4. Configure the service:
   | Setting | Value |
   |---|---|
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
5. Add environment variables under **Environment**:
   - `GEMINI_API_KEY` = `your_gemini_api_key_here`
6. Deploy. Render will give you a live URL like:
   ```
   https://your-app-name.onrender.com
   ```
7. Test it: visit `https://your-app-name.onrender.com/api/health`.

### Frontend → Vercel

1. Go to [Vercel](https://vercel.com/) → **Add New** → **Project**.
2. Import your GitHub repository and set the **Root Directory** to `frontend/`.
3. Vercel auto-detects Vite — confirm these settings:
   | Setting | Value |
   |---|---|
   | **Framework Preset** | Vite |
   | **Build Command** | `npm run build` |
   | **Output Directory** | `dist` |
4. Add an environment variable:
   - `VITE_API_BASE_URL` = `https://your-app-name.onrender.com`
5. Deploy. Your app will be live at:
   ```
   https://your-app-name.vercel.app
   ```
6. **Important:** Update CORS settings in `backend/main.py` to allow requests from your Vercel domain.

---

## 🔐 Environment Variables

**Backend (`backend/.env`)**
| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | No | Your Google Gemini API key. If omitted, the app runs in **Mock Fallback Mode**. |

**Frontend (`frontend/.env`)**
| Variable | Required | Description |
|---|---|---|
| `VITE_API_BASE_URL` | No | Base URL of the FastAPI backend. Defaults to `http://localhost:8000` in development. |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check for the backend service. |
| `POST` | `/api/analyze` | Accepts a resume file + job description, returns ATS score, keyword gaps, and section feedback. |
| `POST` | `/api/optimize-bullet` | Accepts a raw bullet point, returns an AI-optimized version using the XYZ formula. |

---

## 🗺️ Roadmap / Future Improvements

- [ ] User authentication & resume history
- [ ] Multi-resume comparison against one job description
- [ ] Export analysis report as PDF
- [ ] Support for additional file formats (`.txt`, `.rtf`)
- [ ] Browser extension for one-click analysis from job boards

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

- [Google Gemini API](https://ai.google.dev/) for AI-powered analysis
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [Vite](https://vitejs.dev/) for blazing-fast frontend tooling
- [Lucide Icons](https://lucide.dev/) for the icon set

---

<p align="center">Built with ❤️ to help job seekers land more interviews.</p>

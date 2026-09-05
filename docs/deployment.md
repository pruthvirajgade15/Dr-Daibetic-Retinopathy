# 🚀 Production Deployment Guide: Hugging Face Spaces & Vercel

This guide walks you through deploying the **DR-Screening-AI** platform to production using:
1. **Hugging Face Spaces (or Render)** for the FastAPI + PyTorch Backend API.
2. **Vercel** for the Next.js 14 Frontend.

---

## 🏗️ Architecture Overview

```
 ┌───────────────────────────┐         HTTPS / REST API         ┌───────────────────────────┐
 │   Vercel (Frontend)       │ ───────────────────────────────> │   Hugging Face Spaces     │
 │   Next.js 14 App Router   │ <─────────────────────────────── │   FastAPI + PyTorch DL    │
 │   https://*.vercel.app    │        JSON + XAI Reports        │   https://*.hf.space      │
 └───────────────────────────┘                                  └───────────────────────────┘
```

---

## Part 1: Deploy Backend on Hugging Face Spaces (Free Cloud GPU/CPU)

Hugging Face Spaces provides free hosting for machine learning models and FastAPI backends via Docker.

### Step 1: Create a New Space on Hugging Face
1. Log in to [Hugging Face](https://huggingface.co/) (or create an account).
2. Click on your profile icon (top right) $\rightarrow$ **"New Space"**.
3. Configure the Space settings:
   - **Space Name:** `dr-screening-backend` (or your choice).
   - **License:** `MIT`.
   - **Select the Space SDK:** Choose **`Docker`** $\rightarrow$ **`Blank`**.
   - **Space Hardware:** `CPU Basic` (Free) or `T4 small` (GPU).
   - **Visibility:** `Public` (recommended so Vercel can access the API).
4. Click **"Create Space"**.

---

### Step 2: Push Backend Code to Hugging Face Space

You can push the `backend/` folder contents directly to your Hugging Face Space Git repository:

```powershell
# Clone your newly created Hugging Face Space repository
git clone https://huggingface.co/spaces/<YOUR_HF_USERNAME>/dr-screening-backend hf-backend-space

# Copy backend files into the cloned space directory
Copy-Item -Path "backend\*" -Destination "hf-backend-space" -Recurse -Force

# Navigate to the space directory
cd hf-backend-space

# Commit and push to Hugging Face
git add .
git commit -m "feat: deploy FastAPI PyTorch DR screening backend"
git push
cd ..
```

---

### Step 3: Verify Hugging Face Space Endpoint

1. Once the build finishes (takes ~1-2 minutes), Hugging Face will show **"Running"**.
2. Hugging Face Spaces exposes your API directly at:
   👉 **`https://<YOUR_HF_USERNAME>-dr-screening-backend.hf.space`**
3. Verify the health check by visiting:
   - `https://<YOUR_HF_USERNAME>-dr-screening-backend.hf.space/api/health`
   - Interactive Swagger API docs: `https://<YOUR_HF_USERNAME>-dr-screening-backend.hf.space/docs`

---

## Part 2: Deploy Frontend on Vercel (Next.js 14)

### Step 1: Push your Code to GitHub
Ensure your repository is pushed to GitHub:
```powershell
git add .
git commit -m "feat: ready for render & vercel deployment"
git push origin main
```

---

### Step 2: Create a New Web Service on Render
1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click **"New +"** in the top right and select **"Web Service"**.
3. Connect your GitHub repository (`Dr-Daibetic-Retinopathy`).

---

### Step 3: Configure Web Service Settings
Fill in the deployment settings as follows:

| Field | Setting |
| :--- | :--- |
| **Name** | `dr-screening-backend` |
| **Region** | Select closest region (e.g. `Frankfurt`, `Oregon`, `Singapore`) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free or Starter ($7/mo recommended for faster PyTorch CPU inference) |

---

### Step 4: Add Environment Variables
Under the **Environment Variables** section on Render, add:

| Key | Value | Notes |
| :--- | :--- | :--- |
| `PYTHON_VERSION` | `3.10.11` | Ensures consistent Python version |
| `ENVIRONMENT` | `production` | Production mode |
| `PORT` | `10000` | Render injects this automatically |

---

### Step 5: Configure Health Check Path
Under **Advanced**:
- **Health Check Path:** `/api/health`

Click **"Create Web Service"**. Render will install dependencies, load the EfficientNet weights, and start FastAPI.

Once deployed, copy your backend URL:  
👉 `https://dr-screening-backend.onrender.com`

---

## Part 2: Deploying the Frontend on Vercel

### Step 1: Import Project into Vercel
1. Log in to [Vercel Dashboard](https://vercel.com/).
2. Click **"Add New..."** -> **"Project"**.
3. Import your GitHub repository (`Dr-Daibetic-Retinopathy`).

---

### Step 2: Configure Project Settings
In the Vercel project configuration screen:

1. **Framework Preset:** `Next.js`
2. **Root Directory:** Click **Edit** and select **`frontend`** (🚨 **Critical Step**).
3. **Build Command:** `npm run build` (Default)
4. **Output Directory:** `.next` (Default)
5. **Install Command:** `npm install` (Default)

---

### Step 3: Configure Environment Variables
Under **Environment Variables**, add:

| Key | Value | Example |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_BACKEND_URL` | Your Render Backend URL | `https://dr-screening-backend.onrender.com` |

---

### Step 4: Deploy
Click **"Deploy"**. Vercel will:
- Install Next.js dependencies.
- Compile and optimize production bundles.
- Assign your production URL: 👉 `https://dr-screening-frontend.vercel.app`

---

## Part 3: Verification & End-to-End Testing

1. Open your Vercel URL in your browser: `https://dr-screening-frontend.vercel.app`.
2. Navigate to `/screening`.
3. Upload a retinal fundus image (e.g., from `ml-training/data/processed/` or any test sample).
4. Click **"Run AI Retinal Screening"**.
5. Verify that:
   - **Quality Score** calculates clarity and illumination.
   - **5-Grade ICDR Prediction** displays stage & confidence.
   - **Grad-CAM Viewer** overlays saliency heatmaps with interactive opacity slider.
   - **Clinical Report** button allows downloading/printing the A4 clinical sheet.

---

## 🔧 Troubleshooting & Tips

### Cold Starts on Render Free Tier
Render free instances spin down after 15 minutes of inactivity. The first API request may take ~30-45 seconds to wake up.
- To keep it warm, use a free uptime monitor (like [UptimeRobot](https://uptimerobot.com/)) pinging `https://your-backend.onrender.com/api/health` every 10 minutes.

### CORS Configuration
The backend is pre-configured with wildcard and domain origins in [`backend/app/core/config.py`](file:///d:/GitHub/Dr-Daibetic-Retinopathy/backend/app/core/config.py):
```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "*"
]
```
If you want to restrict CORS to only your Vercel domain, update `ALLOWED_ORIGINS` to include `https://your-app.vercel.app`.

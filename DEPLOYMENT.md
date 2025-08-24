# 🚀 Free Hosting Guide for AI Friend

## **Option 1: Render (Recommended - Easiest)**

### **Step 1: Prepare Your Repository**
1. Push your code to GitHub
2. Make sure all files are committed

### **Step 2: Deploy on Render**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `hothasha-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python api_server.py`
   - **Plan**: Free

### **Step 3: Deploy Frontend**
1. Click "New +" → "Static Site"
2. Connect the same repository
3. Configure:
   - **Name**: `hothasha-web`
   - **Build Command**: `echo "No build needed"`
   - **Publish Directory**: `static`
   - **Plan**: Free

### **Step 4: Update Frontend URL**
Update `static/index.html` with your Render API URL:
```javascript
this.apiUrl = 'https://your-api-name.onrender.com';
```

---

## **Option 2: Railway**

### **Step 1: Deploy**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect and deploy

### **Step 2: Get URL**
- Railway will provide a URL like: `https://your-app-name.railway.app`
- Update your frontend with this URL

---

## **Option 3: Heroku (Limited Free Tier)**

### **Step 1: Install Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Or download from heroku.com
```

### **Step 2: Deploy**
```bash
# Login to Heroku
heroku login

# Create app
heroku create hothasha-gf

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open app
heroku open
```

---

## **Option 4: Vercel (Frontend Only)**

### **Step 1: Deploy Frontend**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `static`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

### **Step 2: Deploy Backend Separately**
Use Render or Railway for the API, then update the frontend URL.

---

## **Option 5: Netlify (Frontend Only)**

### **Step 1: Deploy**
1. Go to [netlify.com](https://netlify.com)
2. Drag and drop your `static` folder
3. Or connect GitHub repository

### **Step 2: Configure**
- **Publish directory**: `static`
- **Build command**: Leave empty

---

## **🔧 Important Notes:**

### **Model Storage**
For free hosting, you'll need to store your model files externally:

1. **Hugging Face Hub** (Recommended):
   ```bash
   # Upload your model to Hugging Face
   huggingface-cli login
   huggingface-cli upload your-username/hothasha-model ./trained_model
   ```

2. **Update API to load from HF**:
   ```python
   # In api_server.py
   model_path = "your-username/hothasha-model"
   ```

### **Environment Variables**
Set these in your hosting platform:
- `HUGGINGFACE_TOKEN`: Your HF token
- `PORT`: Port number (auto-set by platform)

### **CORS Configuration**
Update CORS in `api_server.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## **🎯 Recommended Setup:**

1. **Backend**: Render (API)
2. **Frontend**: Vercel or Netlify
3. **Model**: Hugging Face Hub
4. **Database**: None needed (stateless)

---

## **💰 Cost: FREE**

All these options offer free tiers that are perfect for your chat application!

---

## **🚀 Quick Start (Render):**

1. **Fork/Clone** this repository
2. **Push** to GitHub
3. **Deploy** on Render (follow Option 1)
4. **Update** frontend URL
5. **Share** your live app! 🎉

Your "AI Friend" will be live and accessible worldwide! 💕

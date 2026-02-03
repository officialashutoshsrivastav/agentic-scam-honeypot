## Railway Deployment Steps

1. Push code to GitHub
2. Go to https://railway.app
3. New Project -> Deploy from GitHub
4. Set Environment Variables:
   - API_KEY
   - OPENAI_API_KEY
5. Railway auto-builds and gives public URL

## Run Locally
pip install -r requirements.txt
uvicorn main:app --reload
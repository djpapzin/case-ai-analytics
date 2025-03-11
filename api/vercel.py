from main import app
from fastapi.middleware.cors import CORSMiddleware

# Configure CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handler for Vercel serverless function
handler = app 
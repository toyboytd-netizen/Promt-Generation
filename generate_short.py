import os
import random
from datetime import datetime
import google.generativeai as genai
from github import Github

# --- CONFIGURATION (GitHub Secrets se values uthayega) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GITHUB_TOKEN = os.environ.get("Token_git")
REPO_NAME = "toyboytd-netizen/Promt-Generation"

# 1. Gemini Configure karein
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

# 2. Unique topics ki list taaki har baar naya video bane
topics = [
    "Mysterious deep ocean secrets that science cannot explain",
    "Unsolved historical mysteries of ancient civilizations",
    "Creepy urban legends from abandoned places",
    "Psychological tricks that feel illegal to know",
    "Bizarre space anomalies discovered recently",
]

selected_topic = random.choice(topics)
prompt = f"""
Aap ek professional YouTube Shorts creator hain. Topic: '{selected_topic}'.
Mujhe iske liye ek engaging YouTube Short video ki script aur visual prompts chahiye.
Format:
1. Video Title
2. Hook (0-3 sec)
3. Narration Script (Voiceover ke liye)
4. Scene-wise Visual Prompts (AI image/video generation ke liye)
5. Description & Hashtags
"""

print(f"Generating content for topic: {selected_topic}...")
response = model.generate_content(prompt)
script_content = response.text

# 3. GitHub par file save/commit karna
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

filename = f"shorts/short_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

try:
  repo.create_file(
      path=filename,
      message=f"New YouTube Short script generated for {selected_topic}",
      content=script_content,
      branch="main",
  )
  print(f"Successfully committed {filename} to GitHub!")
except Exception as e:
  print(f"Error committing to GitHub: {e}")

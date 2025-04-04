# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
# import os

# app = Flask(__name__)

# # Setup Gemini API key
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Add to Render later
# genai.configure(api_key=GOOGLE_API_KEY)

# # System prompt
# system_prompt = """
# You are HomeOrganizer, a helpful assistant specialized in providing advice on home organization and tidying.
# Your purpose is to help users organize their living spaces effectively.

# You can:
# - Provide step-by-step guides for organizing different areas of the home
# - Suggest decluttering methods and strategies
# - Recommend storage solutions
# - Give advice on maintaining organized spaces
# - Help create personalized organization systems

# Be friendly, supportive, and provide practical advice that users can implement right away.
# """

# # Area-specific advice
# organization_tips = {
#     "kitchen": [
#         "Group similar items together",
#         "Use clear containers for pantry items",
#         "Install cabinet organizers for pots and pans",
#         "Consider a pegboard for utensils"
#     ],
#     "bedroom": [
#         "Use under-bed storage for seasonal items",
#         "Install closet dividers for clothes",
#         "Use drawer organizers for small items",
#         "Consider a bedside caddy for essentials"
#     ],
#     "bathroom": [
#         "Use shower caddies for toiletries",
#         "Install towel hooks or bars",
#         "Use drawer dividers for small items",
#         "Consider over-the-toilet storage"
#     ],
#     "living room": [
#         "Use multi-functional furniture with storage",
#         "Install floating shelves for decor and books",
#         "Use baskets to organize blankets and pillows",
#         "Consider a coffee table with storage"
#     ],
#     "home office": [
#         "Use vertical file organizers",
#         "Install a cable management system",
#         "Use drawer dividers for small supplies",
#         "Consider wall-mounted shelves for reference materials"
#     ]
# }

# # Check for area-specific advice
# def get_area_specific_tips(msg):
#     msg = msg.lower()
#     for area, tips in organization_tips.items():
#         if area in msg:
#             return f"\nSpecialized tips for {area.upper()}:\n" + "\n".join([f"- {tip}" for tip in tips])
#     return ""

# # Gemini model setup
# model = genai.GenerativeModel(
#     model_name="gemini-1.5-pro",
#     system_instruction=system_prompt,
#     generation_config={
#         "temperature": 0.7,
#         "top_p": 0.95,
#         "top_k": 40,
#         "max_output_tokens": 1024,
#     }
# )

# chat = model.start_chat(history=[])

# # Routes
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat_route():
#     user_input = request.json.get("message")
#     response = chat.send_message(user_input)
#     area_tips = get_area_specific_tips(user_input)
#     full_response = response.text + ("\n\n" + area_tips if area_tips else "")
#     return jsonify({"response": full_response})

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Setup Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "your-gemini-api-key"  # Fallback for local testing

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# System prompt
system_prompt = """
You are HomeOrganizer, a helpful assistant specialized in providing advice on home organization and tidying.
Your purpose is to help users organize their living spaces effectively.

You can:
- Provide step-by-step guides for organizing different areas of the home
- Suggest decluttering methods and strategies
- Recommend storage solutions
- Give advice on maintaining organized spaces
- Help create personalized organization systems

Be friendly, supportive, and provide practical advice that users can implement right away.
"""

# Area-specific advice
tips = {
    "kitchen": [
        "Group similar items together",
        "Use clear containers for pantry items",
        "Install cabinet organizers for pots and pans",
        "Consider a pegboard for utensils"
    ],
    "bedroom": [
        "Use under-bed storage for seasonal items",
        "Install closet dividers for clothes",
        "Use drawer organizers for small items",
        "Consider a bedside caddy for essentials"
    ],
    "bathroom": [
        "Use shower caddies for toiletries",
        "Install towel hooks or bars",
        "Use drawer dividers for small items",
        "Consider over-the-toilet storage"
    ],
    "living room": [
        "Use multi-functional furniture with storage",
        "Install floating shelves for decor and books",
        "Use baskets to organize blankets and pillows",
        "Consider a coffee table with storage"
    ],
    "home office": [
        "Use vertical file organizers",
        "Install a cable management system",
        "Use drawer dividers for small supplies",
        "Consider wall-mounted shelves for reference materials"
    ]
}

def get_area_tips(msg):
    msg = msg.lower()
    for area, area_tips in tips.items():
        if area in msg:
            return f"\nSpecialized tips for {area.upper()}:\n" + "\n".join([f"- {tip}" for tip in area_tips])
    return ""

# Gemini model setup
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_prompt,
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
)

chat = model.start_chat(history=[])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    user_input = request.json.get("message")
    response = chat.send_message(user_input)
    area_tips = get_area_tips(user_input)
    full_response = response.text + ("\n\n" + area_tips if area_tips else "")
    return jsonify({"response": full_response})

if __name__ == '__main__':
    app.run(debug=True)

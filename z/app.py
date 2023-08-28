import openai
from flask import Flask, request, render_template
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask
app = Flask(__name__)

# Configure your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

# Render the initial HTML form
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Handle form submission and email generation
@app.route("/", methods=["POST"])
def generate_emails():
    # Get user inputs from the form
    campaign_goal = request.form.get("campaign_goal")
    brand_tone = request.form.get("brand_tone")
    industry = request.form.get("industry")
    tell_more = request.form.get("tell_more")

    # Generate 5 emails using a single API call
    email_templates = generate_email_templates(campaign_goal, brand_tone, industry, tell_more, num_emails=5)

    # Render the HTML template with the generated emails
    return render_template("results.html", email_templates=email_templates)

def generate_email_templates(campaign_goal, brand_tone, industry, tell_more, num_emails=1):
    email_templates = []

    # Generate emails using OpenAI's ChatGPT API
    prompt = f"Generate {num_emails} emails for a campaign with the following details:\n\nCampaign Goal: {campaign_goal}\nBrand Tone: {brand_tone}\nIndustry: {industry}\nTell us more: {tell_more}\n\n"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,  # Adjust max tokens as needed
        n=num_emails  # Specify the number of emails to generate
    )

    for email in response.choices:
        email_templates.append(email.text.strip())

    return email_templates

if __name__ == "__main__":
    app.run(debug=True)

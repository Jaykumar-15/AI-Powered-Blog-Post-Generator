from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from seo_fetcher import fetch_seo_data
from ai_generator import generate_blog_post
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

load_dotenv()

app = Flask(__name__)

@app.route('/generate', methods=['GET'])
def generate():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Please provide a keyword"}), 400

    # Placeholder SEO data
    seo_data = fetch_seo_data(keyword)


    #Generate blog post using OpenAI
    blog_post = generate_blog_post(keyword, seo_data)


    # Save to posts folder
    filename = f"posts/{keyword.replace(' ', '_').lower()}.md"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(blog_post)

    return jsonify({
        "keyword": keyword,
        "seo_data": seo_data,
        "blog_post": blog_post
    })

if __name__ == '__main__':
    app.run(debug=True)

POSTS_DIR = "posts"
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

def auto_generate_daily_blog():
    keyword = "wireless earbuds"  # You can change this
    seo_data = fetch_seo_data(keyword)
    blog_post = generate_blog_post(keyword, seo_data)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{POSTS_DIR}/{keyword.replace(' ', '_')}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(blog_post)

    print(f"[{timestamp}] Blog post for '{keyword}' saved to {filename}")

scheduler = BackgroundScheduler()
scheduler.add_job(auto_generate_daily_blog, 'interval', days=1)
scheduler.start()

# 🔁 Trigger manually once to test
auto_generate_daily_blog()
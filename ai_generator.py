import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_blog_post(keyword, seo_data):
    prompt = f"""
Write a high-quality blog post about the keyword: "{keyword}".

Include:
- Introduction
- SEO stats: Search Volume: {seo_data['search_volume']}, Keyword Difficulty: {seo_data['keyword_difficulty']}, Avg CPC: {seo_data['avg_cpc']}
- Main content with 2–3 subheadings
- A conclusion
- Two affiliate links using this exact format (do NOT include inner links or brackets):
  {{AFF_LINK_1: Text you want to appear for the link}}
  {{AFF_LINK_2: Text you want to appear for the second link}}

Return the blog in Markdown format.
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a helpful blog writing assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
        )

        if response.status_code != 200:
            return f"Error from OpenRouter: {response.status_code} - {response.text}"

        data = response.json()

        if "choices" not in data:
            return f"Unexpected response format: {data}"

        blog = data["choices"][0]["message"]["content"]

        # 🔧 Function to convert {AFF_LINK_1: text} to [text](URL)
        def replace_affiliate_links(blog: str, keyword: str) -> str:
            search_query = keyword.strip()
            google_link = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            amazon_link = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    
            # Replace affiliate placeholders with actual links
            blog = re.sub(r"\{AFF_LINK_1:\s*(.*?)\}", rf"[\1]({google_link})", blog)
            blog = re.sub(r"\{AFF_LINK_2:\s*(.*?)\}", rf"[\1]({amazon_link})", blog)
            return blog


        blog = replace_affiliate_links(blog, keyword)

        return blog

    except Exception as e:
        return f"Error generating blog: {str(e)}"

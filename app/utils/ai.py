import cohere
from app.config.settings import settings
from typing import Optional, Tuple

class CohereAI:
    def __init__(self):
        self.co = cohere.Client(settings.COHERE_API_KEY)

    def generate_blog(self, prompt: str) -> Tuple[Optional[str], Optional[str]]:
        """Generate a blog post from a prompt"""
        try:
            blog_prompt = f"""Write a professional blog post about: {prompt}

            The blog post should be well-structured with:
            - An engaging title
            - A compelling introduction
            - Well-organized body paragraphs
            - A strong conclusion
            
            Make it informative, engaging, and SEO-friendly."""

            response = self.co.generate(
                model='command',
                prompt=blog_prompt,
                max_tokens=1000,
                temperature=0.7,
                stop_sequences=[],
                return_likelihoods='NONE'
            )

            return response.generations[0].text.strip(), None
        except Exception as e:
            return None, str(e)

    def convert_to_social_posts(self, blog_content: str) -> Tuple[dict, Optional[str]]:
        """Convert blog content to social media posts"""
        try:
            social_prompt = f"""Convert this blog post into two different social media posts:
            1. A Facebook post (max 500 characters)
            2. A LinkedIn post (max 3000 characters)

            Blog content:
            {blog_content}

            Format the output exactly like this:
            FACEBOOK:
            [Facebook post content]

            LINKEDIN:
            [LinkedIn post content]"""

            response = self.co.generate(
                model='command',
                prompt=social_prompt,
                max_tokens=1000,
                temperature=0.7,
                stop_sequences=[],
                return_likelihoods='NONE'
            )

            output = response.generations[0].text.strip()
            
            # Parse the output
            parts = output.split('\n\n')
            facebook_post = parts[0].replace('FACEBOOK:', '').strip()
            linkedin_post = parts[1].replace('LINKEDIN:', '').strip()

            return {
                'facebook': facebook_post,
                'linkedin': linkedin_post
            }, None
        except Exception as e:
            return {}, str(e) 
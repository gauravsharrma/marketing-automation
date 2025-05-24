import facebook
import requests
from typing import Optional
from app.config.settings import settings

class FacebookAPI:
    def __init__(self):
        self.graph = facebook.GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)

    def post_to_facebook(self, message: str) -> tuple[bool, Optional[str]]:
        """Post content to Facebook"""
        try:
            self.graph.put_object(
                parent_object="me",
                connection_name="feed",
                message=message
            )
            return True, None
        except facebook.GraphAPIError as e:
            return False, str(e)

class LinkedInAPI:
    def __init__(self):
        self.access_token = settings.LINKEDIN_ACCESS_TOKEN
        self.api_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def post_to_linkedin(self, text: str) -> tuple[bool, Optional[str]]:
        """Post content to LinkedIn"""
        try:
            # First get the user's URN
            author = self._get_user_urn()
            
            # Create the post
            post_url = f"{self.api_url}/ugcPosts"
            post_data = {
                "author": f"urn:li:person:{author}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            response = requests.post(post_url, headers=self.headers, json=post_data)
            if response.status_code == 201:
                return True, None
            else:
                return False, f"LinkedIn API Error: {response.text}"

        except Exception as e:
            return False, str(e)

    def _get_user_urn(self) -> str:
        """Get the user's URN (Uniform Resource Name)"""
        response = requests.get(
            f"{self.api_url}/me",
            headers=self.headers
        )
        return response.json().get("id") 
import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def _1setUp(self):
        self.client = app.test_client()

    def _2test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>TyRoyLog Portfolio</title>" in html
        assert "<html lang=\"en\">" in html
        assert "<a href=\"/loganswork/\" class=\"homeLink\">" in html

    
    def _3test_empty_timeline(self):
        response = self.client.get("api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def _4test_timeline(self):
        get_response = self.client.get("api/timeline_post")
        assert get_response.status_code == 200
        assert get_response.is_json
        assert "timeline_posts" in json
        json = get_response.get_json()
        post_amt_before = len(json["timeline_posts"])
        post_response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert post_response.status_code == 200
        assert len(json["timeline_posts"]) == (post_amt_before + 1)
        first_post = json["timeline_posts"][0]
        assert "name" in first_post
        assert first_post['name'] == "John Doe"
        # assert "John Doe" and "john@example.com" and "Hello world, I'm John!" in json

    def _5test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html






        
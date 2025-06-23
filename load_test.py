# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import uuid
from locust import HttpUser, task, between


class ResearchAgentUser(HttpUser):
    """Load test user for the Research Agent."""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Set up user session when starting."""
        self.user_id = f"user_{uuid.uuid4()}"
        self.session_id = f"session_{uuid.uuid4()}"
        
        # Create session first  
        session_data = {"state": {"preferred_language": "English", "visit_count": 1}}
        
        self.client.put(
            f"/apps/research_agent/users/{self.user_id}/sessions/{self.session_id}",
            headers={"Content-Type": "application/json"},
            json=session_data,
        )

    @task(3)
    def research_topics(self):
        """Test researching various topics with different focus areas."""
        # Random topic and focus selection
        topics = ["artificial intelligence", "climate change", "blockchain"]
        focus_areas = ["general", "technical", "business", "social"]
        
        topic = random.choice(topics)
        focus = random.choice(focus_areas)
        
        # Vary the message format
        message_formats = [
            f"Research {topic} with a {focus} focus",
            f"Can you research {topic} from a {focus} perspective?",
            f"Tell me about {topic} with a focus on {focus} aspects",
            f"What can you tell me about {topic}?",
            f"Explain {topic} in simple terms"
        ]
        
        message_data = {
            "message": random.choice(message_formats),
            "session_id": self.session_id,
        }
        
        response = self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )
        
        if response.status_code == 200:
            data = response.json()
            # Validate response structure
            if "response" in data and "conversation_id" in data:
                self.conversation_id = data["conversation_id"]

    @task(2)
    def analyze_trends(self):
        """Test trend analysis across different domains."""
        # Random domain selection and varied message formats
        domains = ["technology", "business", "science"]
        domain = random.choice(domains)
        
        message_formats = [
            f"Analyze current trends in {domain}",
            f"What are the emerging trends in {domain}?",
            f"Tell me about {domain} trends",
            f"What's happening in the {domain} space?",
            f"Analyze trends in {domain} research" if domain == "science" else f"What are the latest {domain} developments?"
        ]
        
        message_data = {
            "message": random.choice(message_formats),
            "session_id": self.session_id,
        }
        
        self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )

    def on_stop(self):
        """Clean up when user session ends."""
        # Optionally submit feedback
        if hasattr(self, 'conversation_id'):
            feedback_data = {
                "score": random.randint(3, 5),
                "text": "Load test feedback",
                "invocation_id": self.conversation_id,
                "user_id": self.user_id
            }
            
            self.client.post(
                "/feedback",
                headers={"Content-Type": "application/json"},
                json=feedback_data,
            ) 
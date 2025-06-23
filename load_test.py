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
    def research_artificial_intelligence(self):
        """Test researching artificial intelligence with different focus areas."""
        focus_areas = ["general", "technical", "business", "social"]
        focus = random.choice(focus_areas)
        
        message_data = {
            "message": f"Research artificial intelligence with a {focus} focus",
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
    def research_climate_change(self):
        """Test researching climate change with different focus areas."""
        focus_areas = ["general", "technical", "business", "social"]
        focus = random.choice(focus_areas)
        
        message_data = {
            "message": f"Can you research climate change from a {focus} perspective?",
            "session_id": self.session_id,
        }
        
        self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )

    @task(2)
    def research_blockchain(self):
        """Test researching blockchain technology."""
        focus_areas = ["general", "technical", "business", "social"]
        focus = random.choice(focus_areas)
        
        message_data = {
            "message": f"Tell me about blockchain technology with a focus on {focus} aspects",
            "session_id": self.session_id,
        }
        
        self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )

    @task(2)
    def analyze_technology_trends(self):
        """Test analyzing trends in technology domain."""
        message_data = {
            "message": "Analyze current trends in technology",
            "session_id": self.session_id,
        }
        
        self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )

    @task(1)
    def analyze_business_trends(self):
        """Test analyzing trends in business domain."""
        message_data = {
            "message": "What are the emerging trends in business?",
            "session_id": self.session_id,
        }
        
        self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )

    @task(1)
    def analyze_science_trends(self):
        """Test analyzing trends in science domain."""
        message_data = {
            "message": "Analyze trends in scientific research",
            "session_id": self.session_id,
        }
        
        self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )

    @task(1)
    def general_research_query(self):
        """Test general research queries."""
        queries = [
            "What can you tell me about artificial intelligence?",
            "How does climate change affect businesses?",
            "Explain blockchain in simple terms",
            "What are the latest technology trends?",
            "How is AI changing the business landscape?"
        ]
        
        message_data = {
            "message": random.choice(queries),
            "session_id": self.session_id,
        }
        
        self.client.post(
            f"/apps/research_agent/users/{self.user_id}/conversations",
            headers={"Content-Type": "application/json"},
            json=message_data,
        )

    @task(1)
    def test_unknown_topic(self):
        """Test error handling with unknown topics."""
        unknown_topics = [
            "Research quantum mechanics",
            "Tell me about cryptocurrency regulations",  
            "Analyze trends in space exploration",
            "What about renewable energy trends?"
        ]
        
        message_data = {
            "message": random.choice(unknown_topics),
            "session_id": self.session_id,
        }
        
        # This should trigger error handling in the agent
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
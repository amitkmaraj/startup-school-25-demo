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

import os
from pathlib import Path

import google.auth
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.cloud import logging as google_cloud_logging

# Load environment variables from .env file in root directory
root_dir = Path(__file__).parent.parent
dotenv_path = root_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Use default project from credentials if not in .env
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

logging_client = google_cloud_logging.Client()
logger = logging_client.logger("researcher-agent")


def research_topic(topic: str, focus_area: str = "general") -> dict:
    """Provides research insights and analysis on a given topic based on existing knowledge.

    Args:
        topic (str): The topic to research (e.g., "artificial intelligence", "climate change", "blockchain").
        focus_area (str): The area of focus for the research (e.g., "general", "technical", "business", "social").

    Returns:
        dict: A dictionary containing the research information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'research' key with detailed insights.
              If 'error', includes an 'error_message' key.
    """
    logger.log_text(
        f"--- Tool: research_topic called for topic: {topic}, focus: {focus_area} ---", severity="INFO"
    )
    
    topic_normalized = topic.lower().strip()
    focus_normalized = focus_area.lower().strip()

    # Knowledge base for various topics
    knowledge_base = {
        "artificial intelligence": {
            "general": "AI is a rapidly evolving field focused on creating machines that can perform tasks typically requiring human intelligence. Key areas include machine learning, natural language processing, computer vision, and robotics. Current trends show significant advancement in large language models, generative AI, and autonomous systems.",
            "technical": "AI encompasses various approaches including supervised/unsupervised learning, neural networks, deep learning architectures (CNNs, RNNs, Transformers), reinforcement learning, and symbolic AI. Modern architectures like attention mechanisms and transformer models have revolutionized NLP and multimodal applications.",
            "business": "AI is transforming industries through automation, predictive analytics, personalized experiences, and decision support systems. Companies are investing heavily in AI infrastructure, talent acquisition, and ethical AI practices. Key challenges include ROI measurement, data quality, and integration complexity.",
            "social": "AI raises important questions about job displacement, privacy, bias in algorithms, and the future of human-machine collaboration. Discussions focus on AI governance, ethical frameworks, transparency, and ensuring AI benefits society broadly."
        },
        "climate change": {
            "general": "Climate change refers to long-term shifts in global temperatures and weather patterns, primarily driven by human activities since the Industrial Revolution. Key indicators include rising global temperatures, melting ice caps, sea level rise, and extreme weather events.",
            "technical": "Climate science involves understanding greenhouse gas emissions (CO2, CH4, N2O), feedback loops, climate modeling, and mitigation technologies. Solutions include renewable energy systems, carbon capture, energy efficiency, and sustainable transportation technologies.",
            "business": "Climate change presents both risks and opportunities for businesses. Companies are adopting sustainability practices, ESG reporting, carbon accounting, and climate risk assessments. Green finance and sustainable business models are becoming competitive advantages.",
            "social": "Climate change disproportionately affects vulnerable populations and raises questions of climate justice, adaptation strategies, and international cooperation. Social movements and policy advocacy play crucial roles in driving climate action."
        },
        "blockchain": {  
            "general": "Blockchain is a distributed ledger technology that maintains a continuously growing list of records, linked and secured using cryptography. It enables decentralized, transparent, and immutable record-keeping without requiring a central authority.",
            "technical": "Blockchain systems use cryptographic hashing, consensus mechanisms (Proof of Work, Proof of Stake), smart contracts, and distributed networks. Key technical challenges include scalability, energy consumption, and interoperability between different blockchain networks.",
            "business": "Blockchain applications span cryptocurrency, supply chain management, digital identity, decentralized finance (DeFi), and non-fungible tokens (NFTs). Businesses are exploring blockchain for transparency, reducing intermediaries, and creating new business models.",
            "social": "Blockchain raises questions about financial inclusion, regulatory frameworks, energy consumption, and the decentralization of traditional institutions. It has potential to increase transparency and reduce corruption in various sectors."
        }
    }

    # Check if topic exists in knowledge base
    if topic_normalized in knowledge_base:
        topic_data = knowledge_base[topic_normalized]
        if focus_normalized in topic_data:
            research_content = topic_data[focus_normalized]
        else:
            # Default to general if specific focus not found
            research_content = topic_data.get("general", "Limited information available for this focus area.")
        
        return {
            "status": "success",
            "research": {
                "topic": topic,
                "focus_area": focus_area,
                "insights": research_content,
                "methodology": "Analysis based on existing knowledge base",
                "last_updated": "Knowledge current as of training data"
            }
        }
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have comprehensive research data for '{topic}'. Available topics include: artificial intelligence, climate change, blockchain."
        }


def analyze_trends(domain: str) -> dict:
    """Analyzes current trends and developments in a specific domain.

    Args:
        domain (str): The domain to analyze trends for (e.g., "technology", "business", "science").

    Returns:
        dict: A dictionary containing trend analysis.
    """
    logger.log_text(
        f"--- Tool: analyze_trends called for domain: {domain} ---", severity="INFO"
    )
    
    domain_normalized = domain.lower().strip()
    
    trend_analysis = {
        "technology": {
            "key_trends": [
                "Generative AI and Large Language Models",
                "Edge Computing and IoT Integration", 
                "Quantum Computing Development",
                "Sustainable Technology Solutions",
                "Extended Reality (AR/VR/MR)"
            ],
            "emerging_patterns": "Technology is moving toward more distributed, intelligent, and sustainable solutions. AI integration is becoming ubiquitous across all tech sectors.",
            "future_outlook": "Continued convergence of AI, cloud computing, and sustainable practices will shape the next decade of technological development."
        },
        "business": {
            "key_trends": [
                "Digital Transformation Acceleration",
                "Remote and Hybrid Work Models",
                "ESG and Sustainability Focus",
                "Customer Experience Personalization",
                "Data-Driven Decision Making"
            ],
            "emerging_patterns": "Businesses are prioritizing agility, sustainability, and customer-centricity while leveraging technology for competitive advantage.",
            "future_outlook": "Organizations that successfully balance human-centered approaches with technological innovation will lead market transformations."
        },
        "science": {
            "key_trends": [
                "Interdisciplinary Research Collaboration",
                "AI-Assisted Scientific Discovery",
                "Open Science and Data Sharing",
                "Climate Science and Environmental Research",
                "Precision Medicine and Biotechnology"
            ],
            "emerging_patterns": "Scientific research is becoming more collaborative, data-intensive, and focused on addressing global challenges.",
            "future_outlook": "Integration of AI tools with traditional scientific methods will accelerate discovery and innovation across all fields."
        }
    }
    
    if domain_normalized in trend_analysis:
        return {
            "status": "success",
            "analysis": trend_analysis[domain_normalized],
            "domain": domain,
            "analysis_date": "Based on current knowledge patterns"
        }
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, trend analysis not available for '{domain}'. Available domains: technology, business, science."
        }


root_agent = Agent(
    name="researcher_agent",
    model="gemini-2.5-flash",
    instruction="""You are a knowledgeable research assistant designed to provide insightful analysis and research on various topics based on your existing knowledge. 

You can help users by:
1. Researching topics and providing comprehensive insights from different perspectives (general, technical, business, social)
2. Analyzing trends and developments in various domains
3. Offering structured, well-reasoned analysis based on available knowledge

Your responses should be informative, balanced, and acknowledge the limitations of working with existing knowledge rather than real-time data. Always be helpful while being transparent about your knowledge boundaries.""",
    tools=[research_topic, analyze_trends],
)

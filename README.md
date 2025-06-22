# Researcher Agent - Deploy and Monitor on Cloud Run

A simple research agent that provides insights and analysis on various topics based on existing knowledge. This agent is designed to be stateless and can be easily deployed on Cloud Run or Google GKE without external dependencies.

## Features

- **Knowledge-based Research**: Provides comprehensive insights on topics like AI, climate change, and blockchain
- **Trend Analysis**: Analyzes current trends in technology, business, and science domains
- **Multiple Perspectives**: Offers general, technical, business, and social viewpoints on topics
- **Stateless Design**: No external database dependencies, suitable for containerized deployment
- **Cloud Monitoring**: Integrated with Google Cloud Logging and Cloud Trace for observability
- **Load Testing**: Includes Locust-based load testing for performance validation

## Deploy Agent to Cloud Run

Deploy the simplified research agent to Cloud Run:

```bash
gcloud run deploy researcher-agent \
                  --source . \
                  --port 8080 \
                  --project {YOUR_PROJECT_ID} \
                  --allow-unauthenticated \
                  --region us-central1 \
                  --min-instances 1
```

## Configure for Load Testing

Deploy a new revision optimized for load testing:

```bash
gcloud run deploy researcher-agent \
                  --source . \
                  --port 8080 \
                  --project {YOUR_PROJECT_ID} \
                  --allow-unauthenticated \
                  --region us-central1 \
                  --concurrency 10 \
                  --memory 2Gi \
                  --cpu 2
```

## Run Load Tests

Trigger the Locust load test with the following command:

```bash
# Create results directory
mkdir -p .results

# Run load test
locust -f load_test.py \
-H {YOUR_CLOUD_RUN_SERVICE_URL} \
--headless \
-t 120s -u 60 -r 5 \
--csv=.results/results \
--html=.results/report.html
```

**Load Test Parameters:**

- **Duration**: 120 seconds
- **Users**: 60 concurrent users
- **Spawn Rate**: 5 users per second
- **Test Scenarios**: Research queries, trend analysis, error handling

## Deploy with Traffic Control

Deploy a new revision without traffic for testing:

```bash
gcloud run deploy researcher-agent \
                  --source . \
                  --port 8080 \
                  --project {YOUR_PROJECT_ID} \
                  --allow-unauthenticated \
                  --region us-central1 \
                  --concurrency 10 \
                  --no-traffic
```

## Local Development

Run the agent locally:

```bash
# Install dependencies
uv sync

# Run the server
uv run python server.py
```

The agent will be available at `http://localhost:8080`

## Agent Capabilities

The researcher agent provides two main tools:

1. **Research Topic**: Get comprehensive insights on various topics

   - Supports multiple focus areas: general, technical, business, social
   - Available topics: artificial intelligence, climate change, blockchain

2. **Analyze Trends**: Get trend analysis for different domains
   - Available domains: technology, business, science
   - Provides key trends, patterns, and future outlook

## Load Test Coverage

The load test suite covers:

- **Research Queries**: AI, climate change, blockchain with different focus areas
- **Trend Analysis**: Technology, business, and science domains
- **Error Handling**: Unknown topics and edge cases
- **Session Management**: User sessions and conversation flows
- **Feedback Collection**: Automated feedback submission

## Monitoring

The agent includes built-in monitoring through:

- **Google Cloud Logging**: All operations and tool calls are logged
- **Cloud Trace**: Request tracing for performance monitoring
- **Feedback API**: Collect user feedback at `/feedback` endpoint
- **Load Test Reports**: Performance metrics and response time analysis

## Architecture

- **Stateless**: No external database dependencies
- **Containerized**: Dockerfile included for easy deployment
- **Scalable**: Designed for Cloud Run auto-scaling
- **Observable**: Integrated monitoring and logging
- **Testable**: Comprehensive load testing framework

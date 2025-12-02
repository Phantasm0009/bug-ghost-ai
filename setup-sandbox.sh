#!/bin/bash
# Bug Ghost AI - Sandbox Setup Script
# Builds all sandbox Docker images for local development

set -e

echo "🏗️  Building Bug Ghost AI Sandbox Images..."
echo ""

# Build Python sandbox
echo "📦 Building Python sandbox..."
docker-compose build sandbox-python

# Build Node.js sandbox
echo "📦 Building Node.js sandbox..."
docker-compose build sandbox-node

# Build Java sandbox
echo "📦 Building Java sandbox..."
docker-compose build sandbox-java

echo ""
echo "✅ All sandbox images built successfully!"
echo ""
echo "Images created:"
docker images | grep bug-ghost-sandbox

echo ""
echo "🚀 You can now start the full stack with:"
echo "   docker-compose up -d"
echo ""
echo "📖 Test sandbox execution:"
echo "   curl -X POST http://localhost:8000/api/runs \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"language\": \"python\", \"code\": \"print(\\\"Hello from sandbox!\\\")\"}'
echo ""

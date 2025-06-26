#!/bin/bash

# AWS EC2 배포 스크립트
# 사용법: ./deploy.sh

set -e

echo "🚀 Starting deployment..."

# 환경변수 파일 확인
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with production environment variables"
    exit 1
fi

# 기존 컨테이너 중지 및 제거
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# 최신 이미지 풀
echo "📥 Pulling latest image..."
docker pull your-username/chatbot-server:latest

# 새 컨테이너 시작
echo "🚀 Starting new containers..."
docker-compose -f docker-compose.prod.yml up -d

# 헬스체크
echo "🏥 Health check..."
sleep 10
curl -f http://localhost:8000/ || {
    echo "❌ Health check failed!"
    exit 1
}

echo "✅ Deployment completed successfully!"
echo "🌐 Application is running on http://localhost:8000" 
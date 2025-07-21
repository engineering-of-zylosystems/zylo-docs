#!/bin/bash

set -e

S3_PATH="s3://zylo-docs-lib-fe/docs/"
DEST_DIR="app/static"

# 1. AWS CLI 확인
if ! command -v aws &> /dev/null; then
  echo "❌ aws CLI가 설치되어 있지 않습니다. 먼저 설치해주세요."
  exit 1
fi

# 2. S3 버킷 접근 확인
echo "🔍 S3 버킷 접근 가능한지 확인 중..."
if ! aws s3 ls "$S3_PATH" > /dev/null; then
  echo "❌ S3 경로 접근 실패: $S3_PATH"
  echo "🔒 권한 또는 경로가 잘못되었을 수 있습니다."
  exit 1
fi

# 3. 디렉토리 정리
echo "🧹 Cleaning $DEST_DIR directory..."
mkdir -p "$DEST_DIR"
rm -rf "${DEST_DIR:?}"/*

# 4. 파일 복사
echo "📥 Downloading files from $S3_PATH"
aws s3 cp "$S3_PATH" "$DEST_DIR/" --recursive

echo "✅ Done! Files downloaded to $DEST_DIR"

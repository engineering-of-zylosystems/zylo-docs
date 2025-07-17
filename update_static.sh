#!/bin/bash

set -e

echo "🧹 Cleaning app/static directory..."
rm -rf app/static/*

echo "📥 Downloading files from s3://zylo-frontend/docs/..."
aws s3 cp s3://zylo-frontend/docs/ app/static/ --recursive

echo "✅ Done! Files downloaded to app/static"

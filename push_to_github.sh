#!/bin/bash
# Push analysis report to GitHub
# Usage: ./push_to_github.sh <github_username> <repo_name>

# Get token from environment or prompt
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN environment variable not set"
    echo "Please set it with: export GITHUB_TOKEN=your_token_here"
    exit 1
fi

USERNAME="${1:-lawrencezcl}"
REPO="${2:-quantitative-trading-analysis}"

echo "配置Git远程仓库..."
git remote add origin https://${GITHUB_TOKEN}@github.com/${USERNAME}/${REPO}.git 2>/dev/null || git remote set-url origin https://${GITHUB_TOKEN}@github.com/${USERNAME}/${REPO}.git

echo "推送到GitHub..."
git push -u origin master

echo "✅ 推送完成!"
echo "访问地址: https://github.com/${USERNAME}/${REPO}"

#!/bin/bash
echo "🚀 학습 시작"
python3 scripts/train.py
echo "📊 평가 시작"
python3 scripts/evaluate.py

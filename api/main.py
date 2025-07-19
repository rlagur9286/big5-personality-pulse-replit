import sys
import os

# 상위 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Flask 앱 import
from app import app

# Vercel은 이 파일에서 'app' 객체를 자동으로 찾습니다

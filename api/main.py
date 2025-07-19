import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel에서 직접 app을 사용할 수 있도록 내보내기
def handler(request):
    return app(request.environ, lambda status, headers: None)

# WSGI를 위한 app 객체 (Vercel이 자동으로 감지)
application = app

# 로컬 테스트용
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

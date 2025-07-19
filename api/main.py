import sys
import os

# 상위 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Flask 앱 import
    from app import app
    
    # 기본 테스트를 위한 간단한 라우트 추가
    @app.route('/debug')
    def debug_info():
        return {
            'status': 'original app loaded successfully',
            'template_folder': app.template_folder,
            'static_folder': app.static_folder
        }
    
    # 홈페이지를 간단한 텍스트로 오버라이드 (템플릿 문제 우회)
    @app.route('/')
    def simple_home():
        return '''
        <h1>Big5 성격 테스트</h1>
        <p>임시 홈페이지 - 템플릿 렌더링을 우회한 버전입니다.</p>
        <p><a href="/debug">디버그 정보 확인</a></p>
        <p>원래 앱이 성공적으로 로드되었습니다!</p>
        '''
        
except Exception as e:
    # import 에러가 발생하면 간단한 Flask 앱으로 대체
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error_info():
        return f'Import Error: {str(e)}'
    
    @app.route('/debug')
    def debug_error():
        return {'error': str(e), 'type': str(type(e))}

# Vercel은 이 파일에서 'app' 객체를 자동으로 찾습니다

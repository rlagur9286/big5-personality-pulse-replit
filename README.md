# Big5 성격 테스트 웹 애플리케이션

이중언어(한국어/영어) Big5 성격 테스트를 제공하는 Flask 웹 애플리케이션입니다.

## 🌟 주요 기능

- **50개 질문 Big5 테스트**: 개방성, 성실성, 외향성, 우호성, 신경성 측정
- **애니메이션 캐릭터 매칭**: 루피, 사이타마, 나루토, 짱구, 도라에몽 등과의 성격 매칭
- **결과 공유**: 고유 토큰으로 결과를 다른 사람과 공유 가능
- **이중 언어 지원**: 한국어/영어 완전 지원
- **모던 UI**: Bootstrap 5 + 커스텀 CSS로 반응형 디자인
- **실시간 차트**: Chart.js로 성격 분석 시각화

## 🚀 배포하기

### Railway 무료 배포

1. **GitHub 업로드**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-github-repo-url
   git push -u origin main
   ```

2. **Railway 계정 생성**: https://railway.app

3. **배포하기**
   - "Deploy from GitHub repo" 선택
   - 레포지토리 선택
   - 자동으로 배포 시작

4. **PostgreSQL 추가**
   - "Add Service" → "PostgreSQL" 선택
   - `DATABASE_URL` 자동 생성됨

5. **환경 변수 설정**
   ```
   SESSION_SECRET=your-secret-key-2025
   ```

### 로컬 실행

```bash
python main.py
```

## 📁 프로젝트 구조

```
├── app.py              # 메인 Flask 애플리케이션
├── main.py             # 앱 실행 진입점
├── models.py           # 데이터베이스 모델
├── templates/          # HTML 템플릿
├── static/            # CSS, JS, 이미지
├── attached_assets/   # 캐릭터 이미지
├── Procfile           # Railway 배포 설정
├── runtime.txt        # Python 버전
└── railway.json       # Railway 설정
```

## 🎨 기술 스택

- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Frontend**: Bootstrap 5, Chart.js, Vanilla JavaScript
- **Deployment**: Railway, Gunicorn
- **Database**: PostgreSQL (Production), SQLite (Development)

## 📊 Big5 성격 요인

1. **개방성 (Openness)**: 창의성, 호기심, 예술적 감각
2. **성실성 (Conscientiousness)**: 책임감, 계획성, 자제력
3. **외향성 (Extraversion)**: 사교성, 활동성, 긍정성
4. **우호성 (Agreeableness)**: 협력성, 신뢰, 공감능력
5. **신경성 (Neuroticism)**: 정서적 안정성, 스트레스 대처

## 🎯 애니메이션 캐릭터

- 루피 (원피스) - 자유롭고 모험적
- 사이타마 (원펀맨) - 무표정하지만 강한 정의감
- 나루토 - 밝고 끈기 있는 노력가
- 짱구 - 자유분방하고 창의적
- 도라에몽 - 친절하고 도움이 되는 친구
- 죠타로 - 냉정하고 강인한 의지
- 에드워드 - 천재적이고 열정적
- 코난 - 논리적이고 분석적
- 에렌 - 자유를 갈망하는 전사
- 탄지로 - 따뜻하고 결단력 있는 검사

## 📱 반응형 디자인

모든 기기에서 최적화된 사용자 경험을 제공합니다.

---

Made with ❤️ in Korea
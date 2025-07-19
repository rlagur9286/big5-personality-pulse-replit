import os
import logging
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import json
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Get the directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Create the app with explicit template and static folder paths
app = Flask(__name__, 
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'))
app.secret_key = os.environ.get("SESSION_SECRET", "big5-test-secret-key-2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Big5 Questions - 10 questions per factor (50 total)
BIG5_QUESTIONS = {
    "ko": [
        # Openness (O) - Questions 1-10
        {"id": 1, "text": "나는 새로운 경험을 추구하는 것을 좋아한다", "factor": "O", "reverse": False},
        {"id": 2, "text": "나는 창의적이고 상상력이 풍부하다", "factor": "O", "reverse": False},
        {"id": 3, "text": "나는 예술과 미에 관심이 많다", "factor": "O", "reverse": False},
        {"id": 4, "text": "나는 철학적이고 추상적인 주제에 관심이 있다", "factor": "O", "reverse": False},
        {"id": 5, "text": "나는 전통적인 방식보다 새로운 방식을 선호한다", "factor": "O", "reverse": False},
        {"id": 6, "text": "나는 상상력이 부족하다", "factor": "O", "reverse": True},
        {"id": 7, "text": "나는 예술에 별로 관심이 없다", "factor": "O", "reverse": True},
        {"id": 8, "text": "나는 일상적이고 평범한 것을 선호한다", "factor": "O", "reverse": True},
        {"id": 9, "text": "나는 새로운 아이디어에 개방적이다", "factor": "O", "reverse": False},
        {"id": 10, "text": "나는 변화를 좋아한다", "factor": "O", "reverse": False},
        
        # Conscientiousness (C) - Questions 11-20
        {"id": 11, "text": "나는 계획을 세우고 체계적으로 일을 처리한다", "factor": "C", "reverse": False},
        {"id": 12, "text": "나는 책임감이 강하고 신뢰할 만하다", "factor": "C", "reverse": False},
        {"id": 13, "text": "나는 목표를 달성하기 위해 끈기있게 노력한다", "factor": "C", "reverse": False},
        {"id": 14, "text": "나는 정리정돈을 잘한다", "factor": "C", "reverse": False},
        {"id": 15, "text": "나는 시간을 잘 지킨다", "factor": "C", "reverse": False},
        {"id": 16, "text": "나는 게으르고 미루기를 잘한다", "factor": "C", "reverse": True},
        {"id": 17, "text": "나는 정리정돈이 안 되어 있다", "factor": "C", "reverse": True},
        {"id": 18, "text": "나는 약속을 잘 어긴다", "factor": "C", "reverse": True},
        {"id": 19, "text": "나는 세심하고 꼼꼼하다", "factor": "C", "reverse": False},
        {"id": 20, "text": "나는 자제력이 강하다", "factor": "C", "reverse": False},
        
        # Extraversion (E) - Questions 21-30
        {"id": 21, "text": "나는 활발하고 에너지가 넘친다", "factor": "E", "reverse": False},
        {"id": 22, "text": "나는 사람들과 어울리는 것을 좋아한다", "factor": "E", "reverse": False},
        {"id": 23, "text": "나는 파티나 모임에서 활발히 참여한다", "factor": "E", "reverse": False},
        {"id": 24, "text": "나는 낙관적이고 긍정적이다", "factor": "E", "reverse": False},
        {"id": 25, "text": "나는 새로운 사람들과 만나는 것을 좋아한다", "factor": "E", "reverse": False},
        {"id": 26, "text": "나는 조용하고 내성적이다", "factor": "E", "reverse": True},
        {"id": 27, "text": "나는 혼자 있는 시간을 선호한다", "factor": "E", "reverse": True},
        {"id": 28, "text": "나는 말이 적은 편이다", "factor": "E", "reverse": True},
        {"id": 29, "text": "나는 자신감이 있고 당당하다", "factor": "E", "reverse": False},
        {"id": 30, "text": "나는 자극적이고 흥미진진한 활동을 좋아한다", "factor": "E", "reverse": False},
        
        # Agreeableness (A) - Questions 31-40
        {"id": 31, "text": "나는 다른 사람들을 신뢰한다", "factor": "A", "reverse": False},
        {"id": 32, "text": "나는 다른 사람들을 도와주는 것을 좋아한다", "factor": "A", "reverse": False},
        {"id": 33, "text": "나는 관대하고 너그럽다", "factor": "A", "reverse": False},
        {"id": 34, "text": "나는 협력적이고 타협을 잘한다", "factor": "A", "reverse": False},
        {"id": 35, "text": "나는 다른 사람의 감정을 잘 이해한다", "factor": "A", "reverse": False},
        {"id": 36, "text": "나는 다른 사람들에게 비판적이다", "factor": "A", "reverse": True},
        {"id": 37, "text": "나는 이기적이고 자기중심적이다", "factor": "A", "reverse": True},
        {"id": 38, "text": "나는 다른 사람들과 쉽게 갈등을 일으킨다", "factor": "A", "reverse": True},
        {"id": 39, "text": "나는 겸손하고 잘난 체하지 않는다", "factor": "A", "reverse": False},
        {"id": 40, "text": "나는 다른 사람들의 의견을 존중한다", "factor": "A", "reverse": False},
        
        # Neuroticism (N) - Questions 41-50
        {"id": 41, "text": "나는 자주 걱정하고 불안해한다", "factor": "N", "reverse": False},
        {"id": 42, "text": "나는 스트레스를 받으면 쉽게 화를 낸다", "factor": "N", "reverse": False},
        {"id": 43, "text": "나는 감정 기복이 심하다", "factor": "N", "reverse": False},
        {"id": 44, "text": "나는 우울하거나 슬픈 기분이 자주 든다", "factor": "N", "reverse": False},
        {"id": 45, "text": "나는 자신감이 부족하다", "factor": "N", "reverse": False},
        {"id": 46, "text": "나는 차분하고 감정적으로 안정되어 있다", "factor": "N", "reverse": True},
        {"id": 47, "text": "나는 스트레스 상황에서도 침착함을 유지한다", "factor": "N", "reverse": True},
        {"id": 48, "text": "나는 긴장을 잘 하지 않는다", "factor": "N", "reverse": True},
        {"id": 49, "text": "나는 작은 일에도 쉽게 짜증을 낸다", "factor": "N", "reverse": False},
        {"id": 50, "text": "나는 좌절을 잘 견딘다", "factor": "N", "reverse": True}
    ],
    "en": [
        # Openness (O) - Questions 1-10
        {"id": 1, "text": "I enjoy seeking new experiences", "factor": "O", "reverse": False},
        {"id": 2, "text": "I am creative and imaginative", "factor": "O", "reverse": False},
        {"id": 3, "text": "I have a strong interest in art and beauty", "factor": "O", "reverse": False},
        {"id": 4, "text": "I am interested in philosophical and abstract topics", "factor": "O", "reverse": False},
        {"id": 5, "text": "I prefer new ways over traditional methods", "factor": "O", "reverse": False},
        {"id": 6, "text": "I lack imagination", "factor": "O", "reverse": True},
        {"id": 7, "text": "I have little interest in art", "factor": "O", "reverse": True},
        {"id": 8, "text": "I prefer routine and ordinary things", "factor": "O", "reverse": True},
        {"id": 9, "text": "I am open to new ideas", "factor": "O", "reverse": False},
        {"id": 10, "text": "I enjoy change", "factor": "O", "reverse": False},
        
        # Conscientiousness (C) - Questions 11-20
        {"id": 11, "text": "I make plans and handle things systematically", "factor": "C", "reverse": False},
        {"id": 12, "text": "I am responsible and reliable", "factor": "C", "reverse": False},
        {"id": 13, "text": "I work persistently to achieve my goals", "factor": "C", "reverse": False},
        {"id": 14, "text": "I am good at organizing and tidying up", "factor": "C", "reverse": False},
        {"id": 15, "text": "I am punctual", "factor": "C", "reverse": False},
        {"id": 16, "text": "I am lazy and tend to procrastinate", "factor": "C", "reverse": True},
        {"id": 17, "text": "I am disorganized", "factor": "C", "reverse": True},
        {"id": 18, "text": "I often break promises", "factor": "C", "reverse": True},
        {"id": 19, "text": "I am careful and meticulous", "factor": "C", "reverse": False},
        {"id": 20, "text": "I have strong self-control", "factor": "C", "reverse": False},
        
        # Extraversion (E) - Questions 21-30
        {"id": 21, "text": "I am energetic and full of energy", "factor": "E", "reverse": False},
        {"id": 22, "text": "I enjoy being around people", "factor": "E", "reverse": False},
        {"id": 23, "text": "I actively participate in parties and gatherings", "factor": "E", "reverse": False},
        {"id": 24, "text": "I am optimistic and positive", "factor": "E", "reverse": False},
        {"id": 25, "text": "I enjoy meeting new people", "factor": "E", "reverse": False},
        {"id": 26, "text": "I am quiet and introverted", "factor": "E", "reverse": True},
        {"id": 27, "text": "I prefer spending time alone", "factor": "E", "reverse": True},
        {"id": 28, "text": "I don't talk much", "factor": "E", "reverse": True},
        {"id": 29, "text": "I am confident and assertive", "factor": "E", "reverse": False},
        {"id": 30, "text": "I enjoy exciting and stimulating activities", "factor": "E", "reverse": False},
        
        # Agreeableness (A) - Questions 31-40
        {"id": 31, "text": "I trust other people", "factor": "A", "reverse": False},
        {"id": 32, "text": "I enjoy helping others", "factor": "A", "reverse": False},
        {"id": 33, "text": "I am generous and forgiving", "factor": "A", "reverse": False},
        {"id": 34, "text": "I am cooperative and good at compromising", "factor": "A", "reverse": False},
        {"id": 35, "text": "I understand others' emotions well", "factor": "A", "reverse": False},
        {"id": 36, "text": "I am critical of others", "factor": "A", "reverse": True},
        {"id": 37, "text": "I am selfish and self-centered", "factor": "A", "reverse": True},
        {"id": 38, "text": "I easily get into conflicts with others", "factor": "A", "reverse": True},
        {"id": 39, "text": "I am humble and don't show off", "factor": "A", "reverse": False},
        {"id": 40, "text": "I respect others' opinions", "factor": "A", "reverse": False},
        
        # Neuroticism (N) - Questions 41-50
        {"id": 41, "text": "I often worry and feel anxious", "factor": "N", "reverse": False},
        {"id": 42, "text": "I easily get angry when stressed", "factor": "N", "reverse": False},
        {"id": 43, "text": "I have severe mood swings", "factor": "N", "reverse": False},
        {"id": 44, "text": "I often feel depressed or sad", "factor": "N", "reverse": False},
        {"id": 45, "text": "I lack self-confidence", "factor": "N", "reverse": False},
        {"id": 46, "text": "I am calm and emotionally stable", "factor": "N", "reverse": True},
        {"id": 47, "text": "I remain calm even in stressful situations", "factor": "N", "reverse": True},
        {"id": 48, "text": "I don't get nervous easily", "factor": "N", "reverse": True},
        {"id": 49, "text": "I easily get irritated by small things", "factor": "N", "reverse": False},
        {"id": 50, "text": "I handle frustration well", "factor": "N", "reverse": True}
    ]
}

# Factor descriptions
FACTOR_DESCRIPTIONS = {
    "ko": {
        "O": {
            "name": "개방성 (Openness)",
            "emoji": "🎨",
            "description": "새로운 경험과 아이디어에 대한 개방성",
            "high": "창의적이고 상상력이 풍부하며, 새로운 경험을 추구합니다. 예술과 문화에 관심이 많고, 변화를 즐깁니다.",
            "low": "실용적이고 전통적인 가치를 선호합니다. 안정되고 예측 가능한 환경을 좋아합니다.",
            "careers_high": ["예술가", "작가", "디자이너", "연구원", "마케터"],
            "careers_low": ["회계사", "엔지니어", "관리자", "공무원", "기술자"]
        },
        "C": {
            "name": "성실성 (Conscientiousness)",
            "emoji": "📋",
            "description": "목표 지향적이고 조직적인 성향",
            "high": "계획적이고 체계적이며, 책임감이 강합니다. 목표 달성을 위해 끈기있게 노력합니다.",
            "low": "자유분방하고 즉흥적입니다. 유연하고 적응력이 좋지만, 때로는 계획성이 부족할 수 있습니다.",
            "careers_high": ["의사", "변호사", "회계사", "프로젝트 매니저", "연구원"],
            "careers_low": ["예술가", "연예인", "프리랜서", "기자", "창업가"]
        },
        "E": {
            "name": "외향성 (Extraversion)",
            "emoji": "🎉",
            "description": "사회적 활동과 자극 추구 성향",
            "high": "활발하고 사교적이며, 사람들과의 상호작용에서 에너지를 얻습니다. 리더십을 발휘하기를 좋아합니다.",
            "low": "조용하고 신중하며, 혼자만의 시간을 즐깁니다. 깊이 있는 관계를 선호합니다.",
            "careers_high": ["영업사원", "교사", "정치인", "연예인", "마케터"],
            "careers_low": ["연구원", "작가", "프로그래머", "회계사", "도서관 사서"]
        },
        "A": {
            "name": "우호성 (Agreeableness)",
            "emoji": "🤝",
            "description": "타인에 대한 배려와 협력 성향",
            "high": "친절하고 협력적이며, 다른 사람들을 돕는 것을 좋아합니다. 갈등을 피하고 조화를 추구합니다.",
            "low": "경쟁적이고 독립적입니다. 자신의 의견을 당당히 표현하며, 비판적 사고를 잘합니다.",
            "careers_high": ["간호사", "교사", "상담사", "사회복지사", "의사"],
            "careers_low": ["변호사", "경영자", "판사", "비평가", "과학자"]
        },
        "N": {
            "name": "신경성 (Neuroticism)",
            "emoji": "😰",
            "description": "정서적 안정성과 스트레스 대처 능력",
            "high": "감정 기복이 있고 스트레스에 민감합니다. 걱정이 많지만, 감수성이 풍부하고 세심합니다.",
            "low": "정서적으로 안정되고 차분합니다. 스트레스 상황에서도 침착함을 유지합니다.",
            "careers_high": ["예술가", "작가", "상담사", "심리학자", "치료사"],
            "careers_low": ["의사", "파일럿", "경찰관", "소방관", "관리자"]
        }
    },
    "en": {
        "O": {
            "name": "Openness to Experience",
            "emoji": "🎨",
            "description": "Openness to new experiences and ideas",
            "high": "You are creative and imaginative, seeking new experiences. You have a strong interest in art and culture, and enjoy change.",
            "low": "You prefer practical and traditional values. You like stable and predictable environments.",
            "careers_high": ["Artist", "Writer", "Designer", "Researcher", "Marketer"],
            "careers_low": ["Accountant", "Engineer", "Manager", "Civil Servant", "Technician"]
        },
        "C": {
            "name": "Conscientiousness",
            "emoji": "📋",
            "description": "Goal-oriented and organized tendencies",
            "high": "You are systematic and methodical, with a strong sense of responsibility. You work persistently to achieve your goals.",
            "low": "You are free-spirited and spontaneous. You are flexible and adaptable, but may sometimes lack organization.",
            "careers_high": ["Doctor", "Lawyer", "Accountant", "Project Manager", "Researcher"],
            "careers_low": ["Artist", "Entertainer", "Freelancer", "Journalist", "Entrepreneur"]
        },
        "E": {
            "name": "Extraversion",
            "emoji": "🎉",
            "description": "Social activity and stimulation-seeking tendencies",
            "high": "You are energetic and sociable, gaining energy from interactions with others. You enjoy exercising leadership.",
            "low": "You are quiet and thoughtful, enjoying solitary time. You prefer deep, meaningful relationships.",
            "careers_high": ["Salesperson", "Teacher", "Politician", "Entertainer", "Marketer"],
            "careers_low": ["Researcher", "Writer", "Programmer", "Accountant", "Librarian"]
        },
        "A": {
            "name": "Agreeableness",
            "emoji": "🤝",
            "description": "Consideration for others and cooperative tendencies",
            "high": "You are kind and cooperative, enjoying helping others. You avoid conflict and seek harmony.",
            "low": "You are competitive and independent. You express your opinions confidently and think critically.",
            "careers_high": ["Nurse", "Teacher", "Counselor", "Social Worker", "Doctor"],
            "careers_low": ["Lawyer", "Executive", "Judge", "Critic", "Scientist"]
        },
        "N": {
            "name": "Neuroticism",
            "emoji": "😰",
            "description": "Emotional stability and stress coping ability",
            "high": "You experience mood fluctuations and are sensitive to stress. You worry often but are highly sensitive and attentive.",
            "low": "You are emotionally stable and calm. You maintain composure even in stressful situations.",
            "careers_high": ["Artist", "Writer", "Counselor", "Psychologist", "Therapist"],
            "careers_low": ["Doctor", "Pilot", "Police Officer", "Firefighter", "Manager"]
        }
    }
}

# 만화 캐릭터 매칭 데이터
ANIME_CHARACTERS = {
    "ko": {
        # 각 캐릭터는 Big5 점수 범위와 매칭됩니다
        "루피": {
            "anime": "원피스",
            "personality": "자유롭고 모험을 좋아하는 낙천적인 리더",
            "description": "무엇이든 가능하다고 믿는 긍정적인 성격으로, 친구들을 위해서라면 어떤 위험도 감수하는 용감한 마음을 가지고 있어요.",
            "match_conditions": {"E": (70, 100), "A": (60, 100), "O": (70, 100), "N": (0, 40)},
            "traits": ["모험심 가득", "리더십", "낙천적", "충성심"],
            "image_emoji": "🏴‍☠️👒",
            "image_path": "/static/images/characters/luffy.jpg"
        },
        "사이타마": {
            "anime": "원펀맨", 
            "personality": "무표정하지만 강한 정의감을 가진 영웅",
            "description": "겉으로는 무관심해 보이지만 내면에는 강한 정의감과 책임감을 가지고 있어요. 목표를 위해 꾸준히 노력하는 성실한 면도 있죠.",
            "match_conditions": {"E": (0, 50), "C": (60, 100), "A": (40, 80), "N": (0, 30)},
            "traits": ["강한 의지", "정의감", "꾸준함", "겸손"],
            "image_emoji": "👨‍🦲💪",
            "image_path": "/static/images/characters/saitama.jpg"
        },
        "나루토": {
            "anime": "나루토",
            "personality": "밝고 끈기있는 노력가",
            "description": "절대 포기하지 않는 끈기와 친구들을 소중히 여기는 마음을 가지고 있어요. 때로는 실수하지만 항상 열정적으로 도전합니다.",
            "match_conditions": {"E": (60, 100), "C": (50, 90), "A": (70, 100), "O": (60, 90)},
            "traits": ["끈기", "열정", "우정", "성장형"],
            "image_emoji": "🥷🌀",
            "image_path": "/static/images/characters/naruto.jpg"
        },
        "짱구": {
            "anime": "짱구는 못말려",
            "personality": "자유분방하고 창의적인 개구쟁이",
            "description": "상상력이 풍부하고 자유로운 영혼이에요. 예측불가능하지만 가족과 친구들에게는 따뜻한 마음을 보여줍니다.",
            "match_conditions": {"O": (70, 100), "C": (0, 40), "E": (60, 100), "N": (20, 60)},
            "traits": ["창의성", "자유로움", "유머", "순수함"],
            "image_emoji": "🧒🎨",
            "image_path": "/static/images/characters/shinchanu.jpg"
        },
        "도라에몽": {
            "anime": "도라에몽",
            "personality": "친절하고 도움을 주려는 따뜻한 친구",
            "description": "항상 친구를 도우려 하는 친절한 마음과 문제 해결 능력을 가지고 있어요. 때로는 걱정이 많지만 결국 좋은 결과를 만들어냅니다.",
            "match_conditions": {"A": (70, 100), "C": (60, 90), "E": (40, 80), "O": (80, 100)},
            "traits": ["친절함", "창의성", "문제해결", "보살핌"],
            "image_emoji": "🤖💙",
            "image_path": "/static/images/characters/doraemon.jpg"
        },
        "죠타로": {
            "anime": "죠죠의 기묘한 모험",
            "personality": "냉정하고 강인한 의지의 소유자",
            "description": "겉으로는 차갑고 무뚝뚝해 보이지만 내면에는 강한 정의감과 동료애를 가지고 있어요. 어떤 어려움에도 굴복하지 않는 강철 같은 정신력을 보여줍니다.",
            "match_conditions": {"C": (70, 100), "E": (20, 60), "A": (40, 70), "N": (0, 40)},
            "traits": ["강인함", "냉정함", "정의감", "리더십"],
            "image_emoji": "⭐🧥",
            "image_path": "/static/images/characters/jotaro.jpg"
        },
        "에드워드": {
            "anime": "강철의 연금술사",
            "personality": "천재적이고 열정적인 연금술사",
            "description": "뛰어난 지능과 끝없는 호기심을 가진 완벽주의자예요. 목표를 위해서는 어떤 어려움도 극복하려는 강한 의지를 보여줍니다.",
            "match_conditions": {"O": (80, 100), "C": (70, 100), "E": (60, 90), "A": (50, 80)},
            "traits": ["천재성", "호기심", "의지력", "완벽주의"],
            "image_emoji": "⚗️👦",
            "image_path": "/static/images/characters/edward.jpg"
        },
        "코난": {
            "anime": "명탐정 코난",
            "personality": "논리적이고 분석적인 탐정",
            "description": "뛰어난 관찰력과 논리적 사고를 가진 완벽주의자예요. 정의감이 강하고 진실을 밝히는 것을 중요하게 생각합니다.",
            "match_conditions": {"C": (80, 100), "O": (70, 100), "E": (40, 70), "A": (60, 90)},
            "traits": ["논리적", "관찰력", "정의감", "완벽주의"],
            "image_emoji": "🔍👦",
            "image_path": "/static/images/characters/conan.jpg"
        },
        "에렌": {
            "anime": "진격의 거인",
            "personality": "자유를 갈망하는 강한 의지의 전사",
            "description": "자유에 대한 강한 갈망과 불굴의 의지를 가진 복잡한 성격이에요. 때로는 충동적이지만 목표를 위해서는 어떤 희생도 감수하는 결단력을 보여줍니다.",
            "match_conditions": {"O": (70, 100), "C": (50, 90), "A": (20, 60), "N": (60, 100)},
            "traits": ["강한 의지", "자유추구", "결단력", "복잡함"],
            "image_emoji": "⚔️🗡️",
            "image_path": "/static/images/characters/eren.jpg"
        },
        "센고ku": {
            "anime": "귀멸의 칼날",
            "personality": "따뜻하고 결단력 있는 검사",
            "description": "강한 의지와 따뜻한 마음을 동시에 가진 균형잡힌 성격이에요. 어떤 어려움도 포기하지 않고 타인에 대한 깊은 공감능력을 보여줍니다.",
            "match_conditions": {"C": (70, 100), "A": (80, 100), "E": (50, 80), "O": (60, 90)},
            "traits": ["의지력", "공감능력", "결단력", "따뜻함"],
            "image_emoji": "⚔️🔥",
            "image_path": "/static/images/characters/tanjiro.jpg"
        }
    },
    "en": {
        "Luffy": {
            "anime": "One Piece",
            "personality": "Free-spirited adventurous optimistic leader",
            "description": "Has a positive personality that believes anything is possible, with a brave heart willing to take any risk for friends.",
            "match_conditions": {"E": (70, 100), "A": (60, 100), "O": (70, 100), "N": (0, 40)},
            "traits": ["Adventurous", "Leadership", "Optimistic", "Loyal"],
            "image_emoji": "🏴‍☠️",
            "image_path": "/static/images/characters/luffy.jpg"
        },
        "Saitama": {
            "anime": "One Punch Man",
            "personality": "Expressionless but strong sense of justice hero",
            "description": "Appears indifferent on the surface but has strong justice and responsibility inside. Also has a diligent side that works steadily toward goals.",
            "match_conditions": {"E": (0, 50), "C": (60, 100), "A": (40, 80), "N": (0, 30)},
            "traits": ["Strong will", "Justice", "Persistence", "Humble"],
            "image_emoji": "👊",
            "image_path": "/static/images/characters/saitama.jpg"
        },
        "Naruto": {
            "anime": "Naruto",
            "personality": "Bright and persistent hard worker",
            "description": "Has persistence that never gives up and a heart that cherishes friends. Sometimes makes mistakes but always challenges with passion.",
            "match_conditions": {"E": (60, 100), "C": (50, 90), "A": (70, 100), "O": (60, 90)},
            "traits": ["Persistence", "Passion", "Friendship", "Growth"],
            "image_emoji": "🍜",
            "image_path": "/static/images/characters/naruto.jpg"
        },
        "Shin-chan": {
            "anime": "Crayon Shin-chan",
            "personality": "Free-spirited and creative troublemaker",
            "description": "Rich imagination and free spirit. Unpredictable but shows warm heart to family and friends.",
            "match_conditions": {"O": (70, 100), "C": (0, 40), "E": (60, 100), "N": (20, 60)},
            "traits": ["Creativity", "Freedom", "Humor", "Innocence"],
            "image_emoji": "🎭",
            "image_path": "/static/images/characters/shinchanu.jpg"
        },
        "Doraemon": {
            "anime": "Doraemon",
            "personality": "Kind and helpful warm friend",
            "description": "Has a kind heart that always tries to help friends and problem-solving abilities. Sometimes worries a lot but eventually creates good results.",
            "match_conditions": {"A": (70, 100), "C": (60, 90), "E": (40, 80), "O": (80, 100)},
            "traits": ["Kindness", "Creativity", "Problem-solving", "Caring"],
            "image_emoji": "🤖",
            "image_path": "/static/images/characters/doraemon.jpg"
        },
        "Jotaro": {
            "anime": "JoJo's Bizarre Adventure",
            "personality": "Cool and strong-willed individual",
            "description": "Appears cold and blunt on the surface but has strong sense of justice and camaraderie inside. Shows steel-like mental strength that never gives up to any difficulty.",
            "match_conditions": {"C": (70, 100), "E": (20, 60), "A": (40, 70), "N": (0, 40)},
            "traits": ["Strong", "Cool", "Justice", "Leadership"],
            "image_emoji": "⭐🧥",
            "image_path": "/static/images/characters/jotaro.jpg"
        },
        "Edward": {
            "anime": "Fullmetal Alchemist",
            "personality": "Genius and passionate alchemist",
            "description": "Perfectionist with outstanding intelligence and endless curiosity. Shows strong will to overcome any difficulty for goals.",
            "match_conditions": {"O": (80, 100), "C": (70, 100), "E": (60, 90), "A": (50, 80)},
            "traits": ["Genius", "Curiosity", "Willpower", "Perfectionist"],
            "image_emoji": "⚗️👦",
            "image_path": "/static/images/characters/edward.jpg"
        },
        "Conan": {
            "anime": "Detective Conan",
            "personality": "Logical and analytical detective",
            "description": "Perfectionist with excellent observation and logical thinking. Has strong sense of justice and values revealing the truth.",
            "match_conditions": {"C": (80, 100), "O": (70, 100), "E": (40, 70), "A": (60, 90)},
            "traits": ["Logical", "Observant", "Justice", "Perfectionist"],
            "image_emoji": "🔍",
            "image_path": "/static/images/characters/conan.jpg"
        },
        "Eren": {
            "anime": "Attack on Titan",
            "personality": "Freedom-seeking strong-willed warrior",
            "description": "Complex personality with strong desire for freedom and unwavering will. Sometimes impulsive but shows determination to make any sacrifice for goals.",
            "match_conditions": {"O": (70, 100), "C": (50, 90), "A": (20, 60), "N": (60, 100)},
            "traits": ["Strong will", "Freedom", "Determination", "Complex"],
            "image_emoji": "⚔️🗡️",
            "image_path": "/static/images/characters/eren.jpg"
        },
        "Tanjiro": {
            "anime": "Demon Slayer",
            "personality": "Warm and determined swordsman",
            "description": "Balanced personality with strong will and warm heart at the same time. Never gives up on any difficulty and shows deep empathy for others.",
            "match_conditions": {"C": (70, 100), "A": (80, 100), "E": (50, 80), "O": (60, 90)},
            "traits": ["Willpower", "Empathy", "Determination", "Warmth"],
            "image_emoji": "⚔️🔥",
            "image_path": "/static/images/characters/tanjiro.jpg"
        }
    }
}

def find_anime_character(scores, lang="ko"):
    """사용자의 Big5 점수를 바탕으로 가장 적합한 애니메이션 캐릭터를 찾습니다."""
    characters = ANIME_CHARACTERS[lang]
    best_match = None
    best_score = 0
    
    for char_name, char_data in characters.items():
        match_score = 0
        total_conditions = 0
        
        for factor, (min_val, max_val) in char_data["match_conditions"].items():
            total_conditions += 1
            user_score = scores.get(factor, 50)
            
            if min_val <= user_score <= max_val:
                # 완전 매치: 3점
                match_score += 3
            elif abs(user_score - min_val) <= 15 or abs(user_score - max_val) <= 15:
                # 근접 매치: 2점
                match_score += 2
            elif abs(user_score - (min_val + max_val) / 2) <= 25:
                # 부분 매치: 1점
                match_score += 1
        
        # 매치 점수를 백분율로 변환
        final_score = (match_score / (total_conditions * 3)) * 100
        
        if final_score > best_score:
            best_score = final_score
            best_match = {
                "name": char_name,
                "data": char_data,
                "match_percentage": round(final_score, 1)
            }
    
    return best_match

# Database-free version - using sessions only

@app.route('/')
def index():
    lang = request.args.get('lang', 'ko')
    if lang not in ['ko', 'en']:
        lang = 'ko'
    session['language'] = lang
    return render_template('index.html', lang=lang)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['ko', 'en']:
        session['language'] = lang
    return redirect(url_for('index', lang=lang))

@app.route('/start_test')
def start_test():
    # Reset session data
    session['answers'] = {}
    session['current_question'] = 1
    session['test_started'] = datetime.now().isoformat()
    lang = session.get('language', 'ko')
    return redirect(url_for('test', lang=lang))

@app.route('/test', methods=['GET', 'POST'])
@app.route('/test/<int:question_num>', methods=['GET', 'POST'])
def test(question_num=None):
    if 'test_started' not in session:
        return redirect(url_for('index'))
    
    lang = session.get('language', 'ko')
    questions = BIG5_QUESTIONS[lang]
    
    # Handle question navigation
    if question_num is not None:
        if 1 <= question_num <= len(questions):
            session['current_question'] = question_num
        else:
            return redirect(url_for('test'))
    
    current_q = session.get('current_question', 1)
    
    if request.method == 'POST':
        action = request.form.get('action', 'next')
        
        # Save answer if provided
        if 'answer' in request.form:
            answer = int(request.form.get('answer', 3))
            session['answers'][str(current_q)] = answer
            session.modified = True
        
        # Handle navigation
        if action == 'prev' and current_q > 1:
            session['current_question'] = current_q - 1
            return redirect(url_for('test'))
        elif action == 'next':
            if current_q < len(questions):
                session['current_question'] = current_q + 1
                return redirect(url_for('test'))
            else:
                # Test completed, calculate results
                return redirect(url_for('calculate_results'))
        elif action == 'finish':
            # Force finish test (go to results)
            return redirect(url_for('calculate_results'))
    
    # Get current question
    if current_q <= len(questions):
        question = questions[current_q - 1]
        # Calculate progress based on answered questions
        answered_count = len(session.get('answers', {}))
        progress = answered_count / len(questions) * 100
        
        # Get existing answer for this question
        existing_answer = session.get('answers', {}).get(str(current_q), None)
        
        return render_template('test.html', 
                             question=question, 
                             progress=progress,
                             current=current_q,
                             total=len(questions),
                             existing_answer=existing_answer,
                             answered_count=answered_count,
                             lang=lang)
    else:
        return redirect(url_for('calculate_results'))

@app.route('/calculate_results')
def calculate_results():
    lang = session.get('language', 'ko')
    questions = BIG5_QUESTIONS[lang]
    
    # Check if we have enough answers
    if 'answers' not in session or len(session['answers']) < len(questions):
        return redirect(url_for('index'))
    
    # Calculate scores for each factor
    scores = {'O': 0, 'C': 0, 'E': 0, 'A': 0, 'N': 0}
    
    for i, question in enumerate(questions):
        answer = session['answers'].get(str(i + 1), 3)
        factor = question['factor']
        
        # Reverse scoring for reverse-coded items
        if question['reverse']:
            score = 6 - answer  # 1->5, 2->4, 3->3, 4->2, 5->1
        else:
            score = answer
        
        scores[factor] += score
    
    # Convert to percentiles (0-100)
    # Each factor has 10 questions, score range is 10-50
    # Convert to 0-100 scale
    percentile_scores = {}
    for factor, score in scores.items():
        percentile = ((score - 10) / 40) * 100
        percentile_scores[factor] = max(0, min(100, percentile))
    
    # Find matching anime character
    anime_character = find_anime_character(percentile_scores, lang)
    
    # Store results in session (no database)
    session['results'] = percentile_scores
    session['anime_character'] = anime_character
    session['test_completed'] = datetime.now().isoformat()
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    if 'results' not in session:
        return redirect(url_for('index'))
    
    lang = session.get('language', 'ko')
    scores = session['results']
    factor_descriptions = FACTOR_DESCRIPTIONS[lang]
    anime_character = session.get('anime_character', None)
    
    # Define colors for each factor
    factor_colors = {
        'O': '#6366f1',  # Indigo for Openness
        'C': '#10b981',  # Emerald for Conscientiousness  
        'E': '#f59e0b',  # Amber for Extraversion
        'A': '#ef4444',  # Red for Agreeableness
        'N': '#8b5cf6'   # Violet for Neuroticism
    }
    
    # Generate personality insights
    insights = {}
    for factor, score in scores.items():
        factor_info = factor_descriptions[factor].copy()
        factor_info['score'] = score
        factor_info['level'] = 'high' if score >= 60 else 'low' if score <= 40 else 'medium'
        factor_info['color'] = factor_colors[factor]
        insights[factor] = factor_info
    
    # Current date for display
    current_date = datetime.now().strftime('%Y년 %m월 %d일' if lang == 'ko' else '%B %d, %Y')
    
    # No sharing feature in database-free version
    share_url = None
    
    return render_template('results.html', 
                         insights=insights, 
                         scores=scores,
                         anime_character=anime_character,
                         lang=lang,
                         current_date=current_date,
                         share_url=share_url)

# Error handlers for debugging
@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(f'Server Error: {error}')
    return f'Internal Server Error: {str(error)}', 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Not Found: {error}')
    return f'Not Found: {str(error)}', 404

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'ok', 'message': 'Flask app is running'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from app import db
from datetime import datetime
import uuid

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    openness = db.Column(db.Float, nullable=False)
    conscientiousness = db.Column(db.Float, nullable=False)
    extraversion = db.Column(db.Float, nullable=False)
    agreeableness = db.Column(db.Float, nullable=False)
    neuroticism = db.Column(db.Float, nullable=False)
    test_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    share_token = db.Column(db.String(36), unique=True, nullable=True)
    
    def __init__(self, **kwargs):
        super(TestResult, self).__init__(**kwargs)
        if not self.share_token:
            self.share_token = str(uuid.uuid4())
    
    def __repr__(self):
        return f'<TestResult {self.id}>'
    
    @property
    def personality_type(self):
        """Generate a simple personality type based on high/low scores"""
        factors = {
            'O': 'Creative' if self.openness >= 60 else 'Practical',
            'C': 'Organized' if self.conscientiousness >= 60 else 'Flexible',
            'E': 'Outgoing' if self.extraversion >= 60 else 'Reserved',
            'A': 'Cooperative' if self.agreeableness >= 60 else 'Competitive',
            'N': 'Sensitive' if self.neuroticism >= 60 else 'Resilient'
        }
        return factors

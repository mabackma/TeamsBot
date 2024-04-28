from extensions import db
from sqlalchemy.orm import relationship

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(45), nullable=False, unique=True)
    answerType = db.Column(db.String(45), nullable=False)
    satisfactionSurvey_id = db.Column(db.Integer, db.ForeignKey('satisfactionsurvey.id'), nullable=False)
    #satisfaction_survey = db.relationship('SatisfactionSurvey', backref=db.backref('questions', lazy=True))

    satisfaction_survey = relationship("SatisfactionSurvey", back_populates="questions")
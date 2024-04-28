from extensions import db
from sqlalchemy.orm import relationship

class SatisfactionSurvey(db.Model):
    __tablename__ = 'satisfactionsurvey'
    id = db.Column(db.Integer, primary_key=True)
    surveyDate = db.Column(db.Date, nullable=False, unique=True)

    questions = relationship("Question", back_populates="satisfaction_survey")
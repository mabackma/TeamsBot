from extensions import db

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numericResponse = db.Column(db.Integer, nullable=True)
    booleanResponse = db.Column(db.Boolean, nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    question = db.relationship('Question', backref=db.backref('answer', lazy=True))
    employee = db.relationship('Employee', backref=db.backref('answer', lazy=True))
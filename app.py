from datetime import datetime
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from models.department import Department
from models.employee import Employee
from models.answer import Answer
from models.question import Question
from models.satisfactionsurvey import SatisfactionSurvey
from extensions import db
from query_database import fetch_data


load_dotenv()
azure_mysql_username = os.getenv("AZURE_MYSQL_USERNAME")
azure_mysql_password = os.getenv('AZURE_MYSQL_PASSWORD')
azure_mysql_host = os.getenv("AZURE_MYSQL_HOST")
azure_mysql_port = 3306
azure_mysql_database = os.getenv("AZURE_MYSQL_DATABASE")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{azure_mysql_username}:{azure_mysql_password}@{azure_mysql_host}:{azure_mysql_port}/{azure_mysql_database}'
CORS(app)
db.init_app(app)

print("####################################### Teams Bot Server Started!")


@app.route('/user_data', methods=['GET'])
def get_user_data():
    print("user_data endpoint!")
    return jsonify({"received_data": "you sent a GET request to user_data endpoint!"})


@app.route('/query_data', methods=['POST'])
def get_query_data():
    data = request.get_json()
    sql_query = data.get('query')
    print("################# received:", sql_query)

    columns, values = fetch_data(sql_query)
    return jsonify({"columns": columns, "values": values})


@app.route('/user_data', methods=['POST'])
def post_user_data():
    data = request.get_json()
    print("data received:", data)

    # Create department if it doesn't exist yet
    department_name = data.get('department')
    department_id = None
    if department_name:
        department_id = add_department(department_name)
    else:
        department_id = add_department('Ei osastoa')

    # Create employee for the department
    employee_id = add_employee(department_id)

    # Create survey if it doesn't exist yet
    survey_date = data.get('currentDate')
    survey_id = add_satisfaction_survey(survey_date)

    # Iterate through the key-value pairs in the data
    for question_key in data.keys():
        # The key is the question and the value is the answer. Don't include currentDate or department.
        if question_key not in ['currentDate', 'department']:
            answer = data.get(question_key)
            answer_type = 'integer'
            if answer == 'True' or answer == 'False':
                answer_type = 'boolean'
                # Convert string of boolean to actual boolean
                answer = (answer == 'True')

            # Create the question if it doesn't exist yet
            question_id = add_question(question_key, answer_type, survey_id)
            # Create the answer for the question
            add_answer(answer_type, answer, question_id, employee_id)

    return jsonify({"data_saved": data})


def add_department(dep):
    existing_department = Department.query.filter_by(name=dep).first()
    if existing_department is None:
        new_department = Department(name=dep)
        db.session.add(new_department)
        db.session.commit()
        return new_department.id
    else:
        return existing_department.id


# Always creates a new employee because employees answer anonymously
def add_employee(dep_id):
    new_employee = Employee(department_id=dep_id)
    db.session.add(new_employee)
    db.session.commit()
    return new_employee.id


def add_satisfaction_survey(s_date):
    s_date = datetime.strptime(s_date, '%m/%d/%Y %H:%M:%S').date()
    existing_survey = SatisfactionSurvey.query.filter_by(surveyDate=s_date).first()
    if existing_survey is None:
        new_survey = SatisfactionSurvey(surveyDate=s_date)
        db.session.add(new_survey)
        db.session.commit()
        return new_survey.id
    else:
        return existing_survey.id


def add_question(q, ans_type, sv_id):
    existing_question = Question.query.filter_by(question=q, satisfactionSurvey_id=sv_id).first()
    if existing_question is None:
        new_question = Question(question=q, answerType=ans_type, satisfactionSurvey_id=sv_id)
        db.session.add(new_question)
        db.session.commit()
        return new_question.id
    else:
        return existing_question.id


# Always creates an answer because employees can answer only once
def add_answer(ans_type, ans, q_id, emp_id):
    # Response is either integer or boolean
    num_response = None
    bool_response = None
    if ans_type == 'boolean':
        bool_response = ans
    else:
        num_response = ans

    new_answer = Answer(booleanResponse=bool_response, numericResponse=num_response,
                        question_id=q_id, employee_id=emp_id)
    db.session.add(new_answer)
    db.session.commit()
    return new_answer


if __name__ == '__main__':
    app.run(debug=True)

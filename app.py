import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_teachers():
    path = os.path.join(BASE_DIR, 'teacher_answer.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/result", methods=["POST"])
def result():
    teachers = load_teachers()
    
    # HTML에서 제출한 답변 25개 수집
    user_answers = [int(request.form[f'q{i}']) for i in range(1, 26)]
    
    # 차이점 계산
    scores = {}
    for t_name, t_answers in teachers.items():
        diff = sum(abs(u - t) for u, t in zip(user_answers, t_answers))
        scores[t_name] = diff

    best_teacher = min(scores, key=scores.get)
    best_score = scores[best_teacher]

    # result.html 페이지로 매칭된 선생님 이름과 차이 점수를 넘겨줍니다.
    return render_template("result.html", teacher=best_teacher, score=best_score)

if __name__ == "__main__":
    app.run(debug=True)
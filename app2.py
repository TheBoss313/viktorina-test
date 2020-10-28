from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
questions = [{'100': '100', '200': '200', '300': '300', '400': '400'},
             {'100': '100', '200': '200', '300': '300', '400': '400'},
             {'100': '100', '200': '200', '300': '300', '400': '400', '500': '500'}]
qt_dict = {'0': 'question type 1', '1': 'question type 2', '2': 'Question type 3'}
players = {'Name1': 0, 'Name2': 0, 'Name4': 0, 'Name5': 0}


def check(a, b):
    try:
        questions[a][b]
    except KeyError:
        return None
    else:
        return questions[a]


@app.route('/')
def main_page():
    return render_template('index_gkrs.html', questions=questions, qt=qt_dict, check=check)


@app.route('/<int:qt>:<int:pts>/')
def question(qt, pts):
    qt1 = qt_dict[f'{qt}']
    quest = questions[qt][str(pts)]
    del questions[qt][str(pts)]
    return render_template(r'question_gkrs.html', qt=qt1, pts=pts, q=quest)


@app.route('/scores/')
def scores():
    return render_template('scoreboard_gkrs.html', players=players)


@app.route('/admin/', methods=['get', 'post'])
def admin():
    if request.method == 'POST':
        name = request.form.get('name')
        pts = request.form.get('pts')
        players[name] = int(pts)
    return render_template('admin_gkrs.html', players=players)


if __name__ == '__main__':
    app.run()

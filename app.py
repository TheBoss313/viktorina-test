from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
import os

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)
questions_base = [{'100': '“Бежали дни, и он всё больше слабел. И вот настала ночь, когда никто не лёг спать. Вся шайка собралась вокруг. Он лежал неподвижно, прикрыв глаза. Они испуганно вглядывались в его лицо, отыскивая в нём признаки жизни, но, несмотря на яркий огонь в очаге и резкий свет свечи, у кровати было темно”',
                   '200': '“И тут они в испуге выбежали из пещеры. Они злобно глядели на Рони, щёлкали языками и шипели, а она в ответ шипела на них. А когда Бирк пригрозил им копьём, они сломя голову ринулись вниз, цепляясь за выступы отвесной скалы, чтобы не сорваться”',
                   '300': '“Рони шла узенькой тропинкой вниз по крутому склону, осторожно ступая, чтобы не поскользнуться. Когда тропинка вошла в лес, Рони побежала между берёзками и соснами к лесной полянке, где был родник. Но вдруг остановилась как вкопанная. На камне у самого родника кто-то сидел. И представьте себе, это был ...! Да, это был он! Это его чёрные вьющиеся волосы. Сердце Рони замерло, слёзы брызнули из глаз”',
                   '400': '“Послушай, радость моей души, - начал он. - Когда я мальчишкой бродил по лесу, точь-в-точь как ты сейчас, я однажды спас жизнь одному маленькому серому гному, которого хотели погубить злые друды. По чести сказать, серые гномы - отвратительные твари, но этот был совсем не похож на других, и к тому же он так благодарил меня, что я просто не знал, как от него избавиться. И представляешь, он вбил себе в голову, чтобы обязательно должен мне что-то подарить”',
                   '500': '“Крадучись вышла он из зала и взвалила на плечо свой узел, который ещё днём спрятала в чулане. Он был такой тяжёлый, что она еле его тащила. Поэтому, как только она дошла до…, она швырнула его наземь, и узел покатился прямо к ногам…, которые стояли в дозоре”'},
                  {'100': 'Расти не по дням, а по часам', '200': 'След простыл ', '300': 'Нехитрое дело', '400': 'Чуть свет', '500': 'Висеть на волоске'},
                  {'100': 'Из-за чего поссорились Рони с Бирком в пещере?',
                   '200': ' Как звали лошадей, которых приручили Рони с Бирком?',
                   '300': 'Как Рони застряла в сугробе?',
                   '400': ' Как любили веселиться разбойники?',
                   '500': ' Что делала Ловиса каждый вечер перед сном?'},
	              {'100': 'В ясный полдень, в прекрасную погоду, все умерли.',
                   '200': 'Сын узнал, что его мама ведьма.',
                   '300': 'Мальчик и девочка вместе потеряли ложку.',
                   '400': 'Наступила зима, и было так грустно, что захотелось плакать.',
                   '500': 'Пришли прекрасные высокие существа и хотели помочь. Все подружились и стали жить вместе.'}]
qt_dict = {'0': 'Догадайся по описанию', '1': 'Словарь', '2': 'Сюжет', '3': 'Перевёртыши'}
players_base = {'Name1': 0, 'Name2': 0, 'Name4': 0, 'Name5': 0}
questions = questions_base.copy()
players = players_base.copy()

def check(a, b):
    try:
        questions[a][b]
    except KeyError:
        return None
    else:
        return questions[a]


@app.before_first_request
def clear():
    session.clear() # Clears sessions
    questions = questions_base.copy()


@app.route('/')
def main_page():
    if 'logged_in' in session and session['logged_in'] == 'true': 
        return render_template(r'index_gkrs.html', questions=questions, qt=qt_dict, check=check, players=players)
    else:
        return redirect(url_for('login'))


@app.route('/<int:qt>:<int:pts>/')
def question(qt, pts):
    qt1 = qt_dict[f'{qt}']
    quest = questions[qt][str(pts)]
    del questions[qt][str(pts)]
    return render_template(r'question_gkrs.html', qt=qt1, pts=pts, q=quest)


@app.route('/scores/')
def scores():
    return render_template(r'scoreboard_gkrs.html', players=players)


@app.route('/admin/', methods=['get', 'post'])
def admin():
    if request.method == 'POST':
        name = request.form.get('name')
        pts = request.form.get('pts')
        players[name] = int(pts)
    return render_template(r'admin_gkrs.html', players=players)


@app.route('/login/', methods=['get','post'])
def login(message = ''):
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'gkrs2020':
            session['logged_in'] = 'true'
            return redirect(url_for('main_page'))
        else:
            return render_template('login.html', message='WRONG PASSWORD')
    else:
        return render_template('login.html')

@app.route('/reset/', methods=['get','post'])
def reset(message = ''):
    global questions, questions_base
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'gkrs2006':
            questions = questions_base.copy()
            players = players_base.copy()
            return redirect(url_for('main_page'))
        else:
            return render_template('reload.html', message='WRONG PASSWORD')
    else:
        return render_template('reload.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


# A very simple Flask Hello World app for you to get started with...


from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from socket import gethostname
import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True
Markdown(app)


db_uri = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    measureid = db.Column(db.Integer, primary_key=True, autoincrement=True)

    patientid = db.Column(db.Integer)
    patientName = db.Column(db.Text())
    ward = db.Column(db.Text())
    diagnosis = db.Column(db.Text())
    evaperiod = db.Column(db.Text())
    evadate = db.Column(db.Date())
    SS10m = db.Column(db.Numeric)
    MS10m = db.Column(db.Numeric)
    TUG = db.Column(db.Numeric)
    sixmwt = db.Column(db.Numeric)
    FMA = db.Column(db.Integer)
    BBS = db.Column(db.Integer)
    staffname = db.Column(db.Text())



#ホーム画面
@app.route('/')
def list():
    message = '評価一覧'
    posts = Post.query.all()

    return render_template('all_list.html', message=message, posts=posts)

#評価日が新しい順に表示
@app.route('/resent')
def resent_list():
    message = '評価一覧'
    posts = Post.query.order_by(Post.evadate.desc()).limit(5)

    return render_template('resent_list.html', message=message, posts=posts)


#評価ごとに表示する。
@app.route('/show/<int:measureid>')
def show_post(measureid):
    message = "さんの評価です。"
    post = Post.query.get(measureid)

    return render_template('show.html', message=message, post=post)

#新規の評価を入力する
@app.route('/new')
def new_post():
    message = '評価を入力して下さい。'
    return render_template('new.html', message=message)

#評価をDBに取り込む
@app.route('/create', methods=['POST'])
def create_post():
    message = 'create your memo'

    new_post = Post()
    new_post.patientid = request.form['patientid']
    new_post.patientName = request.form['patientName']

    new_post.ward = request.form['ward']
    new_post.diagnosis = request.form['diagnosis']
    new_post.evaperiod = request.form['evaperiod']
    new_post.evadate = request.form['evadate']
    new_post.SS10m = request.form['SS10m']
    new_post.MS10m = request.form['MS10m']
    new_post.TUG = request.form['TUG']
    new_post.sixmwt = request.form['sixmwt']
    new_post.FMA = request.form['FMA']
    new_post.BBS = request.form['BBS']
    new_post.staffname = request.form['staffname']


    db.session.add(new_post)
    db.session.commit()

    post = Post.query.get(new_post.measureid)

    return render_template('show.html', message=message, post=post)

#評価を削除する。
@app.route('/destroy/<int:measureid>')
def destroy_post(measureid):
    message = 'Destroy your memo ' + str(measureid)

    destroy_post = Post.query.get(measureid)
    db.session.delete(destroy_post)
    db.session.commit()

    posts = Post.query.all()

    return render_template('list.html', message=message, posts=posts)

#評価を編集する。
@app.route('/edit/<int:measureid>')
def edit_post(measureid):

    message = '編集します。'
    post = Post.query.get(measureid)

    return render_template('edit.html', message=message, post=post)

#評価を更新するプログラム。
@app.route('/update/<int:measureid>', methods=['POST'])
def update_post(measureid):
    message = 'update your memo' +str(measureid)

    post = Post.query.get(measureid)
    post.patientid = request.form['patientid']
    post.patientName = request.form['patientName']
    post.ward = request.form['ward']
    post.diagnosis = request.form['diagnosis']
    post.evaperiod = request.form['evaperiod']
    post.evadate = request.form['evadate']
    post.SS10m = request.form['SS10m']
    post.MS10m = request.form['MS10m']
    post.TUG = request.form['TUG']
    post.sixmwt = request.form['sixmwt']
    post.FMA = request.form['FMA']
    post.BBS = request.form['BBS']
    post.staffname = request.form['staffname']

    db.session.commit()

    return render_template('show.html', message = message, post = post)

if __name__ == '__main__':
    app.run()

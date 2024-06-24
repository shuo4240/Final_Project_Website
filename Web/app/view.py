from app import app
from app import db
from flask import render_template, flash, redirect, url_for, request
from app.model import UserRegister
from app.form import FormRegister, FormLogin, UsernameUpdate, PasswordUpdate
from flask_login import login_user, current_user, login_required, logout_user
import time


@app.route('/')
def home():  # put application's code here
    return render_template('base.html')


@app.route('/ChooseGame')
def choose_game():  # put application's code here
    return render_template('guess_word.html')
    #return render_template('ChooseGame.html')


@app.route('/OtherWeb')
def other_web():  # put application's code here
    return render_template('OtherWeb.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = UserRegister(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Register Success, Thank You')
        return redirect(url_for('home'))
        # return 'Success Thank You'
    print(form.errors)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        #  當使用者按下login之後，先檢核帳號是否存在系統內。
        user = UserRegister.query.filter_by(email=form.email.data).first()
        if user:
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.check_password(form.password.data):
                #  加入參數『記得我』
                login_user(user, form.remember_me.data)
                #  使用者登入之後，將使用者導回來源url。
                #  利用request來取得參數next
                next = request.args.get('next')
                #  自定義一個驗證的function來確認使用者是否確實有該url的權限
                if not next_is_valid(next):
                    #  如果使用者沒有該url權限，那就reject掉。
                    return 'Bad Boy!!'
                flash('Login Successful')
                return redirect(next or url_for('home'))
                # return 'Welcome' + current_user.username
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('Wrong Email or Password')
        else:
            #  如果資料庫無此帳號，就顯示錯誤訊息。
            flash('Wrong Email or Password')
    return render_template('login.html', form=form)


def next_is_valid(url):
    """
    為了避免被重新定向的url攻擊，必需先確認該名使用者是否有相關的權限，
    舉例來說，如果使用者調用了一個刪除所有資料的uri，那就GG了，是吧 。
    :param url: 重新定向的網址
    :return: boolean
    """
    return True


"""
@app.route('/already_login')
@login_required
def login_home():
    return render_template('base.html')
"""


@app.route('/logout')
def logout():
    logout_user()
    flash('Log Out, See You.')
    return render_template('base.html')


"""
@app.route('/userinfo')
@login_required
def userinfo():
    return 'Here is UserINFO'
"""


@app.route('/update_username', methods=['GET', 'POST'])
@login_required
def update_username():
    form = UsernameUpdate()
    if form.validate_on_submit():
        current_user.username = form.new_username.data
        db.session.commit()
        flash('Updates username successfully!')
        return redirect(url_for('home'))
    return render_template('update_username.html', form=form)

@app.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = PasswordUpdate()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Password updated successfully!')
            return redirect(url_for('home'))
        else:
            flash('Current password is incorrect.')
    return render_template('update_password.html', form=form)

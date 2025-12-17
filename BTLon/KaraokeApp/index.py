import math

from flask import render_template, request, redirect

from KaraokeApp import dao, app, db, admin
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    rooms = dao.loadrooms()
    return render_template("index.html", rooms=rooms)

@app.route('/room')
def room():
    page = request.args.get('page',1, type=int)
    rooms = dao.loadrooms(page=page)
    branches = dao.loadbranches()
    pages = math.ceil(dao.count_room()/app.config["PAGE_SIZE"])

    return render_template("room.html", rooms=rooms, branches=branches, pages=pages, current_page=page)

@app.route('/room/<room_id>')
def details(room_id):
    rooms = dao.get_room_by_id(room_id)

    if rooms:
        branches = dao.get_branches_by_id(rooms.branch_id)
        return render_template("room-details.html", rooms=rooms, branches=branches)

@app.route('/login', methods=['GET', 'POST'])
def login_my_user():

    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = 'Tài khoản và mật khẩu không đúng'

    return render_template("login.html", err_msg=err_msg)

@app.route('/logout')
@login_required
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route('/admin-login', methods=['POST'])
def admin_login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)

    if user:
        login_user(user)
        return redirect('/admin')
    else:
        err_msg = 'Tài khoản và mật khẩu không đúng'

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
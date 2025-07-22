from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = []  # [{id, pw, is_admin, room}]
logs = []   # [{user, action, room}]
room_states = {
    'room101': {'temperature': 25, 'humidity': 50, 'led': False, 'buzzer': False},
    'room102': {'temperature': 26, 'humidity': 45, 'led': False, 'buzzer': False}
}

current_user = None  # 로그인된 사용자 정보

@app.route('/')
def home():
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global users
    if request.method == 'POST':
        user = {
            'id': request.form['id'],
            'pw': request.form['pw'],
            'is_admin': request.form.get('admin') == 'on',
            'room': request.form.get('room')
        }
        users.append(user)
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        for u in users:
            if u['id'] == request.form['id'] and u['pw'] == request.form['pw']:
                current_user = u
                return redirect('/admin' if u['is_admin'] else '/dashboard')
        return "로그인 실패"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not current_user or current_user.get('is_admin'):
        return redirect('/login')
    room = current_user['room']
    state = room_states[room]
    return render_template('dashboard.html', room=room, state=state)

@app.route('/admin')
def admin():
    if not current_user or not current_user.get('is_admin'):
        return redirect('/login')
    return render_template('admin.html', rooms=room_states, logs=logs)

@app.route('/toggle/<device>/<room>')
def toggle_device(device, room):
    if not current_user:
        return redirect('/login')
    room_states[room][device] = not room_states[room][device]
    logs.append({
        'user': current_user['id'],
        'action': f"Toggled {device}",
        'room': room
    })
    return redirect('/admin' if current_user['is_admin'] else '/dashboard')

@app.route('/logout')
def logout():
    global current_user
    current_user = None
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

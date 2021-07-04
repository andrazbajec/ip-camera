from flask import Flask, render_template, Response, request, redirect, url_for, make_response
import cv2
from user import User

app = Flask(__name__)
camera = cv2.VideoCapture(0)
app.static_folder = 'static'

def gen_frames():
    while True:
        success, frame = camera.read()

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    if not User.authenticate():
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    if User.authenticate():
        return redirect('/')

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    authToken = User.login(username, password)
    response = make_response(redirect(url_for('login')))

    if authToken:
        response.set_cookie('auth_token', authToken)

    return response


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")
    app.run(debug=True)
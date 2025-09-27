from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def jarvis_ui():
    return render_template('index.html')  # This will render the Jarvis HTML

if __name__ == '__main__':
    app.run(debug=True)

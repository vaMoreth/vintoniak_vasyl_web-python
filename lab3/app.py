from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('portfolio.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

if __name__ == '__main__':
    app.run(debug=True)
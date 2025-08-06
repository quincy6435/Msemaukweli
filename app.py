from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set()  # No restriction
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        article = request.form.get('article')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if article and article.strip():
            article_filename = f"article_{len(os.listdir(app.config['UPLOAD_FOLDER']))}.txt"
            with open(os.path.join(app.config['UPLOAD_FOLDER'], article_filename), 'w', encoding='utf-8') as f:
                f.write(article)
        return redirect(url_for('index'))
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    uploads = []
    for fname in files:
        upload = {'filename': fname}
        if fname.endswith('.txt'):
            try:
                with open(os.path.join(app.config['UPLOAD_FOLDER'], fname), 'r', encoding='utf-8') as f:
                    upload['article_content'] = f.read()
            except Exception:
                upload['article_content'] = '[Could not read article]'
        uploads.append(upload)
    return render_template('index.html', uploads=uploads)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

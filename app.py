import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'debugsecret')

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('API_KEY'),
    api_secret=os.getenv('API_SECRET'),
    secure=True
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'txt'}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        article = request.form.get('article')
        try:
            if file and file.filename != '' and allowed_file(file.filename):
                result = cloudinary.uploader.upload(
                    file,
                    folder="msemaukweli",
                    resource_type="auto"
                )
                flash(f"Uploaded: {result['secure_url']}", 'success')
            if article and article.strip():
                result = cloudinary.uploader.upload(
                    article,
                    folder="msemaukweli",
                    resource_type="auto",
                    public_id=f"article_{len(article)}_{hash(article)}.txt"
                )
                flash(f"Article uploaded: {result['secure_url']}", 'success')
        except Exception as e:
            flash(f"Upload error: {str(e)}", 'danger')
            print(f"Upload error: {str(e)}")
        return redirect(url_for('index'))
    try:
        resources = cloudinary.Search()\
            .expression('folder=msemaukweli')\
            .execute()
        uploads = resources.get('resources', [])
    except Exception as e:
        flash(f"Error fetching resources: {str(e)}", 'danger')
        print(f"Error fetching resources: {str(e)}")
        uploads = []
    return render_template('index.html', uploads=uploads)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

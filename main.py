from flask.templating import render_template
import random, string
import showdb_py, os, flask_sslify, flask_recaptcha
from flask import Flask, request
db = showdb_py.connect(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'))

app = Flask(__name__)
sllify = flask_sslify.SSLify(app)
recaptcha = flask_recaptcha.ReCaptcha(app, site_key='6Ld_ghAdAAAAACan9vE4SN4uQZTlzJOtDVHm-vit', secret_key=os.environ.get('CAPTCHA_SECRET'))
recaptcha.theme = 'dark'

@app.route('/', methods=['GET', 'POST'])
def _main_page():
    if request.method == 'POST':
        if recaptcha.verify():
            while True:
                url = ''.join(random.sample(string.ascii_letters, 5))
                if url not in db.keys(): break
            db[url] = request.form.get('link')
            return render_template('generated.html', link=f'shortened.site/{url}')
        else:
            return render_template('register.html', message="You must complete the captcha.", prefill=request.form.get('link'))
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT'), debug=True, threaded=True)
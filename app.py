import pickle
from flask import Flask, render_template, request
import gzip

with gzip.open('stats.pkl.gz', 'rb') as f:
    stats = pickle.loads(f.read())

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        print(request.form.to_dict())
        try:
            token_id = int(request.form.get('token_id'))
        except:
            return render_template("index.html", error="Please input a token id between 1 and 1316005")
        if token_id < 1 or token_id > 1316005:
            return render_template("index.html", error="Please input a token id between 1 and 1316005")
        token = stats[token_id]
        print(token)
        return render_template("index.html", token=token, token_id=token_id)
    elif request.method == 'GET':
        return render_template("./index.html")


if __name__ == '__main__':
    app.run()
import pickle
from flask import Flask, render_template, request
from bag_looker import get_stats

with open('stats.pkl', 'rb') as f:
    ranks = pickle.loads(f.read())

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        print(request.form.to_dict())
        try:
            token_id = int(request.form.get('token_id'))
        except:
            return render_template("index.html", error="Please input a token id between 1 and 1316004")
        if token_id < 1 or token_id > 1316004:
            return render_template("index.html", error="Please input a token id between 1 and 1316004")
    elif request.method == 'GET':
        token_id = 174966
    token = get_stats(token_id)
    token['rank'] = ranks[token_id]
    return render_template("index.html", token=token, token_id=token_id)


if __name__ == '__main__':
    app.run()

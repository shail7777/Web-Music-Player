from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    shows = ["Friends", "Office", "HIMYM", "DragonballZ", "Shin Chan"]
    print('updated')
    return render_template(
        "index.html",
        len = len(shows), shows = shows,
    )
    
app.run(
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0'),
    debug=True
)
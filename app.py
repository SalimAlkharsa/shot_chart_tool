from flask import Flask, render_template, request
from Utils.gather_data import Query
from Utils.shot_chart import ShotChart

import matplotlib
matplotlib.use('Agg')  # Use Agg backend to render images without a GUI
import matplotlib.pyplot as plt


app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return '''
    <form method="POST" action="/result">
        <label for="query">Enter the query:</label><br>
        <input type="text" name="query" id="query"><br>
        <p>Query Format: Player Name,Team Name,LastNGames,DateFrom,DateTo</p>
        <p>Fill a 0 if you do not want to specify a field. Date is in YYYYMMDD format.</p>
        <p>Example: 0,Boston Celtics,0,0,0</p>
        <input type="submit" value="Submit">
    </form>
    '''

@app.route('/result', methods=['POST'])
def result():
    query_str = request.form['query']
    query = Query(query_str)
    df = query.data
    Chart = ShotChart(df)
    # Make the shot chart without launching a GUI
    Chart.make_shot_chart()
    image_filename = 'shot_chart_'+query_str+'.png'
    # Save the image to static folder named as shot_chart_query.png
    plt.savefig(f'static/{image_filename}')


    # Return the URL of the saved image to be displayed
    return f'<img src="static/{image_filename}">'




if __name__ == '__main__':
    app.run(debug=True)

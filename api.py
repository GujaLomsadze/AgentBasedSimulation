"""
Super Basic REST-API endpoint to draw a dynamic Node graph
    and return changed nodes.json to javascript calls.

"""

import json

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='/static')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Route to render the HTML template
@app.route('/network/show', methods=['GET'])
def network():
    return render_template('graph_show.html')


# Create an endpoint to handle color updates
@app.route('/update_node_color', methods=['POST'])
def update_node_color():
    data = request.json
    # Implement logic to update node colors based on data['nodeId'] and data['color']
    # You can send a response with a success message or updated data
    response_data = {'success': True, 'message': 'Node color updated'}
    return jsonify(response_data)


@app.route('/get_nodes_n_links')
@cross_origin()
def get_nodes_n_links():
    data = open("data/nodes.json")
    data = json.loads(data.read())

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

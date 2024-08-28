from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# Directory to save HTML files
GRAPH_DIR = os.path.join(os.getcwd(), 'static', 'graphs')


@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    data = request.json
    option = data.get('option')
    filename = "prophet_output.html"

    try:
        if option == 'option1':
            # Run the script to fetch data and generate a graph using Facebook Prophet
            if not os.path.exists(GRAPH_DIR):
                os.makedirs(GRAPH_DIR)
            subprocess.run(["python", "facebook_prophet.py", os.path.join(GRAPH_DIR, filename)], check=True)
        elif option == 'option2':
            subprocess.run(["python", "your_script_for_algorithm2.py"], check=True)

        return jsonify(success=True, graph_url=f'/graphs/{filename}')
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, error=str(e))


@app.route('/graphs/<filename>')
def serve_graph(filename):
    return send_from_directory(GRAPH_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

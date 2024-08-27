from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)


# Root route to display a welcome message
@app.route('/')
def home():
    return "Welcome to the Crypto Prediction Service"


@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    data = request.json
    option = data.get('option')

    try:
        if option == 'option1':
            # Run the script to fetch data and generate a graph using Facebook Prophet
            subprocess.run(["python", "facebook_prophet.py"], check=True)
        elif option == 'option2':
            # Placeholder for another algorithm or script
            subprocess.run(["python", "your_script_for_algorithm2.py"], check=True)
        # Add more options as necessary

        # Return success response after generating the graph
        return jsonify(success=True)
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, error=str(e))


if __name__ == '__main__':
    app.run(debug=True)

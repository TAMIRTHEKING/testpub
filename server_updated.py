from flask import Flask, jsonify, request
import csv
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
app = Flask(__name__)

# Load data into a pandas DataFrame
df = pd.read_csv('home_test.csv')

# Define time rules 180/60
TIME_RULE = timedelta(hours=3)

# Clean up time columns and sort by arrival time
df['Arrival'] = df['Arrival'].str.strip().apply(
    lambda x: datetime.strptime(x, '%H:%M').strftime('%H:%M'))
df['Departure'] = df['Departure'].str.strip().apply(
    lambda x: datetime.strptime(x, '%H:%M').strftime('%H:%M'))
df = df.sort_values(by=['Arrival'])


@app.route('/flights')
def flights():
    # Return all flights as JSON
    return df.to_json(orient='records')

# Define the endpoint for getting flight data by ID


@app.route('/flight/<flight_id>', methods=['GET'])
def get_flight(flight_id):
    # Get the row with the given ID
    row = df[df['flight ID'] == flight_id].to_dict('records')
    if len(row) != 0:
        # Convert the row to a dictionary and return as JSON
        return jsonify(row), 200
    else:
        # Return a 404 error if no row is found
        return jsonify({'message': 'Flight not found'}), 404

# change status by flight ID


@app.route('/flights/<flight_id>/<success>', methods=['POST'])
def update_flight(flight_id, success):
    if request.method == 'POST':
        success = success
        if success is None:
            return jsonify({'error': 'Success parameter is missing'}), 400
        elif success != 'success' and success != 'fail':
            return jsonify({'error': 'Success parameter is not valid'}), 400
        else:
            idx = df.index[df['flight ID'] == flight_id]
            if idx.empty:
                return jsonify({'error': 'Flight not found'}), 404
            else:
                df.loc[idx, 'success'] = success

                # In real world it will update the start csv or DB
                df.to_csv('serverupdate.csv', index=False)

                return jsonify({'message': 'Success column updated for flight {}'.format(flight_id)})


@app.route('/update_flights', methods=['POST'])
def update_flights():
    json_payload = request.json

    # Get the list of updates from the JSON payload

    # Create a list to store the results of the updates
    results = []

    # Loop through each update and apply it to the corresponding row in the flights DataFrame
    for update in json_payload:
        flight_id = update['flight_id']
        success = update['success']
        idx = df.index[df['flight ID'] == flight_id]
        # if id not in flight id
        if idx.empty:
            results.append(
                {"flight_id": flight_id, "success": "na", "status": "not found"})
        else:
            # if in flight id update
            update_flight(flight_id, success)
            results.append(
                {"flight_id": flight_id, "success": success, "status": success})

    # Return the results as a JSON response
    return jsonify({"results": results})


# Run the server
if __name__ == '__main__':
    app.run(debug=False)

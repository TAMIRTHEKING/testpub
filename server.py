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

# Endpoint for getting flight data by ID


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


@app.route('/flights/<flight_id>', methods=['POST'])
def update_flight(flight_id):
    if request.method == 'POST':
        success = request.json.get('success')
        if success is None:
            return jsonify({'error': 'Success parameter is missing'}), 400
        else:
            idx = df.index[df['flight ID'] == flight_id]
            if idx.empty:
                return jsonify({'error': 'Flight not found'}), 404
            else:
                df.loc[idx, 'success'] = success

                # In real world it will update the start csv or DB
                df.to_csv('serverupdate.csv', index=False)

                return jsonify({'message': 'Success column updated for flight {}'.format(flight_id)})


# Run the server
if __name__ == '__main__':
    app.run(debug=False)

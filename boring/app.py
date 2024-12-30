from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
import json
import os

app = Flask(__name__)

# Route for the main CSV editor
@app.route('/')
def index():
    return render_template('index.html')

# Route for loading CSV files
@app.route('/load/<int:file_index>')
def load_file(file_index):
    try:
        filename = f'file{file_index}.csv'
        df = pd.read_csv(filename)
        return jsonify({
            'data': df.to_dict('records'),
            'columns': df.columns.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route for saving CSV files
@app.route('/save/<int:file_index>', methods=['POST'])
def save_file(file_index):
    try:
        data = request.json
        df = pd.DataFrame(data)
        filename = f'file{file_index}.csv'
        df.to_csv(filename, index=False)
        return jsonify({'message': 'File updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route for 3D visualization page
@app.route('/visualization')
def visualization():
    return render_template('visualization.html')

# Route for getting 3D visualization data
@app.route('/get_3d_data')
def get_3d_data():
    try:
        fig = go.Figure()
        
        # Read and process each CSV file
        for i in range(1, 3):  # Adjust range based on number of files
            df = pd.read_csv(f'file{i}.csv')
            
            x = df.index
            y = range(len(df.columns))
            z = df.values

            fig.add_trace(go.Surface(
                x=x,
                y=y,
                z=z,
                name=f'Layer {i}',
                opacity=0.7,
                showscale=True
            ))

        fig.update_layout(
            scene=dict(
                xaxis_title='X Axis',
                yaxis_title='Y Axis',
                zaxis_title='Values'
            ),
            title='3D Visualization of CSV Layers'
        )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify(graphJSON)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
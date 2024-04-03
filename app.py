# app.py

from flask import Flask, render_template, request, jsonify
import h5py
import yaml
from plotter import Plotter
import pandas as pd
import plotly.io as pio

app: Flask = Flask(__name__)


# Function to read plotting specifications from YAML file
def read_plot_specs(file_path=None):
    if file_path is not None:
        with open(file_path, 'r') as file:
            specs = yaml.safe_load(file)
        return specs
    else:
        return None

with app.app_context():
    specs = read_plot_specs('plot_specs.yaml')

def load_data(file_path='fake_data.h5'):
    # Load data from HDF5 file
    data = pd.read_hdf(file_path)
    columns = data.columns

    # Store data and column names in app context
    app.data = data
    app.columns = columns

with app.app_context():
    load_data()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tab1')
def tab1():
    return render_template('tab1.html')


@app.route('/tab2')
def tab2():
    return render_template('tab2.html')


@app.route('/generate-plot', methods=['POST'])
def generate_plot(plot_specs=specs):
    # Get tab identifier from request
    tab = request.json.get('tab')

    # Get plot specifications for the requested tab
    plots = specs.get(tab, [])
    if not plots:
        return jsonify({'plots': []})

    # Generate HTML plots for the requested tab
    html_plots = []
    for plot in plots:
        # Create Plotter instance and set specifications
        p = Plotter()
        p.set_specs(plot)
        p.set_data(app.data)

        # Generate plot and convert to HTML
        p.make_plot()
        html_plots.append(pio.to_html(p.fig))

    # Return HTML plots to client
    return jsonify({'plots': html_plots})


@app.route('/tab3')
def tab3():
    return render_template('tab3.html', columns=app.columns)


@app.route('/generate-user-plot', methods=['POST'])
def generate_user_plot():
    # receive plot specs
    plot_specs = request.json

    # make the plot
    p = Plotter()
    p.set_specs(plot_specs)
    p.set_data(app.data)
    p.make_plot()
    return pio.to_html(p.fig)


if __name__ == '__main__':
    app.run(debug=True)

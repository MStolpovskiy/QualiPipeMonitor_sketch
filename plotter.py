import plotly.graph_objs as go
import plotly.express as px
import numpy as np

class Plotter:
    def __init__(self):
        self.plot_specs = {}
        self.data = None
        self.fig = None

    def set_specs(self, specs):
        """Set plot specifications."""
        self.plot_specs = specs

    def update_specs(self, specs):
        """Update plot specifications and recreate the plot."""
        self.plot_specs.update(specs)
        self.make_plot()

    def set_data(self, data):
        """Set data for plotting."""
        self.data = data

    def update_data(self, data):
        """Update data and recreate the plot."""
        self.data = data
        self.make_plot()

    def make_plot(self):
        """Create the plot."""
        if 'plot_type' not in self.plot_specs:
            return None

        plot_type = self.plot_specs['plot_type']

        if plot_type == '1d':
            self.fig = self._make_1d_plot()
        elif plot_type == '2d':
            self.fig = self._make_2d_plot()
        elif plot_type == '3d':
            self.fig = self._make_3d_plot()

    def _get_mask(self):
        """Get mask for plotting."""
        if 'masking_variable' in self.plot_specs.keys() and self.plot_specs['masking_variable'] != '':
            lower_limit = self.plot_specs['lower_limit']
            if lower_limit == '':
                lower_limit = -np.inf
            else:
                try:
                    lower_limit = float(lower_limit)
                except ValueError:
                    lower_limit = -np.inf
            upper_limit = self.plot_specs['upper_limit']
            if upper_limit == '':
                upper_limit = np.inf
            else:
                try:
                    upper_limit = float(upper_limit)
                except ValueError:
                    upper_limit = np.inf
            masking_variable = self.data[self.plot_specs['masking_variable']]
            mask = (masking_variable > lower_limit) & (masking_variable < upper_limit)
            return mask
        else:
            return None


    def _make_1d_plot(self):
        """Create a 1D plot."""
        if self.data is None:
            return None

        x_data = self.data[self.plot_specs['x_axis']]

        mask = self._get_mask()
        if mask is not None:
            x_data = x_data[mask]

        fig = go.Figure(data=[go.Histogram(x=x_data)])
        return fig

    def _make_2d_plot(self):
        """Create a 2D plot."""
        if self.data is None:
            return None

        x_data = self.data[self.plot_specs['x_axis']]
        y_data = self.data[self.plot_specs['y_axis']]

        mask = self._get_mask()
        if mask is not None:
            x_data = x_data[mask]
            y_data = y_data[mask]

        fig = px.density_heatmap(x=x_data, y=y_data, marginal_x="histogram", marginal_y="histogram")
        return fig

    def _make_3d_plot(self):
        """Create a 3D plot."""
        if self.data is None:
            return None

        x_data = self.data[self.plot_specs['x_axis']]
        y_data = self.data[self.plot_specs['y_axis']]
        z_data = self.data[self.plot_specs['z_axis']]

        mask = self._get_mask()
        if mask is not None:
            x_data = x_data[mask]
            y_data = y_data[mask]
            z_data = z_data[mask]

        fig = px.scatter(x=x_data, y=y_data, color=z_data)
        return fig

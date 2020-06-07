from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

import pandas as pd
from math import pi
from bokeh.transform import cumsum
from bokeh.palettes import Category20c


class BaseChart:
    def __init__(self, chart_title=None):
        self._chart_title = chart_title

    @property
    def chart_title(self):
        return self._chart_title

    @chart_title.setter
    def chart_title(self, chart_title):
        if isinstance(chart_title, str):
            self._chart_title = chart_title
        else:
            raise Exception('Error chart_title')


class PieChart(BaseChart):

    def __init__(self):
        super(PieChart, self).__init__(self)
        self._pie_chart_data = dict()

    @property
    def pie_chart_data(self):
        return self._pie_chart_data

    @pie_chart_data.setter
    def pie_chart_data(self, pie_chart_data):
        if isinstance(pie_chart_data, dict):
            self._pie_chart_data = pie_chart_data
        else:
            raise Exception('Error pie_chart_data')

    def create_pie_chart(self):

        test_data = self._pie_chart_data
        data = pd.Series(test_data).reset_index(name='value').rename(
            columns={'index': 'category'})
        data['angle'] = data['value'] / data['value'].sum() * 2 * pi
        data['color'] = Category20c[len(test_data)]
        p = figure(plot_height=500, title=self.chart_title,
                   toolbar_location=None,
                   tools="hover", tooltips="@category: @value",
                   x_range=(-1, 1.0))

        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white", fill_color='color', legend_field='category',
                source=data)

        p.axis.axis_label = None
        p.axis.visible = False
        p.grid.grid_line_color = None
        plot_html = file_html(p, CDN)
        return plot_html

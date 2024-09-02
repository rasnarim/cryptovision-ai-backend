from bokeh.plotting import figure, output_file, save
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import DatetimeTickFormatter
import pandas as pd

def create_bokeh_plot(historical_time_values, prices, time_values, predictions,
                      upper_bound, lower_bound, crypto_name, algorithm):
    # Ensure all time values are datetime objects
    historical_time_values = pd.to_datetime(historical_time_values)
    time_values = pd.to_datetime(time_values)

    # Create a Bokeh plot
    p = figure(title=f"{algorithm} on {crypto_name.capitalize()} Price Prediction",
               x_axis_label='Time', y_axis_label='Price (USD)',
               width=800, height=400, x_axis_type="datetime")

    # Plot historical data
    p.line(historical_time_values, prices, legend_label="Historical Data", line_width=2, color='blue')

    # Plot the predicted trend line (including historical and future data)
    p.line(time_values, predictions, legend_label="Predicted Trend", line_width=2, color='green', line_dash='solid')

    # Plot upper and lower bounds for the entire prediction range (historical + future)
    p.line(time_values, upper_bound, legend_label="Upper Bound", line_width=2, color='red', line_dash='dotted')
    p.line(time_values, lower_bound, legend_label="Lower Bound", line_width=2, color='orange', line_dash='dotted')

    # Customize the plot
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.xaxis.formatter = DatetimeTickFormatter(days="%d %b %Y", months="%b %Y", years="%Y")

    # Get the HTML components
    script, div = components(p)

    # Combine everything into an HTML format
    plot_html = f"""
    <html>
    <head>
        {'<link rel="stylesheet" href="{}">'.format(CDN.css_files[0]) if CDN.css_files else ''}
        {'<script src="{}"></script>'.format(CDN.js_files[0]) if CDN.js_files else ''}
    </head>
    <body>
        {div}
        {script}
    </body>
    </html>
    """

    return p, plot_html  # Return the figure object and HTML string


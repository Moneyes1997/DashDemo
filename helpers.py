import pandas as pd
import numpy as np
from pmdarima.arima import auto_arima
import plotly.graph_objects as go


def revenue_forecaster(data_revenue, country, movie):
    """
    Forecast the next 3 month's revenue of a movie
    :param data_revenue: revenue data
    :param country: the country where the movie is watched
    :param movie: movie name
    :return: a plotly plot object
    """

    # Apply the filter
    if movie != '':
        filter = (data_revenue['Country'] == country) & \
                 (data_revenue['Movie'] == movie)
        df = data_revenue[filter]
    else:
        filter = data_revenue['Country'] == country
        df = data_revenue[filter]
        df = df.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()


    # Create the time index
    df['Index'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))

    # Make predictions
    model = auto_arima(np.log(df['Revenue'] + 1).to_numpy(), suppress_warnings=True)
    pred = model.predict(n_periods=3, return_conf_int=True)
    F = lambda x: np.exp(x) - 1  # Reverse pre-processing helper

    pred_yhat = F(pred[0])
    pred_ylower = F(pred[1][:, 0])
    pred_yupper = F(pred[1][:, 1])

    # Plot the result
    fig = go.Figure()
    if movie != '':
        fig.update_layout(
            title='Revenue Forecasting for ' + movie + ' in ' + country)
    else:
        fig.update_layout(
            title='Revenue Forecasting for ' + country)

    index_forecast = df['Index'][-4:] + pd.DateOffset(months=3)
    fig.add_trace(go.Scatter(x=index_forecast,
                             y=np.insert(pred_yhat, 0, df['Revenue'].to_numpy()[-1], axis=0),
                             mode='lines',
                             name='forecast', line_color='#d62728'))
    fig.add_trace(go.Scatter(x=index_forecast,
                             y=np.insert(pred_ylower, 0, df['Revenue'].to_numpy()[-1], axis=0),
                             mode='lines',
                             name='forecast_upper_95%_interval', line_color='#ff7f0e'))
    fig.add_trace(go.Scatter(x=index_forecast,
                             y=np.insert(pred_yupper, 0, df['Revenue'].to_numpy()[-1], axis=0),
                             mode='lines',
                             name='forecast_lower_95%_interval', line_color='#ff7f0e'))

    fig.add_trace(go.Scatter(x=df['Index'], y=df['Revenue'], mode='lines', name='past', line_color='#1f77b4'))

    return fig


def movie_tags(data_movie, movie):
    """
    Get the movie tags(such as genres)
    :param data_movie: movie data
    :param movie: title of the movie
    :return: text describing its tags
    """

    # Apply the filter
    filter = (data_movie['Movie'] == movie)
    df = data_movie[filter]

    # Get tags
    tags = df.columns[(df == 1).iloc[0]]
    tags = 'Tags: ' + ', '.join(tags) + ' (tags can be genres for example)'
    return tags


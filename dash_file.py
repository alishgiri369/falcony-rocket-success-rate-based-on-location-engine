import dash
import pandas as pd
from dash import dcc, html, Input, Output
import plotly.express as px


data = pd.read_csv('/Users/alishgiri/Desktop/jupyter-work/capstone/spacex_launch_dash.csv')

app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All sites', 'value': 'All'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='All',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={i :str(i) for i in range(0,10001,1000)},
                value=[0, 10000]),
    dcc.Graph(id='success-pie-chart'),
    dcc.Graph('success-payload-scatter-chart')
])


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def get_pie_chart(entered_site):
 
    
    if entered_site == 'All':
        
        fig = px.pie(data, names='Launch Site', values='class', 
                     title='Total Success Launches by Site')
    else:
        
        filtered_df = data[data['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Total Success Launches for site {entered_site}')

    return fig

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
   [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    mask = (data['Payload Mass (kg)'] >= low) & (data['Payload Mass (kg)'] <= high)
    filtered_data = data[mask]
    
    if entered_site == 'All':
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category', 
                         title='Correlation between Payload and Success for All Sites')
    else:
        filtered_data = filtered_data[filtered_data['Launch Site'] == entered_site]
        fig = px.scatter(filtered_data, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category', 
                         title=f'Correlation between Payload and Success for {entered_site}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

site_names = spacex_df['Launch Site'].drop_duplicates()
opts = []    
opts.append({'label': 'All Sites', 'value': 'ALL'})
for site_name in site_names:
    opts.append({'label': site_name, 'value': site_name})
                                
# Create a dash application
app = dash.Dash(__name__)

app.logger.info('START')
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                
                                dcc.Dropdown(id='site-dropdown', 
                                    options=opts,
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={
                                                    0: '0', 
                                                    2500: '2500',
                                                    5000: '5000',
                                                    7500: '7500',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.copy()
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
            names='Launch Site', 
            title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site].copy()
        filtered_df['count'] = 1
        fig = px.pie(filtered_df, values='count', 
            names='class', 
            title=f'Total Success Launches for site {entered_site}')
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), 
             Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, range_payload_mass):
    payload_filter = (spacex_df['Payload Mass (kg)'] >= range_payload_mass[0]) & (spacex_df['Payload Mass (kg)'] <= range_payload_mass[1])
    filtered_df = spacex_df[payload_filter].copy()
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site].copy()
        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for {entered_site} Site')

        return fig
        # return the outcomes piechart for a selected site


# Run the app
if __name__ == '__main__':
    app.run_server()

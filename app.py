from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

#####################   Get data from csv file  ###############
clients = pd.read_csv('hcp_clients.csv')

#####################   Dash App  #############################
# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)

server = app.server  # for Gunicorn
               
# Create the app's layout
app.layout = html.Div(
  [
    html.H1('Care Provider Name',
            style={'color': '#292B74',
                   'fontSize': '40px'}
           ),

    # ▼▼ Radio button to choose state (separated by divider lines) ▼▼
    html.Hr(),
    dcc.RadioItems(
      id='state-radio',
      options=['VIC', 'QLD'], 
      value='VIC'
    ),
    html.Hr(),

    # ▼▼ Commentary on data selection ▼▼
    html.P('Data selection:'),
    html.Ul(
      [html.Li('Clients with HCP packages'),
       html.Li('Service status: current'),
       html.Li('Service end date: blank')
      ]
    ),

    # ▼▼ INTERACTIVE CHART ▼▼
    dcc.Graph(figure={}, id='state-histogram'),

    # ▼▼ INTERACTIVE TABLE ▼▼
    dash_table.DataTable(
      id='clients-table',
      data=clients.to_dict('records'), 
      sort_action='native',
      style_cell=dict(textAlign='left'),
      page_size=10
    )
  ]
)

# Add controls to build the interaction
@callback(
    Output(component_id='state-histogram', component_property='figure'),
    Output('clients-table', component_property='data'),
    Input(component_id='state-radio', component_property='value')
)

def update_outputs(state_chosen):
  
  newdf = clients[clients['State'] == state_chosen].copy()
  
  fig = px.histogram(newdf, 
                     x='ClientType', 
                     text_auto=True,
                     labels={"ClientType": "Client Type", "count": "Number of clients"},
                     title=f"HCP clients in {state_chosen}"
                    )
  return fig, newdf.to_dict('records')
  
if __name__ == '__main__':
  # In Docker we don’t need debug=True and we bind on 0.0.0.0
  app.run(host="0.0.0.0", port=8050, debug=False)  

import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash
from dash import Input, Output, State, html, dcc, callback , dash_table
import plotly.express as px
import gparams
import plotly.graph_objects as go
from helper import Helper

# Initialize the app - constructor
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div(children=[

    html.Div([
        html.Label('Golden Unit Monitoring', style={'color': 'Black', 'font-size': 55}),
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    html.Div([

    html.Div(id='hidden-div', style={'display': 'none'}),

    html.Div(children=[

        html.Div([

            html.Div(children=[

                html.Label('Settings', style={'color': 'Black', 'font-size': 60}),
                html.Br(),

                html.Label('Client IP', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_set_client_ip', type='text', value='127.0.0.1', style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Server IP', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_set_server_ip', type='text', value='192.168.200.117', style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Number of probe packets', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_set_num_packets', type='text', value='12', style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Max probe duration (sec)', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_set_exp_duration', type='text', value='3', style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Ping interval (sec)', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_set_ping_interval', type='text', value='0.5', style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Ping packets', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_set_ping_packs', type='text', value='50', style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

            ], style={'padding': 10, 'flex': 1, 'width': '10%'}),

            html.Div(children=[
                html.Label('Measurement Setup', style={'color': 'Black', 'font-size': 60}),
                html.Br(),

                html.Label('Campaign name', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_meas_campaign_name', type='text', value='test', style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Experiments per campaign', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_meas_exps', type='text', value='3',
                          style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Campaign repetitions (times)', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_meas_repet', type='text', value='2',
                          style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

                html.Label('Repetition time gap (hours)', style={'color': 'Black', 'font-size': 35}),
                html.Br(),
                dcc.Input(id='in_meas_gap', type='text', value='1',
                          style={'width': '600px', 'font-size': 25}),
                html.Br(),
                html.Br(),

            ], style={'padding': 10, 'flex': 1}),

            html.Div(children=[
                html.Label('Application Filter', style={'color': 'Black', 'font-size': 60}),
                html.Br(),

                html.Label('Baseline', style={'color': 'Black', 'font-size': 35}),
                html.Div([
                    dcc.Dropdown(['True', 'False'], 'True', id='in_app_base',style={'width': '600px', 'font-size': 25}),
                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                html.Br(),

                html.Label('MQTT', style={'color': 'Black', 'font-size': 35}),
                html.Div([
                    dcc.Dropdown(['True', 'False'], 'True', id='in_app_mqtt',style={'width': '600px', 'font-size': 25}),
                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                html.Br(),

                html.Label('Video Stream', style={'color': 'Black', 'font-size': 35}),
                html.Div([
                    dcc.Dropdown(['True', 'False'], 'True', id='in_app_video_stream',style={'width': '600px', 'font-size': 25}),
                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                html.Br(),

                html.Label('Profinet', style={'color': 'Black', 'font-size': 35}),
                html.Div([
                    dcc.Dropdown(['True', 'False'], 'True', id='in_app_profinet',style={'width': '600px', 'font-size': 25}),
                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                html.Br(),

                html.Div(children=[

                    html.Button(id='button_start', n_clicks=0, children='Start!',
                                style={'font-size': '55px', 'width': '200px', 'display': 'inline-block',
                                       'margin-bottom': '10px',
                                       'margin-right': '5px', 'height': '100px', 'verticalAlign': 'top',
                                       'color': 'rgb(255,215,0)',
                                       'background-color': 'rgb(0,0,0)'}),

                ], style={'padding': 10, 'flex': 1}),

            ], style={'padding': 10, 'flex': 1}),

        ], style={'display': 'flex', 'flex-direction': 'row'})

    ], style={'padding': 10, 'flex': 1, 'width': '10%',"border-left":"2px black solid"}),

    dbc.Modal(
        [
            html.Div(children=[

                # Row 1: Title of UI
                dbc.Row(
                    dbc.Col(
                        html.Div([
                            html.Label('Golden Unit Monitoring', style={'color': 'Black', 'font-size': 75}),
                        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

                        width={"size": 6, "offset": 3},
                    )
                ),

                # Row 2: Base stats
                dbc.Row(
                    html.Div(children=[
                        # Row 2.1: Title
                        dbc.Row(
                            dbc.Col(
                                html.Div([
                                    html.Label('Baseline statistics', style={'color': 'Black', 'font-size': 35}),
                                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                          'justify-content': 'center'}),
                                width={"size": 6, "offset": 3},
                            )
                        ),

                        # Row 2.2: Graphs
                        dbc.Row(
                            [
                                dbc.Col(
                                    [

                                        #html.Div([
                                          #  html.Label('TCP Throughput (Mbps)', style={'color': 'Black', 'font-size': 20}),
                                      #  ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                               #   'justify-content': 'center'}),

                                        html.Div([
                                            dcc.Graph(id="fig_thru_tcp", style={}),
                                        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                  'justify-content': 'center'}),

                                    ]
                                ,width=2,style={'margin-right': '0px', 'margin-left': '200px'}),

                                dbc.Col(
                                    [

                                        #html.Div([
                                        #    html.Label('UDP Throughput (Mbps)', style={'color': 'Black', 'font-size': 20}),
                                        #], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                          #        'justify-content': 'center'}),

                                        html.Div([
                                            dcc.Graph(id="fig_thru_udp", style={}),
                                        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                  'justify-content': 'center'}),
                                    ]
                                ,width=2,style={'margin-right': '0px', 'margin-left': '400px'}),

                                dbc.Col(
                                    [

                                        #html.Div([
                                        #    html.Label('Latency (msec)', style={'color': 'Black', 'font-size': 20}),
                                       # ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                        #          'justify-content': 'center'}),

                                        html.Div([
                                            dcc.Graph(id="fig_delay", style={}),
                                        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                  'justify-content': 'center'}),

                                    ]
                                ,width=2,style={'margin-right': '0px', 'margin-left': '400px'}),
                            ]
                        ),
                    ], style={}),
                ),

                # Row 3: App stats and log/buttons
                dbc.Row(
                    [
                        # Left col-> app stats
                        dbc.Col(
                            html.Div(children=[
                                # Row Title
                                dbc.Row(
                                    dbc.Col(
                                        html.Div([
                                            html.Label('Application-specific statistics', style={'color': 'Black', 'font-size': 35}),
                                        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                  'justify-content': 'center'}),
                                        width={"size": 6, "offset": 3},
                                    )
                                ),

                                # Row 2.2: Graphs
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [

                                                #html.Div([
                                                #    html.Label('Throughput (Mbps)',
                                                #               style={'color': 'Black', 'font-size': 20}),
                                               # ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                 #         'justify-content': 'center'}),

                                                html.Div([
                                                    dcc.Graph(id="fig_app_thru", style={}),
                                                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                          'justify-content': 'center'}),

                                            ]
                                            , width=1, style={'margin-right': '0px', 'margin-left': '300px'}
                                        ),

                                        dbc.Col(
                                            [

                                                #html.Div([
                                                #    html.Label('RTT (msec)',
                                                #               style={'color': 'Black', 'font-size': 20}),
                                                #], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                #          'justify-content': 'center'}),

                                                html.Div([
                                                    dcc.Graph(id="fig_app_delay", style={}),
                                                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                          'justify-content': 'center'}),

                                            ]
                                            , width=1, style={'margin-right': '0px', 'margin-left': '600px'}
                                        ),
                                    ]
                                )
                            ], style={}),
                        ),
                        # Right col-> misc
                        dbc.Col(
                            html.Div(children=[

                                dbc.Row(
                                    dbc.Col(
                                        html.Div([
                                            html.Label('Event log',
                                                       style={'color': 'Black', 'font-size': 35}),
                                        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                                  'justify-content': 'center'}),
                                        width={"size": 6, "offset": 3},
                                    )
                                ),

                                html.Div([
                                    dash_table.DataTable(id='table_news',
                                                         style_data={'whiteSpace': 'normal',
                                                                     'backgroundColor': 'rgb(255,215,0)',
                                                                     'color': 'black'},
                                                         style_header={'backgroundColor': 'black', 'color': 'white'},
                                                         fill_width=True,
                                                         css=[{
                                                             'selector': '.dash-spreadsheet td div',
                                                             'rule': '''
                                                                line-height: 15px;
                                                                max-height: 30px; min-height: 30px; height: 30px;
                                                                display: block;
                                                                overflow-y: hidden;
                                                                '''
                                                         }],
                                                         style_cell={'textAlign': 'left',
                                                                     'minWidth': '500px',
                                                                     'width': '500px',
                                                                     'maxWidth': '500px'},
                                                         style_cell_conditional=[
                                                             {'if': {'column_id': 'time'},
                                                              'textAlign': 'left',
                                                              'minWidth': '150px',
                                                              'width': '150px',
                                                              'maxWidth': '150px'},
                                                             {'if': {'column_id': 'description'},
                                                              'textAlign': 'left',
                                                              'minWidth': '500px',
                                                              'width': '500px',
                                                              'maxWidth': '500px'},
                                                         ]
                                                         ),
                                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center','justify-content': 'center'}),

                                dcc.Interval(
                                    id='interval1',
                                    interval=1 * 1000,  # in milliseconds
                                    n_intervals=0
                                ),

                                html.Br(),

                                # Button
                                html.Div([
                                    html.Button(id='button_save_base', n_clicks=0, children='Save base stats',
                                                style={'font-size': '25px', 'width': '300px', 'display': 'inline-block',
                                                       'margin-bottom': '10px', 'margin-right': '5px', 'height': '60px',
                                                       'verticalAlign': 'top', 'color': 'rgb(255,215,0)',
                                                       'background-color': 'rgb(100,100,100)'}),
                                    dcc.Download(id="download_save_base"),
                                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                          'justify-content': 'center'}),

                                html.Div([
                                    html.Button(id='button_save_apps', n_clicks=0, children='Save app stats',
                                                style={'font-size': '25px', 'width': '300px', 'display': 'inline-block',
                                                       'margin-bottom': '10px', 'margin-right': '5px', 'height': '60px',
                                                       'verticalAlign': 'top', 'color': 'rgb(255,215,0)',
                                                       'background-color': 'rgb(100,100,100)'}),
                                    dcc.Download(id="download_save_apps"),
                                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center',
                                          'justify-content': 'center'}),

                                # Button
                                html.Div([
                                    html.Button(id='button_exit', n_clicks=0, children='Exit',
                                                style={'font-size': '25px', 'width': '300px', 'display': 'inline-block',
                                                       'margin-bottom': '10px', 'margin-right': '5px', 'height': '60px',
                                                       'verticalAlign': 'top', 'color': 'rgb(255,215,0)',
                                                       'background-color': 'rgb(0,0,0)'}),
                                ], style={'width': '100%', 'display': 'flex', 'align-items': 'center','justify-content': 'center'}),


                            ], style={}),width={"size": 4, "order": "1", "offset": 0},


                        ),
                    ]
                ),

            ], style={'text-align': 'left','backgroundColor':'rgb(255,215,0)'})

        ],
        id="modal-fs",
        fullscreen=True,
        size="xl",
        backdrop="static",
        keyboard=False,
        centered=False
        #style={'height':'1200px','width':'3500px','text-align': 'left','align_content':'left'}
    )

], style={'display': 'flex', 'flex-direction': 'row'})
], style={'text-align': 'center','backgroundColor':'rgb(255,215,0)'})

@callback(
    Output('hidden-div', 'children'),
    #Output('modal-fs', 'is_open'),
    Input('button_start', 'n_clicks'),

    State('in_set_client_ip', 'value'),
    State('in_set_server_ip', 'value'),
    State('in_set_num_packets', 'value'),
    State('in_set_exp_duration', 'value'),
    State('in_set_ping_interval', 'value'),
    State('in_set_ping_packs', 'value'),

    State('in_meas_campaign_name', 'value'),
    State('in_meas_exps', 'value'),
    State('in_meas_repet', 'value'),
    State('in_meas_gap', 'value'),

    State('in_app_base', 'value'),
    State('in_app_mqtt', 'value'),
    State('in_app_video_stream', 'value'),
    State('in_app_profinet', 'value')
)
def update_output(button_start,
in_set_client_ip,
in_set_server_ip,
in_set_num_packets,
in_set_exp_duration,
in_set_ping_interval,
in_set_ping_packs,
in_meas_campaign_name,
in_meas_exps,
in_meas_repet,
in_meas_gap,
in_app_base,
in_app_mqtt,
in_app_video_stream,
in_app_profinet
):
    mydict={
        'in_set_client_ip':[in_set_client_ip],
        'in_set_server_ip': [in_set_server_ip],
        'in_set_num_packets': [in_set_num_packets],
        'in_set_exp_duration': [in_set_exp_duration],
        'in_set_ping_interval': [in_set_ping_interval],
        'in_set_ping_packs': [in_set_ping_packs],
        'in_meas_campaign_name': [in_meas_campaign_name],
        'in_meas_exps': [in_meas_exps],
        'in_meas_repet': [in_meas_repet],
        'in_meas_gap': [in_meas_gap],
        'in_app_base': [in_app_base],
        'in_app_mqtt': [in_app_mqtt],
        'in_app_video_stream': [in_app_video_stream],
        'in_app_profinet': [in_app_profinet],
    }

    mydf=pd.DataFrame(mydict)
    helper.clean_db(loc=gparams._DB_FILE_LOC_INPUT_USER)
    res=helper.write_df2db(loc=gparams._DB_FILE_LOC_INPUT_USER,df=mydf,header=True)
    if res is not None:
        print('(DEBUG) DB: Updated db according to new user input - Success')
    else:
        return None

@app.callback(
    Output("modal-fs", "is_open"),
    Input("button_start", "n_clicks"),
    Input("button_exit", "n_clicks"),
    State("modal-fs", "is_open"),
)
def toggle_modal(button_start, button_exit, is_open):
    if button_start or button_exit:
        return not is_open
    return is_open

@callback(
    Output("download_save_base", "data"),
    Input("button_save_base", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    df=helper.read_db_df(gparams._DB_FILE_LOC_OUTPUT_BASE)
    return dcc.send_data_frame(df.to_csv, "base_stats.csv", index=False)

@callback(
    Output("download_save_apps", "data"),
    Input("button_save_apps", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    df=helper.read_db_df(gparams._DB_FILE_LOC_OUTPUT_APP)
    return dcc.send_data_frame(df.to_csv, "app_stats.csv", index=False)

@callback(
    Output('fig_thru_tcp', 'figure'),
    Output('fig_thru_udp', 'figure'),
    Output('fig_delay', 'figure'),
    Output('fig_app_thru', 'figure'),
    Output('fig_app_delay', 'figure'),
    Output('table_news', 'data'),
    Input('interval1', 'n_intervals'),
)
def update_graph_live(n_intervals):
    df_out_base=helper.read_db_df(loc=gparams._DB_FILE_LOC_OUTPUT_BASE)

    df_out_base['TCP Uplink (Mbps)'] = df_out_base['iperf_tcp_ul_sent_bps']  * (1e-6)
    df_out_base['TCP Downlink (Mbps)'] = df_out_base['iperf_tcp_dl_received_bps'] * (1e-6)

    fig_my_thru_tcp = px.area(df_out_base, x="timestamp", y=['TCP Uplink (Mbps)','TCP Downlink (Mbps)'],markers=False)

    fig_my_thru_tcp.update_xaxes(
        #title_text="Time",
        #title_font={"size": 30,'color':'black'},
        #title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor = 'black',
        color='black',
        linewidth = 3,
        linecolor='black',
        zerolinecolor='black'
    )

    fig_my_thru_tcp.update_yaxes(
        #title_text="Training loss",
        #title_font={"size": 30,'color':'black'},
        #title_standoff=25,
        tickfont={"size": 18,'color':'black'},
        gridcolor = 'black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black',
        visible=True,
        showticklabels=True
    )

    fig_my_thru_tcp.update_layout(
        yaxis_title='TCP Throughput (Mbps)',
        xaxis_title='Timestamp',
        width=500,
        height=250,
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        plot_bgcolor='rgb(255,215,0)',
        paper_bgcolor='rgb(255,215,0)',
        #title={'text':'Global convergence (training loss) w.r.t. time','font':{'color':'black','size':25}}
    )

    fig_my_thru_tcp.update_traces(
        stackgroup=None, fill='tozeroy'
        #marker_size=20,
        #marker_symbol='x',
        #marker_color='black'
    )

    ######### Fig 2 UDP ###########

    df_out_base['UDP Uplink (Mbps)'] = df_out_base['iperf_udp_ul_bps']  * (1e-6)
    df_out_base['UDP Downlink (Mbps)'] = df_out_base['iperf_udp_dl_bps'] * (1e-6)

    fig_my_thru_udp = px.area(df_out_base, x="timestamp", y=['UDP Uplink (Mbps)','UDP Downlink (Mbps)'],markers=False)

    fig_my_thru_udp.update_xaxes(
        #title_text="Time",
        #title_font={"size": 30,'color':'black'},
        #title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor = 'black',
        color='black',
        linewidth = 3,
        linecolor='black',
        zerolinecolor='black'
    )

    fig_my_thru_udp.update_yaxes(
        #title_text="Training loss",
        #title_font={"size": 30,'color':'black'},
        #title_standoff=25,
        tickfont={"size": 18,'color':'black'},
        gridcolor = 'black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black',
        visible=True,
        showticklabels=True
    )

    fig_my_thru_udp.update_layout(
        yaxis_title='UDP Throughput (Mbps)',
        xaxis_title='Timestamp',
        width=500,
        height=250,
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        plot_bgcolor='rgb(255,215,0)',
        paper_bgcolor='rgb(255,215,0)',
        #title={'text':'Global convergence (training loss) w.r.t. time','font':{'color':'black','size':25}}
    )

    fig_my_thru_udp.update_traces(
        stackgroup=None, fill='tozeroy'
        #marker_size=20,
        #marker_symbol='x',
        #marker_color='black'
    )

    ############## Fig 3 Delay #########

    df_out_base['RTT (msec)'] = df_out_base['ping_rtt_avg']
    df_out_base['Jitter (msec)'] = df_out_base['ping_jitter']

    fig_my_delay = px.area(df_out_base, x="timestamp", y=['RTT (msec)', 'Jitter (msec)'], markers=False)

    fig_my_delay.update_xaxes(
        # title_text="Time",
        # title_font={"size": 30,'color':'black'},
        # title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor='black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black'
    )

    fig_my_delay.update_yaxes(
        # title_text="Training loss",
        # title_font={"size": 30,'color':'black'},
        # title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor='black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black',
        visible=True,
        showticklabels=True
    )

    fig_my_delay.update_layout(
        yaxis_title='Latency',
        xaxis_title='Timestamp',
        width=500,
        height=250,
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        plot_bgcolor='rgb(255,215,0)',
        paper_bgcolor='rgb(255,215,0)',
        # title={'text':'Global convergence (training loss) w.r.t. time','font':{'color':'black','size':25}}
    )

    fig_my_delay.update_traces(
        stackgroup=None, fill='tozeroy'
        # marker_size=20,
        # marker_symbol='x',
        # marker_color='black'
    )


    ############## Fig 4 app thru #########
    df_out_app=helper.read_db_df(loc=gparams._DB_FILE_LOC_OUTPUT_APP)

    df_out_app['Throughput (Mbps)'] = df_out_app['throughput_bps'] * (1e-6)
    df_out_app['RTT (msec)'] = df_out_app['mean_rtt']
    # get all apps (filter)
    list_of_apps=df_out_app['app'].unique()

    # plot the data
    fig_my_app_thru = go.Figure()
    fig_my_app_delay=go.Figure()


    for app in list_of_apps:
        app_df=df_out_app.loc[df_out_app['app'] == app]

        fig_my_app_thru = fig_my_app_thru.add_trace(go.Scatter(x=app_df["timestamp"],
                                       y=app_df["Throughput (Mbps)"],
                                       name=app))
        fig_my_app_delay = fig_my_app_delay.add_trace(go.Scatter(x=app_df["timestamp"],
                                       y=app_df["RTT (msec)"],
                                       name=app))

    fig_my_app_thru.update_xaxes(
        # title_text="Time",
        # title_font={"size": 30,'color':'black'},
        # title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor='black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black'
    )

    fig_my_app_thru.update_yaxes(
        # title_text="Training loss",
        # title_font={"size": 30,'color':'black'},
        # title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor='black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black',
        visible=True,
        showticklabels=True
    )

    fig_my_app_thru.update_layout(
        yaxis_title='Throughput (Mbps)',
        xaxis_title='Timestamp',
        width=500,
        height=250,
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        plot_bgcolor='rgb(255,215,0)',
        paper_bgcolor='rgb(255,215,0)',
        # title={'text':'Global convergence (training loss) w.r.t. time','font':{'color':'black','size':25}}
    )

    # fig_my_delay.update_traces(
        # stackgroup=None, fill='tozeroy'
        # marker_size=20,
        # marker_symbol='x',
        # marker_color='black'
    # )


    fig_my_app_delay.update_xaxes(
        # title_text="Time",
        # title_font={"size": 30,'color':'black'},
        # title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor='black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black'
    )

    fig_my_app_delay.update_yaxes(
        # title_text="Training loss",
        # title_font={"size": 30,'color':'black'},
        # title_standoff=25,
        tickfont={"size": 18, 'color': 'black'},
        gridcolor='black',
        color='black',
        linewidth=3,
        linecolor='black',
        zerolinecolor='black',
        visible=True,
        showticklabels=True
    )

    fig_my_app_delay.update_layout(
        yaxis_title='RTT (msec)',
        xaxis_title='Timestamp',
        width=500,
        height=250,
        margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
        plot_bgcolor='rgb(255,215,0)',
        paper_bgcolor='rgb(255,215,0)',
        # title={'text':'Global convergence (training loss) w.r.t. time','font':{'color':'black','size':25}}
    )

    mydf_news=helper.read_db_df(loc=gparams._DB_FILE_LOC_OUTPUT_LOG)
    # remove repeated entries hack
    #mydf_news = mydf_news.drop_duplicates(subset='description', keep="first")
    #mydf_news['time'] = pd.to_datetime(mydf_news['time'])
    #curr_df = mydf_news.loc[mydf_news['time'] < helper.get_curr_time()]
    mydf_news = mydf_news.tail(6)
    output_news=mydf_news.to_dict('records')

    return fig_my_thru_tcp,fig_my_thru_udp,fig_my_delay,fig_my_app_thru,fig_my_app_delay,output_news


if __name__ == '__main__':
    print('(Frontend) DBG: Frontend initialized')
    helper=Helper()
    app.run_server(host='0.0.0.0')
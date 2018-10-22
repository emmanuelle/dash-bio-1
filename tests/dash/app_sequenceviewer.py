import base64

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_bio
from dash_bio.helpers import proteinReader as pr

proteinFolder = 'proteins'
sequence = '-'

highlightColor = 'blue'

selection = [10, 20, highlightColor]


def layout():
    return(
            html.Div([

                html.Div(
                    id='header',
                    children=[
                        "Dash sequence viewer",


                    ]
                ),
                html.Div(
                    id='fasta-upload',
                    children=[
                        dcc.Upload(
                            id='upload-fasta-data',
                            children=html.Div([
                                "Drag and Drop or ",
                                html.A("Select file")
                            ]),
                            style={
                                'width': '100%',
                                'height': '50px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                            }
                        ),
                        html.Div(
                            id='upload-data-output'
                        )
                    ]
                ),

                html.Div(
                    id='sequence-viewer-container',
                    children=[
                        dash_bio.SequenceViewerComponent(
                            id='sequence-viewer',
                            title="",
                            wrapAminoAcids=True,
                            search=True,
                            sequence='-',
                            selection=[]
                        )
                    ]
                ),

                html.Div(
                    id='controls-container',
                    children=[

                        dcc.RadioItems(
                            id='selection-or-coverage',
                            options=[
                                {'label': 'Enable selection', 'value': 'sel'},
                                {'label': 'Enable coverage', 'value': 'cov'}
                            ],
                            value='sel'
                        ),

                        html.Div(
                            id='sel-slider-container',
                            children=[
                                "Selection slider",
                                dcc.RangeSlider(
                                    id='sel-slider',
                                    min=0,
                                    max=len(sequence),
                                    step=1,
                                    value=[10, 20]
                                ),
                            ]
                        ),

                        html.Div(
                            id='protein-dropdown-container',
                            children=[
                                "Protein to view",
                                dcc.Dropdown(
                                    id='protein-dropdown',
                                    options=[
                                        {'label': 1, 'value': 0}
                                    ],
                                    value=0
                                )
                            ]
                        )
                    ]
                ),

                html.Div(
                    id='info-container',
                    children=[
                        html.Span(
                            "Description: ",
                            style={
                                'font-weight': 'bold'
                            }
                        ),
                        html.Div(
                            id='desc-info'
                        ),
                        html.Br(),

                        html.Span(
                            "Selection information: ",
                            style={
                                'font-weight': 'bold'
                            }
                        ),
                        html.Div(
                            id='test-selection'
                        ),
                        html.Br(),

                        html.Span(
                            "Coverage info: ",
                            style={
                                'font-weight': 'bold'
                            }
                        ),
                        html.Div(
                            id='test-coverage'
                        ),
                        html.Br(),

                        html.Span(
                            "Mouse sel: ",
                            style={
                                'font-weight': 'bold'
                            }
                        ),
                        html.Div(
                            id='test-mouse-selection'
                        ),
                        html.Br(),

                        html.Span(
                            "Subpart sel: ",
                            style={
                                'font-weight': 'bold'
                            }
                        ),
                        html.Div(
                            id='test-subpart-selection'
                        )
                    ]
                )
            ])
    )


def callbacks(app):
    # sequence viewer display
    @app.callback(
        Output('sequence-viewer-container', 'children'),
        [Input('upload-fasta-data', 'contents'),
         Input('protein-dropdown', 'value')]
    )
    def update_sequence(upload_contents, p):
        data = ''
        try:
            content_type, content_string = upload_contents.split(',')
            data = base64.b64decode(content_string).decode('UTF-8')
        except AttributeError:
            pass
        if data == '':
            return [
                dash_bio.SequenceViewerComponent(
                    id='sequence-viewer',
                    title='',
                    wrapAminoAcids=True,
                    search=True,
                    sequence='-',
                    selection=[]
                )
            ]
        protein = pr.readFasta(dataString=data)[p]
        sequence = protein['sequence']
        try:
            title = protein['description']['accession']
        except KeyError:
            title = ''

        return [
            dash_bio.SequenceViewerComponent(
                id='sequence-viewer',
                title=title,
                wrapAminoAcids=True,
                search=True,
                sequence=sequence,
                selection=[]
            )
        ]

    # controls
    @app.callback(
        Output('sel-slider', 'disabled'),
        [Input('selection-or-coverage', 'value')]
    )
    def enable_disable_slider(v):
        if(v == 'sel'):
            return False
        return True

    @app.callback(
        Output('sequence-viewer', 'selection'),
        [Input('sel-slider', 'value'),
         Input('selection-or-coverage', 'value')]
    )
    def update_sel(v, v2):
        if(v2 != 'sel'):
            return []
        return [v[0], v[1], highlightColor]

    @app.callback(
        Output('protein-dropdown', 'options'),
        [Input('upload-fasta-data', 'contents')]
    )
    def update_protein_options(upload_contents):
        dropdownOptions = [
            {'label': 1, 'value': 0}
        ]
        data = ''
        try:
            content_type, content_string = upload_contents.split(',')
            data = base64.b64decode(content_string).decode('UTF-8')
        except AttributeError:
            pass
        proteins = pr.readFasta(dataString=data)
        if(type(proteins) is list):
            dropdownOptions = []
            for i in range(len(proteins)):
                dropdownOptions.append(dict(
                    label=i+1,
                    value=i
                ))
        return dropdownOptions

    @app.callback(
        Output('sel-slider-container', 'children'),
        [Input('sequence-viewer', 'sequence')]
    )
    def update_slider_values(seq):
        return[
            "Selection slider",
            dcc.RangeSlider(
                id='sel-slider',
                min=0,
                max=len(seq),
                step=1,
                value=[0, 0]
            )
        ]

    # info display
    @app.callback(
        Output('test-selection', 'children'),
        [Input('sequence-viewer', 'selection')],
        state=[State('sequence-viewer', 'sequence')]
    )
    def get_aa_comp(v, seq):
        if(len(v) < 2):
            return ''

        subsequence = seq[v[0]:v[1]]
        aminoAcids = list(set(subsequence))
        summary = []
        for aa in aminoAcids:
            summary.append(
                html.Tr([html.Td(pr.translateSeq(aa)[0]),
                         html.Td(str(subsequence.count(aa)))])
            )
        return html.Table(summary)

    @app.callback(
        Output('test-mouse-selection', 'children'),
        [Input('sequence-viewer', 'mouseSelection')]
    )
    def update_mouse_sel(v):
        print(v)
        return v

    @app.callback(
        Output('desc-info', 'children'),
        [Input('upload-fasta-data', 'contents'),
         Input('protein-dropdown', 'value')],
    )
    def update_desc_info(upload_contents, p):
        data = ''

        try:
            content_type, content_string = upload_contents.split(',')
            data = base64.b64decode(content_string).decode('UTF-8')
        except AttributeError:
            pass
        if data == '':
            return []

        protein = pr.readFasta(dataString=data)[p]
        desc = []
        for key in protein['description']:
            tmp = key
            tmp += ': '
            tmp += protein['description'][key]
            desc.append(tmp)
            desc.append(html.Br())
        return desc

    @app.callback(
        Output('test-subpart-selection', 'children'),
        [Input('sequence-viewer', 'subpartSelected')]
    )
    def update_subpart_sel(v):
        if(v is None):
            return ''
        test = []
        for sel in v:
            test.append("Start: %d " % sel['start'])
            test.append("End: %d " % sel['end'])
            test.append("Sequence: %s" % sel['sequence'])
            test.append(html.Br())
        return test



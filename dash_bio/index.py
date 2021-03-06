# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class index(Component):
    """A index component.
The OncoPrint component is used to view multile genetic alteration events
through an interactive and zoomable heatmap. It is a React/Dash port of the
popular oncoPrint() function from the BioConductor R package.
Under the hood, the rending is done using Plotly.js built upon D3.
Plotly's interactivity allows the user to bind clicks and hovers to genetic
events, allowing the user to create complex bioinformatic apps or workflows
that rely on crossfiltering.
Read more about the component here:
https://github.com/plotly/react-oncoprint

Keyword arguments:
- data (list; optional): Input data, in CBioPortal format where each list entry is a dict
consisting of 'sample', 'gene', 'alteration', and 'type'
- padding (number; optional): Adjusts the padding (amount of whitespace) between two tracks.
Value is a ratio between 0 and 1.
Default of 0.05 or 5%. If set to 0 plot will look like a heatmap.
- colorscale (boolean | dict; optional): If not null, will override the default OncoPrint colorscale.
Default OncoPrint colorscale same as CBioPortal implementation.
Make your own colrscale as a {'mutation': COLOR} dict.
Supported mutation keys in ['MISSENSE, 'INFRAME', 'FUSION',
'AMP', 'GAIN', 'HETLOSS', 'HMODEL', 'UP', 'DOWN']
Note that this is NOT a standard plotly colorscale.
- backgroundcolor (string; optional): Default color for the tracks, in common name, hex, rgb or rgba format.
If left blank, will default to a light grey rgb(190, 190, 190).
- range (list; optional): .Toogles whether or not to show a legend on the right side of the plot,
with mutation information.
- showlegend (boolean; optional): .Toogles whether or not to show a legend on the right side of the plot,
with mutation information.
- showoverview (boolean; optional): .Toogles whether or not to show a heatmap overview of the tracks.
- width (number | string; optional): Width of the OncoPrint.
Will disable auto-resizing of plots if set.
- height (number | string; optional): Width of the OncoPrint.
Will disable auto-resizing of plots if set.

Available events: """
    @_explicitize_args
    def __init__(self, data=Component.UNDEFINED, padding=Component.UNDEFINED, colorscale=Component.UNDEFINED, backgroundcolor=Component.UNDEFINED, range=Component.UNDEFINED, showlegend=Component.UNDEFINED, showoverview=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, **kwargs):
        self._prop_names = ['data', 'padding', 'colorscale', 'backgroundcolor', 'range', 'showlegend', 'showoverview', 'width', 'height']
        self._type = 'index'
        self._namespace = 'dash_bio'
        self._valid_wildcard_attributes =            []
        self.available_events = []
        self.available_properties = ['data', 'padding', 'colorscale', 'backgroundcolor', 'range', 'showlegend', 'showoverview', 'width', 'height']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(index, self).__init__(**args)

    def __repr__(self):
        if(any(getattr(self, c, None) is not None
               for c in self._prop_names
               if c is not self._prop_names[0])
           or any(getattr(self, c, None) is not None
                  for c in self.__dict__.keys()
                  if any(c.startswith(wc_attr)
                  for wc_attr in self._valid_wildcard_attributes))):
            props_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self._prop_names
                                      if getattr(self, c, None) is not None])
            wilds_string = ', '.join([c+'='+repr(getattr(self, c, None))
                                      for c in self.__dict__.keys()
                                      if any([c.startswith(wc_attr)
                                      for wc_attr in
                                      self._valid_wildcard_attributes])])
            return ('index(' + props_string +
                   (', ' + wilds_string if wilds_string != '' else '') + ')')
        else:
            return (
                'index(' +
                repr(getattr(self, self._prop_names[0], None)) + ')')

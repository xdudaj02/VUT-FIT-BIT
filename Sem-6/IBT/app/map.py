"""
This file handles creation of more or less blind maps.

file:   map.py
author: Jakub Duda, xdudaj02
date:   8. 5. 2022
"""

import mapnik
import cairo
from pyproj import Transformer

import math
import re
import json

import layers
import map_util


def check_style_file(style_dict):
    """Checks validity of style set definition.

    :param style_dict: Style set definition to be checked.
    :return: True if valid, False otherwise.
    """
    for key, value in style_dict.items():
        # check element group validity
        if key not in layers.options:
            return False
        # check validity of list values
        if type(layers.options[key]) is list and type(value) is list:
            for i in value:
                if i not in layers.options[key]:
                    return False
        # check validity of string value
        elif type(layers.options[key]) is list and type(value) is str:
            if value not in layers.options[key]:
                return False
        # check validity of integer value
        elif type(layers.options[key]) is int and type(value) is str:
            try:
                if (int(value) - 1) not in range(layers.options[key]):
                    return False
            except ValueError:
                return False
        else:
            return False
    return True


def parse_style_file(style_dict):
    """Parses given style set definition. Removes element groups from unselected layers. Populates settings for each
    type of concerned elements.

    :param style_dict: Style set definition.
    :return: Parsed style set definition.
    """
    # remove element groups that are from unselected layers
    if 'layer' not in style_dict:
        return {}
    for layer in layers.options['layer']:
        if layer not in style_dict:
            for item in style_dict.keys():
                if re.match('^' + item + '_', item):
                    style_dict.pop(item, None)

    style_dict.pop('layer', None)
    style_dict.pop('surface_color', None)

    # remove element groups that are not set to be drawn
    for key, value in list(style_dict.items()):
        if int(value) < 2:
            style_dict.pop(key, None)
        else:
            style_dict[key] = int(value)

    # populate settings
    # railway tunnel
    rw_name = ['rail_normal', 'rail_special', 'rail_tram']
    rw_options = ['rail_normal', 'rail_special', 'rail_tram', 'rail_subway', 'rail_disused']
    if 'rail_tunnels' in style_dict and style_dict['rail_tunnels'] > 1:
        for x in rw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_tunnel'] = style_dict[x]
                if x in rw_name and style_dict['rail_tunnels'] > 2:
                    style_dict[x + '_tunnel_name'] = style_dict['rail_tunnels'] - 3
    style_dict.pop('rail_tunnels', None)

    # railway bridge
    rw_options = ['rail_normal', 'rail_special', 'rail_tram', 'rail_subway', 'rail_disused', 'rail_construction']
    if 'rail_bridges' in style_dict and style_dict['rail_bridges'] > 1:
        for x in rw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_bridge'] = style_dict[x]
                if x in rw_name and style_dict['rail_bridges'] > 2:
                    style_dict[x + '_bridge_name'] = style_dict['rail_bridges'] - 3
    style_dict.pop('rail_bridges', None)

    # highway junction
    hw_name = ['roads_motorway', 'roads_primary', 'roads_secondary', 'roads_tertiary']
    hw_options = ['roads_motorway']
    if 'roads_junction' in style_dict and style_dict['roads_junction'] > 1:
        for x in hw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_junction'] = 2

    # highway link
    hw_options = ['roads_motorway', 'roads_primary', 'roads_secondary', 'roads_tertiary']
    if 'roads_link' in style_dict and style_dict['roads_link'] > 1:
        for x in hw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_link'] = style_dict[x]
    style_dict.pop('roads_link', None)

    # highway name
    hw_options = ['roads_motorway', 'roads_primary', 'roads_secondary', 'roads_tertiary', 'roads_residential',
                  'roads_service']
    if 'roads_names' in style_dict and style_dict['roads_names'] > 1:
        for x in hw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_name'] = 2
    style_dict.pop('roads_names', None)

    # highway oneway
    hw_options = ['roads_motorway', 'roads_primary', 'roads_secondary', 'roads_tertiary', 'roads_residential',
                  'roads_service', 'roads_path', 'roads_motorway_link', 'roads_primary_link',
                  'roads_secondary_link', 'roads_tertiary_link']
    if 'roads_signs' in style_dict and style_dict['roads_signs'] > 1:
        for x in hw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_oneway'] = 2

    # highway construction
    hw_options = ['roads_motorway', 'roads_primary', 'roads_secondary', 'roads_tertiary', 'roads_residential',
                  'roads_service', 'roads_motorway_link', 'roads_primary_link',
                  'roads_secondary_link', 'roads_tertiary_link']
    if 'roads_construction' in style_dict and style_dict['roads_construction'] > 1:
        for x in hw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_const'] = style_dict[x]
    style_dict.pop('roads_construction', None)

    # highway tunnel
    if 'roads_tunnels' in style_dict and style_dict['roads_tunnels'] > 1:
        for x in hw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_tunnel'] = style_dict[x]
                if x in hw_name and style_dict['roads_tunnels'] > 2:
                    style_dict[x + '_tunnel_name'] = style_dict['roads_tunnels'] - 3
    style_dict.pop('roads_tunnels', None)

    # highway bridge
    hw_options = ['roads_motorway', 'roads_primary', 'roads_secondary', 'roads_tertiary', 'roads_residential',
                  'roads_service', 'roads_path', 'roads_pavement', 'roads_motorway_link', 'roads_primary_link',
                  'roads_secondary_link', 'roads_tertiary_link', 'roads_motorway_const', 'roads_primary_const',
                  'roads_secondary_const', 'roads_tertiary_const', 'roads_residential_const',
                  'roads_service_const', 'roads_path_const', 'roads_pavement_const', 'roads_motorway_link_const',
                  'roads_primary_link_const', 'roads_secondary_link_const', 'roads_tertiary_link_const']
    if 'roads_bridges' in style_dict and style_dict['roads_bridges'] > 1:
        for x in hw_options:
            if x in style_dict and style_dict[x] > 1:
                style_dict[x + '_bridge'] = style_dict[x]
                if x in hw_name and style_dict['roads_bridges'] > 2:
                    style_dict[x + '_bridge_name'] = style_dict['roads_bridges'] - 3
    style_dict.pop('roads_bridges', None)

    return style_dict


def get_extent(left, bottom, right, top):
    """Tries to get extent from values. Returns None if invalid parameters are used.

    :param left: Left cooridnate.
    :param bottom: Bottom cooridnate.
    :param right: Rigth cooridnate.
    :param top: Top cooridnate.
    :return: List of coordinates defining map extent.
    """
    extent = [left, bottom, right, top]
    try:
        return [float(x) for x in extent]
    except ValueError:
        return None


def get_ppi(name, custom_value):
    """Tries to get ppi based on parameters. Returns None if invalid parameters are used.

    :param name: Name of selected PPI option.
    :param custom_value: Custom PPI value if used.
    :return: Numerical representation of selected PPI.
    """
    try:
        ppi_dict = {'classic': 90.7, 'print': 300, 'custom': custom_value}
        return float(ppi_dict[name])
    except KeyError or ValueError:
        return None


def get_pixel(number, unit, ppi):
    """Tries to get pizel size based on parameters. Returns None if invalid parameters are used.

    :param number: Size value.
    :param unit: Unit of given size value.
    :param ppi: Selected value of PPI.
    :return: Size value in pixels.
    """
    if unit not in ['px', 'mm']:
        return None
    try:
        number = int(number)
    except ValueError:
        return None

    if unit == 'mm':
        # mm to px
        number *= (90.7 / 25.4) * (ppi / 90.7)
    # mapnik pixel limit
    if number > 32768:
        return None
    return number


def get_zoom_level(scale, projection):
    """Gets zoom level for given scale. Accounts for different scale values for maps with different projections.

    :param scale: Map scale.
    :param projection: Map projection.
    :return: Zoom level.
    """
    # adjust scale for Krovak
    if projection[:4] == '5514':
        scale *= 1.837684249783303  # Krovak scale to Mercator scale factor

    # get zoom level
    for i, x in enumerate(layers.zoom_level_limits):
        if scale > x:
            return i
    return len(layers.zoom_level_limits)


def adjust_to_zoom(config, map_zoom_level):
    """Adjusts given style set definition to given zoom level.

    :param config: Style set definition.
    :param map_zoom_level: Zoom level.
    :return: Adjusted style set definition.
    """
    for key, value in layers.limits.items():
        if key not in config:
            continue
        for zoom, detail in value.items():
            if zoom >= map_zoom_level:
                config[key] = str(min(int(config[key]), detail))
                break
    return config


def get_template_config(map_type, map_zoom_level=None):
    """Gets style set definition for given map type. Possibly adjusts to zoom level.

    :param map_type: Map type string.
    :param map_zoom_level: Zoom level. Defaults to None.
    :return: Style set definition.
    """
    try:
        # load style set definition from file
        with open('data/style_sets/' + map_type + '.json', 'r') as file:
            data = file.read()
            config = json.loads(data)
    except OSError:
        return None

    # if zoom level set, adjust style set definition
    if map_zoom_level is not None:
        config = adjust_to_zoom(config, map_zoom_level)
    return config


def pad_extent(extent, proj, reverse=False):
    """Pads map extent to account for rotation of Krovak projection. Uses algorithm for calculating the angle of
    krovak projection based on longitude available at
    https://cs.wikipedia.org/wiki/K%C5%99ov%C3%A1kovo_zobrazen%C3%AD#Odchylka_od_severu (6.5.2022).

    :param extent: Map extent.
    :param proj: Map projection.
    :param reverse: If true extent is shrunk else extent is extended. Defaults to false.
    :return: Padded extent.
    """
    if proj == '5514':
        left, bottom, right, top = extent

        # algorithm for calculating the angle of krovak projection based on longitude
        # source: https://cs.wikipedia.org/wiki/K%C5%99ov%C3%A1kovo_zobrazen%C3%AD#Odchylka_od_severu (6.5.2022)
        angle = (24.8333333 - extent[0]) / 1.34

        coefficient = math.sin(math.radians(angle)) / math.sin(math.radians(90))
        width = right - left
        height = top - bottom
        width_pad = height * coefficient
        height_pad = width * coefficient
        if reverse:
            extent = [left + width_pad, bottom + height_pad,
                      right - width_pad, top - height_pad]
        else:
            extent = [left - width_pad, bottom - height_pad,
                      right + width_pad, top + height_pad]

        return extent
    else:
        return extent


def get_bbox(extent, proj):
    """Gets bounding box of map in projection coordinates.

    :param extent: Map extent in WSG84 coordinates.
    :param proj: Map projection.
    :return: Map extent in projection coordinates.
    """
    # mercator
    if proj == '3857':
        return mapnik.ProjTransform(mapnik.Projection('+init=epsg:4326'),
                                    mapnik.Projection('+init=epsg:3857')).forward(mapnik.Box2d(*extent))
    # krovak
    elif proj == '5514':
        krovak_transform = Transformer.from_crs("EPSG:4326", "EPSG:5514")
        left, bottom = krovak_transform.transform(extent[1], extent[0])
        right, top = krovak_transform.transform(extent[3], extent[2])
        return mapnik.Box2d(left, bottom, right, top)
    else:
        return None


def select_layers(config, map_zoom_level):
    """Selects and orders layers that should be drawn on the map.

    :param config: Style set definition.
    :param map_zoom_level: Map zoom level.
    :return: Ordered list containing selected layers. Layers are represented using the Layer class.
    """
    hw_tunnel = 'roads_tunnels' in config and int(config['roads_tunnels']) > 1
    hw_bridge = 'roads_bridges' in config and int(config['roads_bridges']) > 1
    rw_tunnel = 'rail_tunnels' in config and int(config['rail_tunnels']) > 1
    rw_bridge = 'rail_bridges' in config and int(config['rail_bridges']) > 1

    # parse style set definition
    config = parse_style_file(config)

    selected = []
    for name, detail in config.items():
        if name not in layers.cases:
            continue

        # get layers and styles for given detail level
        layer_dict = layers.cases[name][detail - 2]

        # add each layer
        for layer_name, layer_detail in layer_dict.items():
            layer_data = layers.layers[layer_name]
            query = layer_data['query']

            # complete database query
            if 'min_area' in layer_data:
                query = layer_data['query'].format(layers.min_area_sizes[layer_data['min_area']][map_zoom_level])
            if 'hw_tunnel' in layer_data and 'hw_bridge' in layer_data:
                query = layer_data['query'].format(' and "covered" is null and "tunnel" is null' if hw_tunnel else '',
                                                   ' and "bridge" is null' if hw_bridge else '')
            if 'hw_bridge' in layer_data and 'hw_tunnel' not in layer_data:
                query = layer_data['query'].format(' and "bridge" is null' if hw_bridge else '')
            if 'rw_bridge' in layer_data and 'rw_tunnel' in layer_data:
                query = layer_data['query'].format(' and "bridge" is null' if rw_bridge else '',
                                                   ' and "covered" is null and "tunnel" is null' if rw_tunnel else '')
            if 'rw_bridge' in layer_data and 'rw_tunnel' not in layer_data:
                query = layer_data['query'].format(' and "bridge" is null' if rw_bridge else '')

            selected.append(map_util.Layer(layer_name, layer_data['order'], layer_data['styles'][layer_detail], query))

    selected.sort(key=lambda x: x.order)
    return selected


def create_layer(layer_name, style_name, query, extent):
    """Creates and returns a Layer object with given parameters. Sets up connection details for retrieving data from
    database.

    :param layer_name: Name of this layer.
    :param style_name: Name of Style element that should be used for this layer.
    :param query: Query to use for retrieving data for this layer.
    :param extent: String representation of map extent.
    :return: Created Layer object.
    """
    query += (' as ' + layer_name.replace('-', '_'))

    lyr = mapnik.Layer(layer_name)
    lyr.srs = '+init=epsg:4326'
    lyr.datasource = mapnik.PostGIS(dbname='gis', host='localhost', user='gisuser', password='gisuser', port='5432',
                                    table=query, extent=extent, srid='4326')
    lyr.styles.append(style_name)

    return lyr


def create_gpx_style(top_color):
    """Creates and returns a Style object for a user imported track.

    :param top_color: Selected color.
    :return: Created Style object.
    """
    # calculate border colour
    bottom_color = '#' + ''.join([hex(max(int(top_color[x: x + 2], 16) - 75, 0))[2:].zfill(2) for x in [1, 3, 5]])

    gpx_style = mapnik.Style()

    # line border
    bottom_rule = mapnik.Rule()
    sym = mapnik.LineSymbolizer()
    sym.stroke = mapnik.Color(bottom_color)
    sym.stroke_width = 5.0
    sym.stroke_linecap = mapnik.stroke_linecap.round
    bottom_rule.symbols.append(sym)

    # line fill
    top_rule = mapnik.Rule()
    sym = mapnik.LineSymbolizer()
    sym.stroke = mapnik.Color(top_color)
    sym.stroke_width = 3.5
    sym.stroke_linecap = mapnik.stroke_linecap.round
    top_rule.symbols.append(sym)

    gpx_style.rules.append(bottom_rule)
    gpx_style.rules.append(top_rule)
    return gpx_style


def create_gpx_layer(m, color, file):
    """Creates and returns a Layer object for a user imported track.

    :param m: Map object.
    :param color: Selected color.
    :param file: File to use as source.
    :return: Created Layer object.
    """
    # counter used for unique layer names
    try:
        create_gpx_layer.counter += 1
    except AttributeError:
        create_gpx_layer.counter = 1

    lyr = mapnik.Layer('gpx-' + str(create_gpx_layer.counter))
    lyr.srs = '+init=epsg:4326'
    lyr.datasource = mapnik.Ogr(file=file, layer='tracks')

    # create and append style
    gpx_style = create_gpx_style(color)
    m.append_style('gpx-' + str(create_gpx_layer.counter), gpx_style)
    lyr.styles.append('gpx-' + str(create_gpx_layer.counter))
    return lyr


def make_map(map_extent, map_size, map_type, map_format, gpx_data=None, custom_style_data=None, path=None,
             map_ppi=90.7, map_proj='3857'):
    """Generates a more or less blind map.

    :param map_extent: Selected map extent [List].
    :param map_size: Selected map size [List].
    :param map_type: Selected map type [String].
    :param map_format: Selected output format [String].
    :param gpx_data: List of GPX files containing user imported tracks. Defaults to None.
    :param custom_style_data: Path prefix to use for filepath of output file. Defaults to None.
    :param path: Path prefix to use for filepath of output file. Defaults to None.
    :param map_ppi: Selected PPI. Defaults to 90.7.
    :param map_proj: EPSG code of selected projection. Defaults to Mercator.
    :return: Filename of output file.
    """
    # get parameters
    padded_extent = pad_extent(map_extent, map_proj)
    bbox = get_bbox(map_extent, map_proj)

    # register fonts
    mapnik.register_fonts('data/fonts/Merriweather')

    if map_proj == '5514':
        map_proj += ' +alpha=30.28813975277778'

    # create map and zoom to desired area
    m = mapnik.Map(*map_size, '+init=epsg:' + map_proj)
    # m.maximum_extent = get_bbox(padded_extent, map_proj)
    m.aspect_fix_mode = mapnik.aspect_fix_mode.GROW_BBOX
    if not bbox:
        return None
    m.zoom_to_box(bbox)

    # get map scale and zoom level
    map_scale = m.scale()
    map_zoom_level = get_zoom_level(map_scale, map_proj)
    zoom_factor = layers.zoom_level_scale_factors[map_zoom_level]

    # get style set definition
    if map_type == 'custom':
        if not check_style_file(custom_style_data):
            return None
        style_data = custom_style_data
    else:
        style_data = get_template_config(map_type, map_zoom_level)
        if not style_data:
            return None

    # get styles
    style_file = 'data/styles/style.xml'
    with open(style_file, 'r') as file:
        style_string = file.read()

    # adjust styles
    try:
        surface_color = style_data['surface_color']
    except KeyError:
        surface_color = 'color'
    style_string = layers.adjust_style(style_string, surface_color, map_zoom_level, map_proj)

    # load styles
    mapnik.load_map_from_string(m, style_string)

    # select layers
    selected_layers = select_layers(style_data, map_zoom_level)

    # add classic layers and gpx layers
    gpx_done = bool(gpx_data is None)
    clear_cache_done = False
    extent_string = ', '.join([str(x) for x in padded_extent])
    for layer in selected_layers:
        if layer.order > 1887 and not clear_cache_done:
            lyr = mapnik.Layer('clear_cache')
            lyr.clear_label_cache = True
            m.layers.append(lyr)
        if layer.order > 1887 and not gpx_done:
            gpx_done = True
            for color, files in gpx_data:
                for file in files:
                    m.layers.append(create_gpx_layer(m, color, file))
        m.layers.append(create_layer(layer.name, layer.style, layer.query, extent_string))

    if not path:
        path = ''

    # generate output file
    scale_factor = map_ppi / 90.7 * zoom_factor
    if map_format == 'png' or map_format == 'jpg':
        im = mapnik.Image(m.width, m.height)
        mapnik.render(m, im, scale_factor)
        filename = map_util.save_raster_file(im, map_format, path=path)
    elif map_format == 'svg' or map_format == 'pdf':
        filename = map_util.generate_vector_filename(map_format, path=path)
        if map_format == 'svg':
            surface = cairo.SVGSurface(filename, *map_size)
            mapnik.render(m, surface, scale_factor, 0, 0)
            surface.finish()
        elif map_format == 'pdf':
            surface = cairo.PDFSurface(filename, *map_size)
            mapnik.render(m, surface, scale_factor, 0, 0)
            surface.finish()
    else:
        return None

    return filename

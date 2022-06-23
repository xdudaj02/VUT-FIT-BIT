"""
This file handles creation of completely blind maps.

file:   blind_map.py
author: Jakub Duda, xdudaj02
date:   8. 5. 2022
"""

import mapnik
import cairo
from pyproj import Transformer

import map_util

# dictionary with data for all layers available for blind maps
layers = {
    'country': {
        'order': 1,
        'style': 'country',
        'query': 'select way from blind_polygon where boundary=\'administrative\' and '
                 'admin_level=\'2\' {}'
    },
    'region': {
        'order': 2,
        'style': 'region',
        'query': 'select way from blind_polygon where boundary=\'administrative\' and '
                 '((admin_level=\'4\' and ref like \'SK%\') or (admin_level=\'6\' and ref not like '
                 '\'SK%\')) {}'
    },
    'district': {
        'order': 3,
        'style': 'district',
        'query': 'select way from blind_polygon where boundary=\'administrative\' and '
                 '((admin_level=\'8\' and ref like \'SK%\') or (admin_level=\'7\' and ref like \'CZ%\')) {}'
    },
    'capital': {
        'order': 10,
        'style': 'capital',
        'query': 'select way from blind_point where place=\'city\' and capital=\'yes\' {}'
    },
    'city': {
        'order': 11,
        'style': 'city',
        'query': 'select way from blind_point where place=\'city\' and (capital is null or '
                 'capital!=\'yes\') {} order by population::int desc'
    },
    'town': {
        'order': 12,
        'style': 'town',
        'query': 'select way from blind_point where place=\'town\' {} order by population::int desc'
    },
    'hydro_area': {
        'order': 9,
        'style': 'hydro_area',
        'query': 'select way from blind_polygon where "natural"=\'water\' and '
                 'ST_Area(way, true) > 1000000 {}'
    },
    'hydro_way_bottom': {
        'order': 7,
        'style': 'hydro_way_bottom',
        'query': 'select way from blind_line where waterway=\'river\' {}'
    },
    'hydro_way_top': {
        'order': 8,
        'style': 'hydro_way_top',
        'query': 'select way from blind_line where waterway=\'river\' {}'
    },
    'mountain': {
        'order': 4,
        'style': 'geomorph',
        'query': 'select way from blind_polygon where "natural"=\'mountain_range\'',
        'limit': 'dwithin {}'
    },
    'valley': {
        'order': 5,
        'style': 'geomorph',
        'query': 'select way from blind_polygon where "natural" in (\'basin\', \'plateau\', \'plain\', '
                 '\'valley\') {}'
    },
    'natpark': {
        'order': 6,
        'style': 'natpark',
        'query': 'select way from blind_polygon where (boundary=\'national_park\' or '
                 '(boundary=\'protected_area\' and protect_class=\'2\')) {}'
    },

    'region_name': {
        'order': 22,
        'style': 'region_name',
        'query': 'select way, name from blind_polygon where boundary=\'administrative\' and '
                 '((admin_level=\'4\' and ref like \'SK%\') or (admin_level=\'6\' and ref not like '
                 '\'SK%\')) {}'
    },
    'district_name': {
        'order': 21,
        'style': 'district_name',
        'query': 'select way, name from blind_polygon where boundary=\'administrative\' and '
                 '((admin_level=\'8\'and ref like \'SK%\') or (admin_level=\'7\' and ref like \'CZ%\')) {}'
    },
    'capital_name': {
        'order': 14,
        'style': 'capital_name',
        'query': 'select way, name from blind_point where place=\'city\' and capital=\'yes\' {}'
    },
    'city_name': {
        'order': 15,
        'style': 'city_name',
        'query': 'select way, name from blind_point where place=\'city\' {} and (capital is null or '
                 'capital!=\'yes\') order by population::int desc'
    },
    'town_name': {
        'order': 16,
        'style': 'town_name',
        'query': 'select way, name from blind_point where place=\'town\' {} order by '
                 'population::int desc'
    },
    'hydro_area_name': {
        'order': 17,
        'style': 'hydro_area_name',
        'query': 'select way, name from blind_polygon where "natural"=\'water\' and '
                 'ST_Area(way, true) > 1000000 {}'
    },
    'hydro_way_name': {
        'order': 18,
        'style': 'hydro_way_name',
        'query': 'select way, name from blind_line where waterway=\'river\' {}'
    },
    'mountain_name': {
        'order': 20,
        'style': 'geomorph_name',
        'query': 'select way, name from blind_polygon where "natural"=\'mountain_range\' {}'
    },
    'valley_name': {
        'order': 19,
        'style': 'geomorph_name',
        'query': 'select way, name from blind_polygon where "natural" in (\'basin\', \'plateau\', '
                 '\'plain\', \'valley\') {}'
    },
    'natpark_name': {
        'order': 13,
        'style': 'natpark_name',
        'query': 'select way, name from blind_polygon where (boundary=\'national_park\' or '
                 '(boundary=\'protected_area\' and protect_class=\'2\')) {}'
    }
}

# extent definitions for available countries
country_extents = {
    'sk': [16.788, 47.697, 22.613, 49.642],
    'cz': [12.029, 48.525, 18.962, 51.086]
}

# ids of objects in database representing available countries
country_ids = {
    'sk': -14296,
    'cz': -51684
}

# zoom factor definitions for available paper sizes
zoom_factors = {
    'a5': 0.8,
    'a4': 1,
    'a3': 1.2
}


def size_to_px(size):
    """Converts paper size name to size in pixels. Returns None for invalid parameters.

    :param size: Name of paper size.
    :return: Paper size in pixels.
    """
    size_dict = {'a3': [4960, 3508], 'a4': [3508, 2480], 'a5': [2480, 1748]}
    try:
        return size_dict[size]
    except KeyError:
        return None


def get_map_format(map_use):
    """Gets output format based on selected map use. Returns None for invalid parameters.

    :param map_use: Selected map use.
    :return: Output format extension.
    """
    if map_use == 'print':
        return 'pdf'
    elif map_use == 'digital':
        return 'png'
    else:
        return None


def get_extent(area):
    """Calculates maximum extent.

    :param area: List of selected countries. Countries are represented using abbreviations.
    :return: Combined extent of selected countries.
    """
    extent_list = [country_extents[x] for x in area]
    extent = [min([x[0] for x in extent_list]),
              min([x[1] for x in extent_list]),
              max([x[2] for x in extent_list]),
              max([x[3] for x in extent_list])]
    return extent


def complete_query(query, name, area):
    """Adds conditions for checking if element is inside selected countries to database query.

    :param query: Original query that should be completed.
    :param name: Name to use for query.
    :param area: List of selected countries. Countries are represented using abbreviations.
    :return: Completed query.
    """
    limit = ' or '.join('in_' + x + '=TRUE' for x in area)
    query = '(' + query.format(' and (' + limit + ')') + ') as ' + name
    return query


def parse_config(config_on, config_name):
    """Handles selection of all layers that should be used.

    :param config_on: List of selected elements that should be drawn on the map. Most names correspond with layer names.
    :param config_name: List of selected elements that should have their names drawn on the map.
    Most names correspond with layer names.
    :return: List of layers that should be used.
    """
    # add country layer
    config_on += ['country']
    # add layers for names of elements
    config_on += [x + '_name' for x in config_name]

    # add all layers for hydro
    if 'hydro' in config_on:
        config_on.remove('hydro')
        config_on += ['hydro_area', 'hydro_way_bottom', 'hydro_way_top']
    if 'hydro_name' in config_on:
        config_on.remove('hydro_name')
        config_on += ['hydro_area_name', 'hydro_way_name']

    # make sure city elements are also added if town elements are added
    if 'town' in config_on and 'city' not in config_on:
        config_on += ['city']
        if 'town_name' in config_on:
            config_on += ['city_name']

    # make sure capital elements are also added if city elements are added
    if 'city' in config_on:
        config_on += ['capital']
        if 'city_name' in config_on:
            config_on += ['capital_name']

    return config_on


def select_layers(config):
    """Selects and orders all layers that should be used on the map.

    :param config: List of layers that should be drawn on the map.
    :return: Sorted list of layers.
    """
    selected = []
    for layer_name in config:
        layer_data = layers[layer_name]
        selected.append(map_util.Layer(layer_name, layer_data['order'], layer_data['style'], layer_data['query']))

    selected.sort(key=lambda x: x.order)
    return selected


def create_layer(layer_name, style_name, query, area):
    """Creates and returns a Layer object with given parameters. Sets up connection details for retrieving data from
    database.

    :param layer_name: Name of this layer.
    :param style_name: Name of Style element that should be used for this layer.
    :param query: Query to use for retrieving data for this layer.
    :param area: List of selected countries.
    :return: Created Layer object.
    """
    query = complete_query(query, layer_name, area)

    lyr = mapnik.Layer(layer_name)
    lyr.srs = '+init=epsg:4326'
    lyr.datasource = mapnik.PostGIS(dbname='gis', host='localhost', user='gisuser', password='gisuser', port='5432',
                                    table=query, extent=(", ".join([str(x) for x in get_extent(area)])), srid='4326')
    lyr.styles.append(style_name)

    return lyr


def make_map(map_area, map_size, map_config_on, map_config_name, map_use, path=None):
    """Generates a completely blind map.

    :param map_area: List of selected countries. Countries are represented using abbreviations.
    :param map_size: Name of paper size.
    :param map_config_on: List of selected elements that should be drawn on the map.
    :param map_config_name: List of selected elements that should have their names drawn on the map.
    :param map_use: Selected map use.
    :param path: Path prefix to use for filepath of output file.
    :return: Filename of output file.
    """
    # get all parameters
    map_format = get_map_format(map_use)
    map_size_px = size_to_px(map_size)
    map_config = parse_config(map_config_on, map_config_name)

    # register fonts
    mapnik.register_fonts('data/fonts/Merriweather')

    # create Map element and focus on desired area
    m = mapnik.Map(*map_size_px, '+init=epsg:3857')
    transform = mapnik.ProjTransform(mapnik.Projection('+init=epsg:4326'), mapnik.Projection('+init=epsg:3857'))
    m.zoom_to_box(transform.forward(mapnik.Box2d(*get_extent(map_area))))

    # left, bottom, right, top = get_extent(map_area)
    # krovak_transform = Transformer.from_crs("EPSG:4326", "EPSG:5514")
    # left, bottom = krovak_transform.transform(bottom, left)
    # right, top = krovak_transform.transform(top, right)
    # m.zoom_to_box(mapnik.Box2d(left, bottom, right, top))

    # load styles
    mapnik.load_map(m, 'data/styles/style-blind.xml')

    # select and add layers
    selected_layers = select_layers(map_config)
    for layer in selected_layers:
        m.layers.append(create_layer(layer.name, layer.style, layer.query, map_area))

    if not path:
        path = ''

    # generate output file
    zoom_factor = zoom_factors[map_size]
    if map_format == 'png':
        im = mapnik.Image(m.width, m.height)
        mapnik.render(m, im, zoom_factor)
        filename = map_util.save_raster_file(im, map_format, path=path)
    elif map_format == 'pdf':
        filename = map_util.generate_vector_filename(map_format, path=path)
        surface = cairo.PDFSurface(filename, *map_size_px)
        mapnik.render(m, surface, zoom_factor, 0, 0)
        surface.finish()
    else:
        return None

    return filename

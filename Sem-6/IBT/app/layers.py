"""
This file contains definitions of layers, layer options and help functions used for generating more or less blind maps.

file:   layers.py
author: Jakub Duda, xdudaj02
date:   8. 5. 2022
"""


def adjust_style(style_string, color_scheme, map_zoom_level, projection):
    """Performs adjustments in style definitions. Adjustments are based on projection, zoom level and color scheme.

    :param style_string: String containing style definitions.
    :param color_scheme: Name of selected color scheme.
    :param map_zoom_level: Zoom level of the map.
    :param projection: String representation of the selected projection.
    :return: Adjusted string containing style definitions.
    """

    # dictionary with background color values for different color schemes
    cs_dict = {
        'grey': {'rgb(255, 217, 179)': 'rgb(217, 217, 217)', 'rgb(160, 220, 160)': 'rgb(225, 225, 225)',
                 'rgb(190, 240, 190)': 'rgb(240, 240, 240)', 'rgb(255, 242, 204)': 'rgb(245, 245, 245)',
                 'rgb(140, 217, 140)': 'rgb(225, 225, 225)', 'rgb(200, 220, 170)': 'rgb(230, 230, 230)',
                 'rgb(210, 210, 190)': 'rgb(235, 235, 235)', 'rgb(223, 191, 159)': 'rgb(220, 220, 220)',
                 '<PolygonPatternSymbolizer file="../symbols/pattern/vineyard.svg" transform="scale(1.0)"/>': '',
                 '<PolygonPatternSymbolizer file="../symbols/pattern/orchard.svg" transform="scale(1.0)"/>': '',
                 'rgb(255, 255, 153)': 'rgb(250, 250, 250)', 'rgb(248, 242, 236)': 'rgb(255, 255, 255)'},
        'winter': {'rgb(255, 217, 179)': 'rgb(217, 217, 217)', 'rgb(160, 220, 160)': 'rgb(181, 205, 227)',
                   'rgb(190, 240, 190)': 'rgb(218, 230, 241)', 'rgb(255, 242, 204)': 'rgb(236, 242, 248)',
                   'rgb(200, 200, 200)': 'rgb(200, 217, 234)', 'rgb(140, 217, 140)': 'rgb(200, 217, 234)',
                   'rgb(200, 220, 170)': 'rgb(200, 217, 234)', 'rgb(210, 210, 190)': 'rgb(200, 217, 234)',
                   '<PolygonPatternSymbolizer file="../symbols/pattern/vineyard.svg" transform="scale(1.0)"/>': '',
                   '<PolygonPatternSymbolizer file="../symbols/pattern/orchard.svg" transform="scale(1.0)"/>': '',
                   'rgb(255, 255, 153)': 'rgb(218, 230, 241)', 'rgb(113, 218, 113)': 'rgb(163, 192, 220)'},
        'color': {}
    }

    # limit value used when deciding on area name size
    area_limit = '0' * (12 - map_zoom_level)

    # adjust colors
    for old, new in cs_dict[color_scheme].items():
        style_string = style_string.replace(old, new)

    # adjust area limits and projection
    style_string = style_string.replace('%area_limit%', area_limit)
    style_string = style_string.replace('%proj%', projection)

    # switch off clipping for Krovak projection - otherwise clipping bounds appear on map
    if projection[:4] == '5514':
        style_string = style_string.replace('clip="true"', '')

    return style_string


# zoom level variables
zoom_level_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
zoom_level_limits = [6188.56, 2232.03, 952.17, 377.87, 94.33, 14.15, 4.72, 0.94]
zoom_level_scale_factors = [0.05, 0.1, 0.25, 0.3, 0.4, 0.6, 1, 1.5, 2]
min_area_sizes = [
    [20000000000, 2000000000, 200000000, 20000000, 2000000, 200000, 20000, 2000, 200, 20],  # theme bottom, parking icon, marina
    [60000000000, 6000000000, 600000000, 60000000, 6000000, 600000, 60000, 6000, 600, 60],  # theme, skipark top
    [100000000000, 10000000000, 1000000000, 100000000, 10000000, 1000000, 100000, 10000, 1000, 100]]  # natural, boundary, landuse areas name, garden, park

# allowed options for every element group (max number for detail levels)
options = {
    'layer': ['surface', 'admin', 'hydro', 'natural', 'roads', 'rail', 'built', 'amenity', 'sport', 'special'],
    'surface_color': ['grey', 'color', 'winter'],
    'surface_natural': 4,
    'surface_farm': 5,
    'surface_built': 4,
    'admin_country': 5,
    'admin_region': 5,
    'admin_district': 5,
    'admin_capital': 3,
    'admin_city': 3,
    'admin_town': 3,
    'admin_village': 3,
    'admin_suburb': 2,
    'hydro_lake': 3,
    'hydro_river': 4,
    'hydro_stream': 3,
    'hydro_reservoir': 3,
    'hydro_canal': 3,
    'hydro_wetland': 2,
    'hydro_waterfall': 3,
    'hydro_spring': 2,
    'hydro_dam': 2,
    'hydro_breakwater': 2,
    'hydro_marina': 4,
    'hydro_route': 2,
    'natural_peak': 4,
    'natural_saddle': 4,
    'natural_cave': 4,
    'natural_volcano': 4,
    'natural_ridge': 2,
    'natural_cliff': 2,
    'natural_protected': 5,
    'natural_trees': 2,
    'natural_viewpoint': 2,
    'roads_motorway': 4,
    'roads_primary': 4,
    'roads_secondary': 4,
    'roads_tertiary': 3,
    'roads_link': 2,
    'roads_service': 3,
    'roads_residential': 3,
    'roads_pavement': 3,
    'roads_track': 2,
    'roads_path': 3,
    'roads_bridges': 4,
    'roads_tunnels': 4,
    'roads_construction': 2,
    'roads_names': 2,
    'roads_signs': 2,
    'roads_junction': 2,
    'rail_normal': 4,
    'rail_special': 4,
    'rail_tram': 3,
    'rail_subway': 3,
    'rail_bridges': 4,
    'rail_tunnels': 4,
    'rail_construction': 2,
    'rail_disused': 2,
    'rail_station': 4,
    'rail_tram_stop': 3,
    'built_buildings': 4,
    'built_aerial': 3,
    'built_statue': 3,
    'built_tower': 3,
    'built_barrier': 2,
    'built_gate': 2,
    'built_city': 2,
    'built_nature': 2,
    'amenity_shop': 3,
    'amenity_education': 3,
    'amenity_art': 3,
    'amenity_religion': 3,
    'amenity_office': 3,
    'amenity_medical': 3,
    'amenity_forces': 3,
    'amenity_finance': 3,
    'amenity_law': 3,
    'amenity_social': 3,
    'amenity_food': 3,
    'amenity_hotel': 3,
    'amenity_hut': 4,
    'amenity_parks': 3,
    'amenity_playground': 3,
    'amenity_pool': 4,
    'amenity_theme': 3,
    'amenity_castle': 3,
    'amenity_bus': 3,
    'amenity_parking': 2,
    'amenity_gas': 3,
    'amenity_aero': 4,
    'amenity_military': 3,
    'amenity_waste': 4,
    'amenity_quarry': 3,
    'amenity_cemetery': 3,
    'sport_racetrack': 2,
    'sport_stadium': 4,
    'sport_pitch': 4,
    'sport_athletic': 2,
    'sport_hike': 3,
    'sport_bike': 5,
    'sport_ski': 3,
    'sport_piste': 3,
    'sport_xcountry': 3,
    'sport_golf': 3
}

# limits for detail level of element groups at zoom levels (zoom level: maximum detail level)
limits = {'surface_natural': {0: 1},
          'surface_farm': {0: 1, 5: 3},
          'surface_built': {0: 1, 4: 3},
          'admin_country': {4: 3},
          'admin_region': {4: 1, 5: 3},
          'admin_district': {1: 1, 6: 3},
          'admin_capital': {1: 1},
          'admin_city': {2: 1},
          'admin_town': {3: 1},
          'admin_village': {5: 1},
          'admin_suburb': {5: 1},
          'hydro_lake': {3: 2},
          'hydro_river': {0: 1, 3: 2},
          'hydro_stream': {4: 1, 5: 2},
          'hydro_tunnel': {3: 1},
          'hydro_reservoir': {3: 2},
          'hydro_canal': {3: 1, 5: 2},
          'hydro_wetland': {4: 1},
          'hydro_waterfall': {5: 1, 6: 2},
          'hydro_spring': {6: 1},
          'hydro_dam': {4: 1},
          'hydro_breakwater': {4: 1},
          'hydro_marina': {4: 1, 5: 3},
          'hydro_route': {4: 1, 5: 2},
          'natural_peak': {5: 1},
          'natural_saddle': {5: 1, 6: 2},
          'natural_cave': {5: 1, 6: 2},
          'natural_volcano': {5: 1},
          'natural_ridge': {5: 1},
          'natural_cliff': {5: 1},
          'natural_protected': {4: 1},
          'natural_trees': {6: 1},
          'natural_viewpoint': {6: 1},
          'roads_motorway': {1: 1, 2: 2},
          'roads_primary': {2: 1, 3: 2},
          'roads_secondary': {3: 1, 4: 2},
          'roads_tertiary': {4: 1, 5: 2},
          'roads_link': {4: 1},
          'roads_service': {5: 1, 6: 2},
          'roads_residential': {5: 1, 6: 2},
          'roads_pavement': {7: 1},
          'roads_track': {5: 1},
          'roads_path': {6: 1},
          'roads_bridges': {6: 1},
          'roads_tunnels': {4: 1, 6: 2},
          'roads_construction': {},
          'roads_names': {5: 1},
          'roads_junction': {6: 1},
          'roads_signs': {7: 1},
          'rail_normal': {3: 1, 4: 2, 5: 3},
          'rail_special': {4: 1, 5: 2, 6: 3},
          'rail_tram': {5: 1, 6: 2},
          'rail_subway': {5: 1, 6: 2},
          'rail_bridges': {6: 1},
          'rail_tunnels': {4: 1, 5: 2},
          'rail_construction': {4: 1},
          'rail_disused': {6: 1},
          'rail_station': {5: 1, 6: 3},
          'rail_tram_stop': {6: 1},
          'built_buildings': {5: 1, 6: 2, 7: 3},
          'built_aerial': {4: 1, 5: 2},
          'built_statue': {6: 1, 7: 2},
          'built_tower': {6: 1, 7: 2},
          'built_barrier': {6: 1},
          'built_gate': {7: 1},
          'built_city': {7: 1},
          'built_nature': {7: 1},
          'amenity_shop': {6: 1, 7: 2},
          'amenity_education': {6: 1, 7: 2},
          'amenity_art': {6: 1, 7: 2},
          'amenity_religion': {6: 1, 7: 2},
          'amenity_office': {6: 1, 7: 2},
          'amenity_medical': {6: 1, 7: 2},
          'amenity_forces': {6: 1, 7: 2},
          'amenity_finance': {6: 1, 7: 2},
          'amenity_law': {6: 1, 7: 2},
          'amenity_social': {6: 1, 7: 2},
          'amenity_food': {6: 1, 7: 2},
          'amenity_hotel': {6: 1, 7: 2},
          'amenity_hut': {6: 1, 7: 2},
          'amenity_parks': {5: 1},
          'amenity_playground': {5: 1, 7: 2},
          'amenity_pool': {4: 1, 6: 2},
          'amenity_theme': {6: 1},
          'amenity_castle': {5: 1, 6: 2},
          'amenity_bus': {6: 1},
          'amenity_parking': {6: 1},
          'amenity_gas': {5: 1, 6: 2},
          'amenity_aero': {5: 1},
          'amenity_military': {4: 1, 5: 3},
          'amenity_waste': {5: 1, 6: 2, 7: 3},
          'amenity_quarry': {5: 1, 6: 3},
          'amenity_cemetery': {5: 1, 6: 3},
          'sport_racetrack': {5: 1},
          'sport_stadium': {5: 1, 6: 2, 7: 3},
          'sport_pitch': {5: 1, 6: 2, 7: 3},
          'sport_athletic': {5: 1, 6: 2},
          'sport_hike': {4: 1},
          'sport_bike': {4: 1},
          'sport_ski': {4: 1, 5: 2},
          'sport_piste': {4: 1, 5: 2},
          'sport_xcountry': {5: 1, 6: 2},
          'sport_golf': {5: 1},
          }

# layers and styles to use for detail levels of available element groups
cases = {
    'surface_natural': [
        {'land_use-natural-bottom': 0, 'natural-area': 0},
        {'land_use-natural-bottom': 1, 'natural-area': 1, 'man_made-way-cutline': 0},
        {'land_use-natural-bottom': 1, 'natural-area': 2, 'man_made-way-cutline': 0}
    ],
    'surface_farm': [
        {'land_use-farm-bottom': 0, 'land_use-farm-top': 0},
        {'land_use-farm-bottom': 1, 'land_use-farm-top': 1},
        {'land_use-farm-bottom': 2, 'land_use-farm-top': 1, 'leisure-area-garden': 0},
        {'land_use-farm-bottom': 2, 'land_use-farm-top': 1, 'leisure-area-garden': 0, 'land_use-farm-name': 0,
         'leisure-area-garden-detail': 0}
    ],
    'surface_built': [
        {'land_use-built-bottom': 0, 'land_use-built-top': 0},
        {'land_use-built-bottom': 0, 'land_use-built-top': 1, 'amenity-area-bottom': 0},
        {'land_use-built-bottom': 0, 'land_use-built-top': 1, 'amenity-area-bottom': 0, 'land_use-built-name': 0,
         'amenity-area-name': 0}
    ],

    # admin
    'admin_country': [
        {'boundary-admin-country': 0},
        {'boundary-admin-country': 0, 'boundary-admin-country-name': 0},
        {'boundary-admin-country': 0, 'boundary-admin-country-name': 1},
        {'boundary-admin-country': 0, 'boundary-admin-country-name': 2}
    ],
    'admin_region': [
        {'boundary-admin-region': 0},
        {'boundary-admin-region': 0, 'boundary-admin-region-name': 0},
        {'boundary-admin-region': 0, 'boundary-admin-region-name': 1},
        {'boundary-admin-region': 0, 'boundary-admin-region-name': 2}
    ],
    'admin_district': [
        {'boundary-admin-district': 0},
        {'boundary-admin-district': 0, 'boundary-admin-district-name': 0},
        {'boundary-admin-district': 0, 'boundary-admin-district-name': 1},
        {'boundary-admin-district': 0, 'boundary-admin-district-name': 2}
    ],
    'admin_capital': [
        {'place-admin-capital': 0},
        {'place-admin-capital': 1}
    ],
    'admin_city': [
        {'place-admin-city': 0},
        {'place-admin-city': 1}
    ],
    'admin_town': [
        {'place-admin-town': 0},
        {'place-admin-town': 1}
    ],
    'admin_village': [
        {'place-admin-village': 0},
        {'place-admin-village': 1, 'place-admin-dwelling': 0}
    ],
    'admin_suburb': [
        {'place-admin-suburb': 0, 'place-admin-neighborhood': 0}
    ],

    # hydro (repeated styles are for covering waterways)
    'hydro_lake': [
        {'hydro-lake': 0, 'hydro-lake-cover': 0},
        {'hydro-lake': 0, 'hydro-lake-cover': 0, 'water-area-lake-name': 0}
    ],
    'hydro_river': [
        {'hydro-river': 0, 'hydro-river-cover': 0},
        {'hydro-river': 0, 'waterway-river-bottom': 0, 'waterway-river-top': 0, 'hydro-river-cover': 0},
        {'hydro-river': 0, 'waterway-river-bottom': 0, 'waterway-river-top': 0, 'hydro-river-cover': 0,
         'waterway-river-name': 0, 'water-area-river-name': 0}
    ],
    'hydro_stream': [
        {'hydro-stream': 0, 'waterway-stream-bottom': 0, 'waterway-stream-top': 0, 'hydro-stream-cover': 0},
        {'hydro-stream': 0, 'waterway-stream-bottom': 0, 'waterway-stream-top': 0, 'hydro-stream-cover': 0,
         'waterway-stream-name': 0}
    ],
    'hydro_reservoir': [
        {'land_use-hydro-bottom': 0, 'hydro-reservoir': 0, 'hydro-reservoir-cover': 0},
        {'land_use-hydro-bottom': 0, 'hydro-reservoir': 0, 'hydro-reservoir-cover': 0, 'water-area-reservoir-name': 0}
    ],
    'hydro_canal': [
        {'hydro-canal': 0, 'waterway-canal-bottom': 0, 'waterway-canal-top': 0, 'waterway-ditch-bottom': 0,
         'waterway-ditch-top': 0, 'hydro-canal-cover': 0},
        {'hydro-canal': 0, 'waterway-canal-bottom': 0, 'waterway-canal-top': 0, 'waterway-ditch-bottom': 0,
         'waterway-ditch-top': 0, 'hydro-canal-cover': 0, 'waterway-canal-name': 0}
    ],
    'hydro_wetland': [
        {'hydro-wetland': 0, 'hydro-wetland-cover': 0}
    ],
    'hydro_waterfall': [
        {'hydro-item-waterfall': 0},
        {'hydro-item-waterfall': 1}
    ],
    'hydro_spring': [
        {'hydro-item-spring': 0}
    ],
    'hydro_dam': [
        {'waterway-dam': 0, 'waterway-area-dam': 0}
    ],
    'hydro_breakwater': [
        {'man_made-area-breakwater': 0, 'man_made-way-breakwater': 0}
    ],
    'hydro_marina': [
        {'leisure-area-marina': 0, 'man_made-area-breakwater': 0, 'man_made-way-breakwater': 0},
        {'leisure-area-marina': 0, 'man_made-area-breakwater': 0, 'man_made-way-breakwater': 0,
         'amenity-item-ferry': 0},
        {'leisure-area-marina': 0, 'man_made-area-breakwater': 0, 'man_made-way-breakwater': 0,
         'amenity-item-ferry': 1, 'leisure-area-marina-detail': 0}
    ],
    'hydro_route': [
        {'route-hydro': 0}
    ],

    # natural
    'natural_peak': [
        {'natural-item-peak': 0},
        {'natural-item-peak': 1},
        {'natural-item-peak': 2}
    ],
    'natural_saddle': [
        {'natural-item-saddle': 0},
        {'natural-item-saddle': 1},
        {'natural-item-saddle': 2}
    ],
    'natural_cave': [
        {'natural-item-cave': 0},
        {'natural-item-cave': 1},
        {'natural-item-cave': 2}
    ],
    'natural_volcano': [
        {'natural-item-volcano': 0},
        {'natural-item-volcano': 1},
        {'natural-item-volcano': 2}
    ],
    'natural_ridge': [
        {'natural-way-ridge': 0}
    ],
    'natural_cliff': [
        {'natural-way-cliff': 0}
    ],
    'natural_protected': [
        {'boundary-protected': 0},
        {'boundary-protected': 0, 'boundary-protected-name': 0},
        {'boundary-protected': 0, 'boundary-protected-name': 1},
        {'boundary-protected': 0, 'boundary-protected-name': 2},
    ],
    'natural_trees': [
        {'natural-way-tree_row': 0}
    ],
    'natural_viewpoint': [
        {'tourism-item-viewpoint': 0}
    ],

    # roads
    'roads_motorway': [
        {'hw-motorway-weak': 0, 'hw-trunk-weak': 0},
        {'hw-motorway-bottom': 0, 'hw-trunk-bottom': 0, 'hw-motorway-top': 0, 'hw-trunk-top': 0},
        {'hw-motorway-bottom': 1, 'hw-trunk-bottom': 1, 'hw-motorway-top': 1, 'hw-trunk-top': 1}
    ],
    'roads_primary': [
        {'hw-primary-weak': 0},
        {'hw-primary-bottom': 0, 'hw-primary-top': 0},
        {'hw-primary-bottom': 1, 'hw-primary-top': 1}
    ],
    'roads_secondary': [
        {'hw-secondary-weak': 0},
        {'hw-secondary-bottom': 0, 'hw-secondary-top': 0},
        {'hw-secondary-bottom': 1, 'hw-secondary-top': 1}
    ],
    'roads_tertiary': [
        {'hw-tertiary-weak': 0},
        {'hw-tertiary-bottom': 0, 'hw-tertiary-top': 0}
    ],
    'roads_motorway_link': [
        {'hw-link-highway-weak': 0},
        {'hw-link-highway-bottom': 0, 'hw-link-highway-top': 0},
        {'hw-link-highway-bottom': 1, 'hw-link-highway-top': 1}
    ],
    'roads_primary_link': [
        {'hw-link-primary-weak': 0},
        {'hw-link-primary-bottom': 0, 'hw-link-primary-top': 0},
        {'hw-link-primary-bottom': 1, 'hw-link-primary-top': 1}
    ],
    'roads_secondary_link': [
        {'hw-link-secondary-weak': 0},
        {'hw-link-secondary-bottom': 0, 'hw-link-secondary-top': 0},
        {'hw-link-secondary-bottom': 1, 'hw-link-secondary-top': 1}
    ],
    'roads_tertiary_link': [
        {'hw-link-tertiary-weak': 0},
        {'hw-link-tertiary-bottom': 0, 'hw-link-tertiary-top': 0}
    ],
    'roads_service': [
        {'hw-service-weak': 0},
        {'highway-area-service': 0, 'hw-service-bottom': 0, 'hw-service-top': 0, 'hw-service-private': 0}
    ],
    'roads_residential': [
        {'hw-residential-weak': 0, 'hw-pedestrian-weak': 0},
        {'highway-area-parking': 0, 'highway-area-pedestrian': 0, 'hw-residential-bottom': 0,
         'hw-pedestrian-bottom': 0, 'hw-residential-top': 0, 'hw-pedestrian-top': 0, 'hw-residential-private': 0}
    ],
    'roads_pavement': [
        {'hw-pavement': 0},
        {'hw-pavement': 1}
    ],
    'roads_track': [
        {'hw-track': 0}
    ],
    'roads_path': [
        {'hw-path': 0},
        {'hw-path': 1}
    ],
    # roads_bridges
    'roads_motorway_bridge': [
        {'hw-bridge-1-motorway-weak-bottom': 0, 'hw-bridge-1-trunk-weak-bottom': 0, 'hw-bridge-1-motorway-weak': 0,
         'hw-bridge-1-trunk-weak': 0, 'hw-bridge-2-motorway-weak-bottom': 0, 'hw-bridge-2-trunk-weak-bottom': 0,
         'hw-bridge-2-motorway-weak': 0, 'hw-bridge-2-trunk-weak': 0, 'hw-bridge-3-motorway-weak-bottom': 0,
         'hw-bridge-3-trunk-weak-bottom': 0, 'hw-bridge-3-motorway-weak': 0, 'hw-bridge-3-trunk-weak': 0,
         'hw-bridge-4-motorway-weak-bottom': 0, 'hw-bridge-4-trunk-weak-bottom': 0, 'hw-bridge-4-motorway-weak': 0,
         'hw-bridge-4-trunk-weak': 0, 'hw-bridge-5-motorway-weak-bottom': 0, 'hw-bridge-5-trunk-weak-bottom': 0,
         'hw-bridge-5-motorway-weak': 0, 'hw-bridge-5-trunk-weak': 0},
        {'hw-bridge-1-motorway-bottom': 0, 'hw-bridge-1-trunk-bottom': 0, 'hw-bridge-1-motorway-top': 0,
         'hw-bridge-1-trunk-top': 0, 'hw-bridge-2-motorway-bottom': 0, 'hw-bridge-2-trunk-bottom': 0,
         'hw-bridge-2-motorway-top': 0, 'hw-bridge-2-trunk-top': 0, 'hw-bridge-3-motorway-bottom': 0,
         'hw-bridge-3-trunk-bottom': 0, 'hw-bridge-3-motorway-top': 0, 'hw-bridge-3-trunk-top': 0,
         'hw-bridge-4-motorway-bottom': 0, 'hw-bridge-4-trunk-bottom': 0, 'hw-bridge-4-motorway-top': 0,
         'hw-bridge-4-trunk-top': 0, 'hw-bridge-5-motorway-bottom': 0, 'hw-bridge-5-trunk-bottom': 0,
         'hw-bridge-5-motorway-top': 0, 'hw-bridge-5-trunk-top': 0},
        {'hw-bridge-1-motorway-bottom': 0, 'hw-bridge-1-trunk-bottom': 0, 'hw-bridge-1-motorway-top': 1,
         'hw-bridge-1-trunk-top': 1, 'hw-bridge-2-motorway-bottom': 0, 'hw-bridge-2-trunk-bottom': 0,
         'hw-bridge-2-motorway-top': 1, 'hw-bridge-2-trunk-top': 1, 'hw-bridge-3-motorway-bottom': 0,
         'hw-bridge-3-trunk-bottom': 0, 'hw-bridge-3-motorway-top': 1, 'hw-bridge-3-trunk-top': 1,
         'hw-bridge-4-motorway-bottom': 0, 'hw-bridge-4-trunk-bottom': 0, 'hw-bridge-4-motorway-top': 1,
         'hw-bridge-4-trunk-top': 1, 'hw-bridge-5-motorway-bottom': 0, 'hw-bridge-5-trunk-bottom': 0,
         'hw-bridge-5-motorway-top': 1, 'hw-bridge-5-trunk-top': 1},
    ],
    'roads_primary_bridge': [
        {'hw-bridge-1-primary-weak-bottom': 0, 'hw-bridge-1-primary-weak': 0, 'hw-bridge-2-primary-weak-bottom': 0,
         'hw-bridge-2-primary-weak': 0, 'hw-bridge-3-primary-weak-bottom': 0, 'hw-bridge-3-primary-weak': 0,
         'hw-bridge-4-primary-weak-bottom': 0, 'hw-bridge-4-primary-weak': 0, 'hw-bridge-5-primary-weak-bottom': 0,
         'hw-bridge-5-primary-weak': 0},
        {'hw-bridge-1-primary-bottom': 0, 'hw-bridge-1-primary-top': 0, 'hw-bridge-2-primary-bottom': 0,
         'hw-bridge-2-primary-top': 0, 'hw-bridge-3-primary-bottom': 0, 'hw-bridge-3-primary-top': 0,
         'hw-bridge-4-primary-bottom': 0, 'hw-bridge-4-primary-top': 0, 'hw-bridge-5-primary-bottom': 0,
         'hw-bridge-5-primary-top': 0},
        {'hw-bridge-1-primary-bottom': 0, 'hw-bridge-1-primary-top': 1, 'hw-bridge-2-primary-bottom': 0,
         'hw-bridge-2-primary-top': 1, 'hw-bridge-3-primary-bottom': 0, 'hw-bridge-3-primary-top': 1,
         'hw-bridge-4-primary-bottom': 0, 'hw-bridge-4-primary-top': 1, 'hw-bridge-5-primary-bottom': 0,
         'hw-bridge-5-primary-top': 1}
    ],
    'roads_secondary_bridge': [
        {'hw-bridge-1-secondary-weak-bottom': 0, 'hw-bridge-1-secondary-weak': 0,
         'hw-bridge-2-secondary-weak-bottom': 0, 'hw-bridge-2-secondary-weak': 0,
         'hw-bridge-3-secondary-weak-bottom': 0, 'hw-bridge-3-secondary-weak': 0,
         'hw-bridge-4-secondary-weak-bottom': 0, 'hw-bridge-4-secondary-weak': 0,
         'hw-bridge-5-secondary-weak-bottom': 0, 'hw-bridge-5-secondary-weak': 0},
        {'hw-bridge-1-secondary-bottom': 0, 'hw-bridge-1-secondary-top': 0, 'hw-bridge-2-secondary-bottom': 0,
         'hw-bridge-2-secondary-top': 0, 'hw-bridge-3-secondary-bottom': 0, 'hw-bridge-3-secondary-top': 0,
         'hw-bridge-4-secondary-bottom': 0, 'hw-bridge-4-secondary-top': 0, 'hw-bridge-5-secondary-bottom': 0,
         'hw-bridge-5-secondary-top': 0},
        {'hw-bridge-1-secondary-bottom': 0, 'hw-bridge-1-secondary-top': 1, 'hw-bridge-2-secondary-bottom': 0,
         'hw-bridge-2-secondary-top': 1, 'hw-bridge-3-secondary-bottom': 0, 'hw-bridge-3-secondary-top': 1,
         'hw-bridge-4-secondary-bottom': 0, 'hw-bridge-4-secondary-top': 1, 'hw-bridge-5-secondary-bottom': 0,
         'hw-bridge-5-secondary-top': 1}
    ],
    'roads_tertiary_bridge': [
        {'hw-bridge-1-tertiary-weak-bottom': 0, 'hw-bridge-1-tertiary-weak': 0, 'hw-bridge-2-tertiary-weak-bottom': 0,
         'hw-bridge-2-tertiary-weak': 0, 'hw-bridge-3-tertiary-weak-bottom': 0, 'hw-bridge-3-tertiary-weak': 0,
         'hw-bridge-4-tertiary-weak-bottom': 0, 'hw-bridge-4-tertiary-weak': 0, 'hw-bridge-5-tertiary-weak-bottom': 0,
         'hw-bridge-5-tertiary-weak': 0},
        {'hw-bridge-1-tertiary-bottom': 0, 'hw-bridge-1-tertiary-top': 0, 'hw-bridge-2-tertiary-bottom': 0,
         'hw-bridge-2-tertiary-top': 0, 'hw-bridge-3-tertiary-bottom': 0, 'hw-bridge-3-tertiary-top': 0,
         'hw-bridge-4-tertiary-bottom': 0, 'hw-bridge-4-tertiary-top': 0, 'hw-bridge-5-tertiary-bottom': 0,
         'hw-bridge-5-tertiary-top': 0},
    ],
    'roads_residential_bridge': [
        {'hw-bridge-1-residential-weak-bottom': 0, 'hw-bridge-1-residential-weak': 0,
         'hw-bridge-1-pedestrian-weak-bottom': 0, 'hw-bridge-1-pedestrian-weak': 0,
         'hw-bridge-2-residential-weak-bottom': 0, 'hw-bridge-2-residential-weak': 0,
         'hw-bridge-2-pedestrian-weak-bottom': 0, 'hw-bridge-2-pedestrian-weak': 0,
         'hw-bridge-3-residential-weak-bottom': 0, 'hw-bridge-3-residential-weak': 0,
         'hw-bridge-3-pedestrian-weak-bottom': 0, 'hw-bridge-3-pedestrian-weak': 0,
         'hw-bridge-4-residential-weak-bottom': 0, 'hw-bridge-4-residential-weak': 0,
         'hw-bridge-4-pedestrian-weak-bottom': 0, 'hw-bridge-4-pedestrian-weak': 0,
         'hw-bridge-5-residential-weak-bottom': 0, 'hw-bridge-5-residential-weak': 0,
         'hw-bridge-5-pedestrian-weak-bottom': 0, 'hw-bridge-5-pedestrian-weak': 0},
        {'hw-bridge-1-residential-bottom': 0, 'hw-bridge-1-residential-top': 0, 'hw-bridge-1-pedestrian-top': 0,
         'hw-bridge-1-residential-private': 0, 'hw-bridge-2-residential-bottom': 0, 'hw-bridge-2-residential-top': 0,
         'hw-bridge-2-pedestrian-top': 0, 'hw-bridge-2-residential-private': 0, 'hw-bridge-3-residential-bottom': 0,
         'hw-bridge-3-residential-top': 0, 'hw-bridge-3-pedestrian-top': 0, 'hw-bridge-3-residential-private': 0,
         'hw-bridge-4-residential-bottom': 0, 'hw-bridge-4-residential-top': 0, 'hw-bridge-4-pedestrian-top': 0,
         'hw-bridge-4-residential-private': 0, 'hw-bridge-5-residential-bottom': 0, 'hw-bridge-5-residential-top': 0,
         'hw-bridge-5-pedestrian-top': 0, 'hw-bridge-5-residential-private': 0}
    ],
    'roads_service_bridge': [
        {'hw-bridge-1-service-weak-bottom': 0, 'hw-bridge-1-service-weak': 0, 'hw-bridge-2-service-weak-bottom': 0,
         'hw-bridge-2-service-weak': 0, 'hw-bridge-3-service-weak-bottom': 0, 'hw-bridge-3-service-weak': 0,
         'hw-bridge-4-service-weak-bottom': 0, 'hw-bridge-4-service-weak': 0, 'hw-bridge-5-service-weak-bottom': 0,
         'hw-bridge-5-service-weak': 0},
        {'hw-bridge-1-service-bottom': 0, 'hw-bridge-1-service-top': 0, 'hw-bridge-1-service-private': 0,
         'hw-bridge-2-service-bottom': 0, 'hw-bridge-2-service-top': 0, 'hw-bridge-2-service-private': 0,
         'hw-bridge-3-service-bottom': 0, 'hw-bridge-3-service-top': 0, 'hw-bridge-3-service-private': 0,
         'hw-bridge-4-service-bottom': 0, 'hw-bridge-4-service-top': 0, 'hw-bridge-4-service-private': 0,
         'hw-bridge-5-service-bottom': 0, 'hw-bridge-5-service-top': 0, 'hw-bridge-5-service-private': 0}
    ],
    'roads_track_bridge': [
        {'hw-bridge-1-track-bottom': 0, 'hw-bridge-1-track-middle': 0, 'hw-bridge-1-track': 0,
         'hw-bridge-2-track-bottom': 0, 'hw-bridge-2-track-middle': 0, 'hw-bridge-2-track': 0,
         'hw-bridge-3-track-bottom': 0, 'hw-bridge-3-track-middle': 0, 'hw-bridge-3-track': 0,
         'hw-bridge-4-track-bottom': 0, 'hw-bridge-4-track-middle': 0, 'hw-bridge-4-track': 0,
         'hw-bridge-5-track-bottom': 0, 'hw-bridge-5-track-middle': 0, 'hw-bridge-5-track': 0}
    ],
    'roads_path_bridge': [
        {'hw-bridge-1-path-bottom': 0, 'hw-bridge-1-path-middle': 0, 'hw-bridge-1-path': 0,
         'hw-bridge-2-path-bottom': 0, 'hw-bridge-2-path-middle': 0, 'hw-bridge-2-path': 0,
         'hw-bridge-3-path-bottom': 0, 'hw-bridge-3-path-middle': 0, 'hw-bridge-3-path': 0,
         'hw-bridge-4-path-bottom': 0, 'hw-bridge-4-path-middle': 0, 'hw-bridge-4-path': 0,
         'hw-bridge-5-path-bottom': 0, 'hw-bridge-5-path-middle': 0, 'hw-bridge-5-path': 0},
        {'hw-bridge-1-path-bottom': 0, 'hw-bridge-1-path-middle': 0, 'hw-bridge-1-path': 1,
         'hw-bridge-2-path-bottom': 0, 'hw-bridge-2-path-middle': 0, 'hw-bridge-2-path': 1,
         'hw-bridge-3-path-bottom': 0, 'hw-bridge-3-path-middle': 0, 'hw-bridge-3-path': 1,
         'hw-bridge-4-path-bottom': 0, 'hw-bridge-4-path-middle': 0, 'hw-bridge-4-path': 1,
         'hw-bridge-5-path-bottom': 0, 'hw-bridge-5-path-middle': 0, 'hw-bridge-5-path': 1}
    ],
    'roads_pavement_bridge': [
        {'hw-bridge-1-pavement-bottom': 0, 'hw-bridge-1-pavement-middle': 0, 'hw-bridge-1-pavement': 0,
         'hw-bridge-2-pavement-bottom': 0, 'hw-bridge-2-pavement-middle': 0, 'hw-bridge-2-pavement': 0,
         'hw-bridge-3-pavement-bottom': 0, 'hw-bridge-3-pavement-middle': 0, 'hw-bridge-3-pavement': 0,
         'hw-bridge-4-pavement-bottom': 0, 'hw-bridge-4-pavement-middle': 0, 'hw-bridge-4-pavement': 0,
         'hw-bridge-5-pavement-bottom': 0, 'hw-bridge-5-pavement-middle': 0, 'hw-bridge-5-pavement': 0},
        {'hw-bridge-1-pavement-bottom': 0, 'hw-bridge-1-pavement-middle': 0, 'hw-bridge-1-pavement': 1,
         'hw-bridge-2-pavement-bottom': 0, 'hw-bridge-2-pavement-middle': 0, 'hw-bridge-2-pavement': 1,
         'hw-bridge-3-pavement-bottom': 0, 'hw-bridge-3-pavement-middle': 0, 'hw-bridge-3-pavement': 1,
         'hw-bridge-4-pavement-bottom': 0, 'hw-bridge-4-pavement-middle': 0, 'hw-bridge-4-pavement': 1,
         'hw-bridge-5-pavement-bottom': 0, 'hw-bridge-5-pavement-middle': 0, 'hw-bridge-5-pavement': 1}
    ],
    'roads_motorway_link_bridge': [
        {'hw-bridge-1-link-highway-weak-bottom': 0, 'hw-bridge-1-link-highway-weak': 0,
         'hw-bridge-2-link-highway-weak-bottom': 0, 'hw-bridge-2-link-highway-weak': 0,
         'hw-bridge-3-link-highway-weak-bottom': 0, 'hw-bridge-3-link-highway-weak': 0,
         'hw-bridge-4-link-highway-weak-bottom': 0, 'hw-bridge-4-link-highway-weak': 0,
         'hw-bridge-5-link-highway-weak-bottom': 0, 'hw-bridge-5-link-highway-weak': 0},
        {'hw-bridge-1-link-highway-bottom': 0, 'hw-bridge-1-link-highway-top': 0, 'hw-bridge-2-link-highway-bottom': 0,
         'hw-bridge-2-link-highway-top': 0, 'hw-bridge-3-link-highway-bottom': 0, 'hw-bridge-3-link-highway-top': 0,
         'hw-bridge-4-link-highway-bottom': 0, 'hw-bridge-4-link-highway-top': 0, 'hw-bridge-5-link-highway-bottom': 0,
         'hw-bridge-5-link-highway-top': 0},
        {'hw-bridge-1-link-highway-bottom': 0, 'hw-bridge-1-link-highway-top': 1, 'hw-bridge-2-link-highway-bottom': 0,
         'hw-bridge-2-link-highway-top': 1, 'hw-bridge-3-link-highway-bottom': 0, 'hw-bridge-3-link-highway-top': 1,
         'hw-bridge-4-link-highway-bottom': 0, 'hw-bridge-4-link-highway-top': 1, 'hw-bridge-5-link-highway-bottom': 0,
         'hw-bridge-5-link-highway-top': 1},
    ],
    'roads_primary_link_bridge': [
        {'hw-bridge-1-link-primary-weak-bottom': 0, 'hw-bridge-1-link-primary-weak': 0,
         'hw-bridge-2-link-primary-weak-bottom': 0, 'hw-bridge-2-link-primary-weak': 0,
         'hw-bridge-3-link-primary-weak-bottom': 0, 'hw-bridge-3-link-primary-weak': 0,
         'hw-bridge-4-link-primary-weak-bottom': 0, 'hw-bridge-4-link-primary-weak': 0,
         'hw-bridge-5-link-primary-weak-bottom': 0, 'hw-bridge-5-link-primary-weak': 0},
        {'hw-bridge-1-link-primary-bottom': 0, 'hw-bridge-1-link-primary-top': 0, 'hw-bridge-2-link-primary-bottom': 0,
         'hw-bridge-2-link-primary-top': 0, 'hw-bridge-3-link-primary-bottom': 0, 'hw-bridge-3-link-primary-top': 0,
         'hw-bridge-4-link-primary-bottom': 0, 'hw-bridge-4-link-primary-top': 0, 'hw-bridge-5-link-primary-bottom': 0,
         'hw-bridge-5-link-primary-top': 0},
        {'hw-bridge-1-link-primary-bottom': 0, 'hw-bridge-1-link-primary-top': 1, 'hw-bridge-2-link-primary-bottom': 0,
         'hw-bridge-2-link-primary-top': 1, 'hw-bridge-3-link-primary-bottom': 0, 'hw-bridge-3-link-primary-top': 1,
         'hw-bridge-4-link-primary-bottom': 0, 'hw-bridge-4-link-primary-top': 1, 'hw-bridge-5-link-primary-bottom': 0,
         'hw-bridge-5-link-primary-top': 1},
    ],
    'roads_secondary_link_bridge': [
        {'hw-bridge-1-link-secondary-weak-bottom': 0, 'hw-bridge-1-link-secondary-weak': 0,
         'hw-bridge-2-link-secondary-weak-bottom': 0, 'hw-bridge-2-link-secondary-weak': 0,
         'hw-bridge-3-link-secondary-weak-bottom': 0, 'hw-bridge-3-link-secondary-weak': 0,
         'hw-bridge-4-link-secondary-weak-bottom': 0, 'hw-bridge-4-link-secondary-weak': 0,
         'hw-bridge-5-link-secondary-weak-bottom': 0, 'hw-bridge-5-link-secondary-weak': 0},
        {'hw-bridge-1-link-secondary-bottom': 0, 'hw-bridge-1-link-secondary-top': 0,
         'hw-bridge-2-link-secondary-bottom': 0, 'hw-bridge-2-link-secondary-top': 0,
         'hw-bridge-3-link-secondary-bottom': 0, 'hw-bridge-3-link-secondary-top': 0,
         'hw-bridge-4-link-secondary-bottom': 0, 'hw-bridge-4-link-secondary-top': 0,
         'hw-bridge-5-link-secondary-bottom': 0, 'hw-bridge-5-link-secondary-top': 0},
        {'hw-bridge-1-link-secondary-bottom': 0, 'hw-bridge-1-link-secondary-top': 1,
         'hw-bridge-2-link-secondary-bottom': 0, 'hw-bridge-2-link-secondary-top': 1,
         'hw-bridge-3-link-secondary-bottom': 0, 'hw-bridge-3-link-secondary-top': 1,
         'hw-bridge-4-link-secondary-bottom': 0, 'hw-bridge-4-link-secondary-top': 1,
         'hw-bridge-5-link-secondary-bottom': 0, 'hw-bridge-5-link-secondary-top': 1},
    ],
    'roads_tertiary_link_bridge': [
        {'hw-bridge-1-link-tertiary-weak-bottom': 0, 'hw-bridge-1-link-tertiary-weak': 0,
         'hw-bridge-2-link-tertiary-weak-bottom': 0, 'hw-bridge-2-link-tertiary-weak': 0,
         'hw-bridge-3-link-tertiary-weak-bottom': 0, 'hw-bridge-3-link-tertiary-weak': 0,
         'hw-bridge-4-link-tertiary-weak-bottom': 0, 'hw-bridge-4-link-tertiary-weak': 0,
         'hw-bridge-5-link-tertiary-weak-bottom': 0, 'hw-bridge-5-link-tertiary-weak': 0},
        {'hw-bridge-1-link-tertiary-bottom': 0, 'hw-bridge-1-link-tertiary-top': 0,
         'hw-bridge-2-link-tertiary-bottom': 0, 'hw-bridge-2-link-tertiary-top': 0,
         'hw-bridge-3-link-tertiary-bottom': 0, 'hw-bridge-3-link-tertiary-top': 0,
         'hw-bridge-4-link-tertiary-bottom': 0, 'hw-bridge-4-link-tertiary-top': 0,
         'hw-bridge-5-link-tertiary-bottom': 0, 'hw-bridge-5-link-tertiary-top': 0},
    ],
    'roads_motorway_const_bridge': [
        {'hw-bridge-1-const-motorway-weak': 0, 'hw-bridge-1-const-trunk-weak': 0,
         'hw-bridge-2-const-motorway-weak': 0, 'hw-bridge-2-const-trunk-weak': 0,
         'hw-bridge-3-const-motorway-weak': 0, 'hw-bridge-3-const-trunk-weak': 0,
         'hw-bridge-4-const-motorway-weak': 0, 'hw-bridge-4-const-trunk-weak': 0,
         'hw-bridge-5-const-motorway-weak': 0, 'hw-bridge-5-const-trunk-weak': 0},
        {'hw-bridge-1-const-highway-bottom': 0, 'hw-bridge-1-const-highway-middle': 0,
         'hw-bridge-1-const-highway-top': 0, 'hw-bridge-2-const-highway-bottom': 0,
         'hw-bridge-2-const-highway-middle': 0, 'hw-bridge-2-const-highway-top': 0,
         'hw-bridge-3-const-highway-bottom': 0, 'hw-bridge-3-const-highway-middle': 0,
         'hw-bridge-3-const-highway-top': 0, 'hw-bridge-4-const-highway-bottom': 0,
         'hw-bridge-4-const-highway-middle': 0, 'hw-bridge-4-const-highway-top': 0,
         'hw-bridge-5-const-highway-bottom': 0, 'hw-bridge-5-const-highway-middle': 0,
         'hw-bridge-5-const-highway-top': 0},
        {'hw-bridge-1-const-highway-bottom': 0, 'hw-bridge-1-const-highway-middle': 0,
         'hw-bridge-1-const-highway-top': 1, 'hw-bridge-2-const-highway-bottom': 0,
         'hw-bridge-2-const-highway-middle': 0, 'hw-bridge-2-const-highway-top': 1,
         'hw-bridge-3-const-highway-bottom': 0, 'hw-bridge-3-const-highway-middle': 0,
         'hw-bridge-3-const-highway-top': 1, 'hw-bridge-4-const-highway-bottom': 0,
         'hw-bridge-4-const-highway-middle': 0, 'hw-bridge-4-const-highway-top': 1,
         'hw-bridge-5-const-highway-bottom': 0, 'hw-bridge-5-const-highway-middle': 0,
         'hw-bridge-5-const-highway-top': 1}
    ],
    'roads_primary_const_bridge': [
        {'hw-bridge-1-const-primary-weak': 0, 'hw-bridge-2-const-primary-weak': 0, 'hw-bridge-3-const-primary-weak': 0,
         'hw-bridge-4-const-primary-weak': 0, 'hw-bridge-5-const-primary-weak': 0},
        {'hw-bridge-1-const-primary-bottom': 0, 'hw-bridge-1-const-primary-middle': 0,
         'hw-bridge-1-const-primary-top': 0, 'hw-bridge-2-const-primary-bottom': 0,
         'hw-bridge-2-const-primary-middle': 0, 'hw-bridge-2-const-primary-top': 0,
         'hw-bridge-3-const-primary-bottom': 0, 'hw-bridge-3-const-primary-middle': 0,
         'hw-bridge-3-const-primary-top': 0, 'hw-bridge-4-const-primary-bottom': 0,
         'hw-bridge-4-const-primary-middle': 0, 'hw-bridge-4-const-primary-top': 0,
         'hw-bridge-5-const-primary-bottom': 0, 'hw-bridge-5-const-primary-middle': 0,
         'hw-bridge-5-const-primary-top': 0},
        {'hw-bridge-1-const-primary-bottom': 0, 'hw-bridge-1-const-primary-middle': 0,
         'hw-bridge-1-const-primary-top': 1, 'hw-bridge-2-const-primary-bottom': 0,
         'hw-bridge-2-const-primary-middle': 0, 'hw-bridge-2-const-primary-top': 1,
         'hw-bridge-3-const-primary-bottom': 0, 'hw-bridge-3-const-primary-middle': 0,
         'hw-bridge-3-const-primary-top': 1, 'hw-bridge-4-const-primary-bottom': 0,
         'hw-bridge-4-const-primary-middle': 0, 'hw-bridge-4-const-primary-top': 1,
         'hw-bridge-5-const-primary-bottom': 0, 'hw-bridge-5-const-primary-middle': 0,
         'hw-bridge-5-const-primary-top': 1}
    ],
    'roads_secondary_const_bridge': [
        {'hw-bridge-1-const-secondary-weak': 0, 'hw-bridge-2-const-secondary-weak': 0,
         'hw-bridge-3-const-secondary-weak': 0, 'hw-bridge-4-const-secondary-weak': 0,
         'hw-bridge-5-const-secondary-weak': 0},
        {'hw-bridge-1-const-secondary-bottom': 0, 'hw-bridge-1-const-secondary-middle': 0,
         'hw-bridge-1-const-secondary-top': 0, 'hw-bridge-2-const-secondary-bottom': 0,
         'hw-bridge-2-const-secondary-middle': 0, 'hw-bridge-2-const-secondary-top': 0,
         'hw-bridge-3-const-secondary-bottom': 0, 'hw-bridge-3-const-secondary-middle': 0,
         'hw-bridge-3-const-secondary-top': 0, 'hw-bridge-4-const-secondary-bottom': 0,
         'hw-bridge-4-const-secondary-middle': 0, 'hw-bridge-4-const-secondary-top': 0,
         'hw-bridge-5-const-secondary-bottom': 0, 'hw-bridge-5-const-secondary-middle': 0,
         'hw-bridge-5-const-secondary-top': 0},
        {'hw-bridge-1-const-secondary-bottom': 0, 'hw-bridge-1-const-secondary-middle': 0,
         'hw-bridge-1-const-secondary-top': 1, 'hw-bridge-2-const-secondary-bottom': 0,
         'hw-bridge-2-const-secondary-middle': 0, 'hw-bridge-2-const-secondary-top': 1,
         'hw-bridge-3-const-secondary-bottom': 0, 'hw-bridge-3-const-secondary-middle': 0,
         'hw-bridge-3-const-secondary-top': 1, 'hw-bridge-4-const-secondary-bottom': 0,
         'hw-bridge-4-const-secondary-middle': 0, 'hw-bridge-4-const-secondary-top': 1,
         'hw-bridge-5-const-secondary-bottom': 0, 'hw-bridge-5-const-secondary-middle': 0,
         'hw-bridge-5-const-secondary-top': 1}
    ],
    'roads_tertiary_const_bridge': [
        {'hw-bridge-1-const-tertiary-weak': 0, 'hw-bridge-2-const-tertiary-weak': 0,
         'hw-bridge-3-const-tertiary-weak': 0, 'hw-bridge-4-const-tertiary-weak': 0,
         'hw-bridge-5-const-tertiary-weak': 0},
        {'hw-bridge-1-const-tertiary-bottom': 0, 'hw-bridge-1-const-tertiary-middle': 0,
         'hw-bridge-1-const-tertiary-top': 0, 'hw-bridge-2-const-tertiary-bottom': 0,
         'hw-bridge-2-const-tertiary-middle': 0, 'hw-bridge-2-const-tertiary-top': 0,
         'hw-bridge-3-const-tertiary-bottom': 0, 'hw-bridge-3-const-tertiary-middle': 0,
         'hw-bridge-3-const-tertiary-top': 0, 'hw-bridge-4-const-tertiary-bottom': 0,
         'hw-bridge-4-const-tertiary-middle': 0, 'hw-bridge-4-const-tertiary-top': 0,
         'hw-bridge-5-const-tertiary-bottom': 0, 'hw-bridge-5-const-tertiary-middle': 0,
         'hw-bridge-5-const-tertiary-top': 0}
    ],
    'roads_residential_const_bridge': [
        {'hw-bridge-1-const-pedestrian-weak': 0, 'hw-bridge-1-const-residential-weak': 0,
         'hw-bridge-2-const-pedestrian-weak': 0, 'hw-bridge-2-const-residential-weak': 0,
         'hw-bridge-3-const-pedestrian-weak': 0, 'hw-bridge-3-const-residential-weak': 0,
         'hw-bridge-4-const-pedestrian-weak': 0, 'hw-bridge-4-const-residential-weak': 0,
         'hw-bridge-5-const-pedestrian-weak': 0, 'hw-bridge-5-const-residential-weak': 0},
        {'hw-bridge-1-const-residential-bottom': 0, 'hw-bridge-1-const-residential-middle': 0,
         'hw-bridge-1-const-residential-top': 0, 'hw-bridge-2-const-residential-bottom': 0,
         'hw-bridge-2-const-residential-middle': 0, 'hw-bridge-2-const-residential-top': 0,
         'hw-bridge-3-const-residential-bottom': 0, 'hw-bridge-3-const-residential-middle': 0,
         'hw-bridge-3-const-residential-top': 0, 'hw-bridge-4-const-residential-bottom': 0,
         'hw-bridge-4-const-residential-middle': 0, 'hw-bridge-4-const-residential-top': 0,
         'hw-bridge-5-const-residential-bottom': 0, 'hw-bridge-5-const-residential-middle': 0,
         'hw-bridge-5-const-residential-top': 0}
    ],
    'roads_service_const_bridge': [
        {'hw-bridge-1-const-service-weak': 0, 'hw-bridge-2-const-service-weak': 0,
         'hw-bridge-3-const-service-weak': 0, 'hw-bridge-4-const-service-weak': 0,
         'hw-bridge-5-const-service-weak': 0},
        {'hw-bridge-1-const-service-bottom': 0, 'hw-bridge-1-const-service-middle': 0,
         'hw-bridge-1-const-service-top': 0, 'hw-bridge-2-const-service-bottom': 0,
         'hw-bridge-2-const-service-middle': 0, 'hw-bridge-2-const-service-top': 0,
         'hw-bridge-3-const-service-bottom': 0, 'hw-bridge-3-const-service-middle': 0,
         'hw-bridge-3-const-service-top': 0, 'hw-bridge-4-const-service-bottom': 0,
         'hw-bridge-4-const-service-middle': 0, 'hw-bridge-4-const-service-top': 0,
         'hw-bridge-5-const-service-bottom': 0, 'hw-bridge-5-const-service-middle': 0,
         'hw-bridge-5-const-service-top': 0}
    ],
    'roads_motorway_link_const_bridge': [
        {'hw-bridge-1-const-link-highway-weak': 0, 'hw-bridge-2-const-link-highway-weak': 0,
         'hw-bridge-3-const-link-highway-weak': 0, 'hw-bridge-4-const-link-highway-weak': 0,
         'hw-bridge-5-const-link-highway-weak': 0},
        {'hw-bridge-1-const-link-highway-bottom': 0, 'hw-bridge-1-const-link-highway-middle': 0,
         'hw-bridge-1-const-link-highway-top': 0, 'hw-bridge-2-const-link-highway-bottom': 0,
         'hw-bridge-2-const-link-highway-middle': 0, 'hw-bridge-2-const-link-highway-top': 0,
         'hw-bridge-3-const-link-highway-bottom': 0, 'hw-bridge-3-const-link-highway-middle': 0,
         'hw-bridge-3-const-link-highway-top': 0, 'hw-bridge-4-const-link-highway-bottom': 0,
         'hw-bridge-4-const-link-highway-middle': 0, 'hw-bridge-4-const-link-highway-top': 0,
         'hw-bridge-5-const-link-highway-bottom': 0, 'hw-bridge-5-const-link-highway-middle': 0,
         'hw-bridge-5-const-link-highway-top': 0},
        {'hw-bridge-1-const-link-highway-bottom': 0, 'hw-bridge-1-const-link-highway-middle': 0,
         'hw-bridge-1-const-link-highway-top': 1, 'hw-bridge-2-const-link-highway-bottom': 0,
         'hw-bridge-2-const-link-highway-middle': 0, 'hw-bridge-2-const-link-highway-top': 1,
         'hw-bridge-3-const-link-highway-bottom': 0, 'hw-bridge-3-const-link-highway-middle': 0,
         'hw-bridge-3-const-link-highway-top': 1, 'hw-bridge-4-const-link-highway-bottom': 0,
         'hw-bridge-4-const-link-highway-middle': 0, 'hw-bridge-4-const-link-highway-top': 1,
         'hw-bridge-5-const-link-highway-bottom': 0, 'hw-bridge-5-const-link-highway-middle': 0,
         'hw-bridge-5-const-link-highway-top': 1}
    ],
    'roads_primary_link_const_bridge': [
        {'hw-bridge-1-const-link-primary-weak': 0, 'hw-bridge-2-const-link-primary-weak': 0,
         'hw-bridge-3-const-link-primary-weak': 0, 'hw-bridge-4-const-link-primary-weak': 0,
         'hw-bridge-5-const-link-primary-weak': 0},
        {'hw-bridge-1-const-link-primary-bottom': 0, 'hw-bridge-1-const-link-primary-middle': 0,
         'hw-bridge-1-const-link-primary-top': 0, 'hw-bridge-2-const-link-primary-bottom': 0,
         'hw-bridge-2-const-link-primary-middle': 0, 'hw-bridge-2-const-link-primary-top': 0,
         'hw-bridge-3-const-link-primary-bottom': 0, 'hw-bridge-3-const-link-primary-middle': 0,
         'hw-bridge-3-const-link-primary-top': 0, 'hw-bridge-4-const-link-primary-bottom': 0,
         'hw-bridge-4-const-link-primary-middle': 0, 'hw-bridge-4-const-link-primary-top': 0,
         'hw-bridge-5-const-link-primary-bottom': 0, 'hw-bridge-5-const-link-primary-middle': 0,
         'hw-bridge-5-const-link-primary-top': 0},
        {'hw-bridge-1-const-link-primary-bottom': 0, 'hw-bridge-1-const-link-primary-middle': 0,
         'hw-bridge-1-const-link-primary-top': 1, 'hw-bridge-2-const-link-primary-bottom': 0,
         'hw-bridge-2-const-link-primary-middle': 0, 'hw-bridge-2-const-link-primary-top': 1,
         'hw-bridge-3-const-link-primary-bottom': 0, 'hw-bridge-3-const-link-primary-middle': 0,
         'hw-bridge-3-const-link-primary-top': 1, 'hw-bridge-4-const-link-primary-bottom': 0,
         'hw-bridge-4-const-link-primary-middle': 0, 'hw-bridge-4-const-link-primary-top': 1,
         'hw-bridge-5-const-link-primary-bottom': 0, 'hw-bridge-5-const-link-primary-middle': 0,
         'hw-bridge-5-const-link-primary-top': 1}
    ],
    'roads_secondary_link_const_bridge': [
        {'hw-bridge-1-const-link-secondary-weak': 0, 'hw-bridge-2-const-link-secondary-weak': 0,
         'hw-bridge-3-const-link-secondary-weak': 0, 'hw-bridge-4-const-link-secondary-weak': 0,
         'hw-bridge-5-const-link-secondary-weak': 0},
        {'hw-bridge-1-const-link-secondary-bottom': 0, 'hw-bridge-1-const-link-secondary-middle': 0,
         'hw-bridge-1-const-link-secondary-top': 0, 'hw-bridge-2-const-link-secondary-bottom': 0,
         'hw-bridge-2-const-link-secondary-middle': 0, 'hw-bridge-2-const-link-secondary-top': 0,
         'hw-bridge-3-const-link-secondary-bottom': 0, 'hw-bridge-3-const-link-secondary-middle': 0,
         'hw-bridge-3-const-link-secondary-top': 0, 'hw-bridge-4-const-link-secondary-bottom': 0,
         'hw-bridge-4-const-link-secondary-middle': 0, 'hw-bridge-4-const-link-secondary-top': 0,
         'hw-bridge-5-const-link-secondary-bottom': 0, 'hw-bridge-5-const-link-secondary-middle': 0,
         'hw-bridge-5-const-link-secondary-top': 0},
        {'hw-bridge-1-const-link-secondary-bottom': 0, 'hw-bridge-1-const-link-secondary-middle': 0,
         'hw-bridge-1-const-link-secondary-top': 1, 'hw-bridge-2-const-link-secondary-bottom': 0,
         'hw-bridge-2-const-link-secondary-middle': 0, 'hw-bridge-2-const-link-secondary-top': 1,
         'hw-bridge-3-const-link-secondary-bottom': 0, 'hw-bridge-3-const-link-secondary-middle': 0,
         'hw-bridge-3-const-link-secondary-top': 1, 'hw-bridge-4-const-link-secondary-bottom': 0,
         'hw-bridge-4-const-link-secondary-middle': 0, 'hw-bridge-4-const-link-secondary-top': 1,
         'hw-bridge-5-const-link-secondary-bottom': 0, 'hw-bridge-5-const-link-secondary-middle': 0,
         'hw-bridge-5-const-link-secondary-top': 1}
    ],
    'roads_tertiary_link_const_bridge': [
        {'hw-bridge-1-const-link-tertiary-weak': 0, 'hw-bridge-2-const-link-tertiary-weak': 0,
         'hw-bridge-3-const-link-tertiary-weak': 0, 'hw-bridge-4-const-link-tertiary-weak': 0,
         'hw-bridge-5-const-link-tertiary-weak': 0},
        {'hw-bridge-1-const-link-tertiary-bottom': 0, 'hw-bridge-1-const-link-tertiary-middle': 0,
         'hw-bridge-1-const-link-tertiary-top': 0, 'hw-bridge-2-const-link-tertiary-bottom': 0,
         'hw-bridge-2-const-link-tertiary-middle': 0, 'hw-bridge-2-const-link-tertiary-top': 0,
         'hw-bridge-3-const-link-tertiary-bottom': 0, 'hw-bridge-3-const-link-tertiary-middle': 0,
         'hw-bridge-3-const-link-tertiary-top': 0, 'hw-bridge-4-const-link-tertiary-bottom': 0,
         'hw-bridge-4-const-link-tertiary-middle': 0, 'hw-bridge-4-const-link-tertiary-top': 0,
         'hw-bridge-5-const-link-tertiary-bottom': 0, 'hw-bridge-5-const-link-tertiary-middle': 0,
         'hw-bridge-5-const-link-tertiary-top': 0},
    ],
    # roads_tunnels
    'roads_motorway_tunnel': [
        {'hw-tunnel-motorway-weak': 0, 'hw-tunnel-trunk-weak': 0},
        {'hw-tunnel-motorway-bottom': 0, 'hw-tunnel-trunk-bottom': 0, 'hw-tunnel-motorway-top': 0,
         'hw-tunnel-trunk-top': 0},
        {'hw-tunnel-motorway-bottom': 1, 'hw-tunnel-trunk-bottom': 1, 'hw-tunnel-motorway-top': 1,
         'hw-tunnel-trunk-top': 1}
    ],
    'roads_primary_tunnel': [
        {'hw-tunnel-primary-weak': 0},
        {'hw-tunnel-primary-bottom': 0, 'hw-tunnel-primary-top': 0},
        {'hw-tunnel-primary-bottom': 1, 'hw-tunnel-primary-top': 1}
    ],
    'roads_secondary_tunnel': [
        {'hw-tunnel-secondary-weak': 0},
        {'hw-tunnel-secondary-bottom': 0, 'hw-tunnel-secondary-top': 0},
        {'hw-tunnel-secondary-bottom': 1, 'hw-tunnel-secondary-top': 1}
    ],
    'roads_tertiary_tunnel': [
        {'hw-tunnel-tertiary-weak': 0},
        {'hw-tunnel-tertiary-bottom': 0, 'hw-tunnel-tertiary-top': 0}
    ],
    'roads_residential_tunnel': [
        {'hw-tunnel-residential-weak': 0, 'hw-tunnel-pedestrian-weak': 0},
        {'hw-tunnel-residential-bottom': 0, 'hw-tunnel-pedestrian-bottom': 0, 'hw-tunnel-residential-top': 0,
         'hw-tunnel-pedestrian-top': 0, 'hw-tunnel-residential-private': 0}
    ],
    'roads_service_tunnel': [
        {'hw-tunnel-service-weak': 0},
        {'hw-tunnel-service-bottom': 0, 'hw-tunnel-service-top': 0, 'hw-tunnel-service-private': 0}
    ],
    'roads_track_tunnel': [
        {'hw-tunnel-track': 0}
    ],
    'roads_path_tunnel': [
        {'hw-tunnel-path': 0},
        {'hw-tunnel-path': 1}
    ],
    'roads_pavement_tunnel': [
        {'hw-tunnel-pavement': 0},
        {'hw-tunnel-pavement': 1}
    ],
    'roads_motorway_link_tunnel': [
        {'hw-tunnel-link-highway-weak': 0},
        {'hw-tunnel-link-highway-bottom': 0, 'hw-tunnel-link-highway-top': 0},
        {'hw-tunnel-link-highway-bottom': 1, 'hw-tunnel-link-highway-top': 1}
    ],
    'roads_primary_link_tunnel': [
        {'hw-tunnel-link-primary-weak': 0},
        {'hw-tunnel-link-primary-bottom': 0, 'hw-tunnel-link-primary-top': 0},
        {'hw-tunnel-link-primary-bottom': 1, 'hw-tunnel-link-primary-top': 1}
    ],
    'roads_secondary_link_tunnel': [
        {'hw-tunnel-link-secondary-weak': 0},
        {'hw-tunnel-link-secondary-bottom': 0, 'hw-tunnel-link-secondary-top': 0},
        {'hw-tunnel-link-secondary-bottom': 1, 'hw-tunnel-link-secondary-top': 1}
    ],
    'roads_tertiary_link_tunnel': [
        {'hw-tunnel-link-tertiary-weak': 0},
        {'hw-tunnel-link-tertiary-bottom': 0, 'hw-tunnel-link-tertiary-top': 0}
    ],
    # roads_construction
    'roads_motorway_const': [
        {'hw-const-motorway-weak': 0, 'hw-const-trunk-weak': 0},
        {'hw-const-highway-bottom': 0, 'hw-const-highway-middle': 0, 'hw-const-highway-top': 0},
        {'hw-const-highway-bottom': 1, 'hw-const-highway-middle': 1, 'hw-const-highway-top': 1},
    ],
    'roads_primary_const': [
        {'hw-const-primary-weak': 0},
        {'hw-const-primary-bottom': 0, 'hw-const-primary-middle': 0, 'hw-const-primary-top': 0},
        {'hw-const-primary-bottom': 1, 'hw-const-primary-middle': 1, 'hw-const-primary-top': 1},
    ],
    'roads_secondary_const': [
        {'hw-const-secondary-weak': 0},
        {'hw-const-secondary-bottom': 0, 'hw-const-secondary-middle': 0, 'hw-const-secondary-top': 0},
        {'hw-const-secondary-bottom': 1, 'hw-const-secondary-middle': 1, 'hw-const-secondary-top': 1},
    ],
    'roads_tertiary_const': [
        {'hw-const-tertiary-weak': 0},
        {'hw-const-tertiary-bottom': 0, 'hw-const-tertiary-middle': 0, 'hw-const-tertiary-top': 0},
    ],
    'roads_residential_const': [
        {'hw-const-residential-weak': 0, 'hw-const-pedestrian-weak': 0},
        {'hw-const-residential-bottom': 0, 'hw-const-residential-middle': 0, 'hw-const-residential-top': 0}
    ],
    'roads_service_const': [
        {'hw-const-service-weak': 0},
        {'hw-const-service-bottom': 0, 'hw-const-service-middle': 0, 'hw-const-service-top': 0}
    ],
    'roads_motorway_link_const': [
        {'hw-const-link-highway-weak': 0},
        {'hw-const-link-highway-bottom': 0, 'hw-const-link-highway-middle': 0, 'hw-const-link-highway-top': 0},
        {'hw-const-link-highway-bottom': 1, 'hw-const-link-highway-middle': 1, 'hw-const-link-highway-top': 1},
    ],
    'roads_primary_link_const': [
        {'hw-const-link-primary-weak': 0},
        {'hw-const-link-primary-bottom': 0, 'hw-const-link-primary-middle': 0, 'hw-const-link-primary-top': 0},
        {'hw-const-link-primary-bottom': 1, 'hw-const-link-primary-middle': 1, 'hw-const-link-primary-top': 1},
    ],
    'roads_secondary_link_const': [
        {'hw-const-link-secondary-weak': 0},
        {'hw-const-link-secondary-bottom': 0, 'hw-const-link-secondary-middle': 0, 'hw-const-link-secondary-top': 0},
        {'hw-const-link-secondary-bottom': 1, 'hw-const-link-secondary-middle': 1, 'hw-const-link-secondary-top': 1},
    ],
    'roads_tertiary_link_const': [
        {'hw-const-link-tertiary-weak': 0},
        {'hw-const-link-tertiary-bottom': 0, 'hw-const-link-tertiary-middle': 0, 'hw-const-link-tertiary-top': 0},
    ],
    'roads_signs': [
        {'hw-item-lights': 0}
    ],
    'roads_motorway_junction': [
        {'hw-junction-name': 0}
    ],
    # hw oneway
    'roads_motorway_oneway': [
        {'hw-highway-oneway': 0}
    ],
    'roads_primary_oneway': [
        {'hw-primary-oneway': 0}
    ],
    'roads_secondary_oneway': [
        {'hw-secondary-oneway': 0}
    ],
    'roads_tertiary_oneway': [
        {'hw-tertiary-oneway': 0}
    ],
    'roads_residential_oneway': [
        {'hw-residential-oneway': 0}
    ],
    'roads_service_oneway': [
        {'hw-service-oneway': 0}
    ],
    'roads_path_oneway': [
        {'hw-path-oneway': 0}
    ],
    'roads_motorway_link_oneway': [
        {'hw-highway-link-oneway': 0}
    ],
    'roads_primary_link_oneway': [
        {'hw-primary-link-oneway': 0}
    ],
    'roads_secondary_link_oneway': [
        {'hw-secondary-link-oneway': 0}
    ],
    'roads_tertiary_link_oneway': [
        {'hw-tertiary-link-oneway': 0}
    ],
    # hw names
    'roads_motorway_name': [
        {'hw-highway-name': 0}
    ],
    'roads_primary_name': [
        {'hw-primary-name': 0}
    ],
    'roads_secondary_name': [
        {'hw-secondary-name': 0}
    ],
    'roads_tertiary_name': [
        {'hw-tertiary-name': 0}
    ],
    'roads_residential_name': [
        {'hw-residential-name': 0}
    ],
    'roads_service_name': [
        {'hw-service-name': 0}
    ],
    'roads_motorway_tunnel_name': [
        {'hw-tunnel-highway-detail': 0},
        {'hw-tunnel-highway-detail': 1}
    ],
    'roads_primary_tunnel_name': [
        {'hw-tunnel-primary-detail': 0},
        {'hw-tunnel-primary-detail': 1}
    ],
    'roads_secondary_tunnel_name': [
        {'hw-tunnel-secondary-detail': 0},
        {'hw-tunnel-secondary-detail': 1}
    ],
    'roads_tertiary_tunnel_name': [
        {'hw-tunnel-tertiary-detail': 0},
        {'hw-tunnel-tertiary-detail': 1}
    ],
    'roads_motorway_bridge_name': [
        {'hw-bridge-highway-detail': 0},
        {'hw-bridge-highway-detail': 1}
    ],
    'roads_primary_bridge_name': [
        {'hw-bridge-primary-detail': 0},
        {'hw-bridge-primary-detail': 1}
    ],
    'roads_secondary_bridge_name': [
        {'hw-bridge-secondary-detail': 0},
        {'hw-bridge-secondary-detail': 1}
    ],
    'roads_tertiary_bridge_name': [
        {'hw-bridge-tertiary-detail': 0},
        {'hw-bridge-tertiary-detail': 1}
    ],

    # rail (tunnel or no tunnel - different queries)
    'rail_normal': [
        # weak
        {'rw-rail': 0},
        # basic
        {'rw-rail': 1},
        # service
        {'rw-rail-serv': 0, 'rw-rail': 1}
    ],
    'rail_special': [
        {'rw-special': 0},
        {'rw-special': 1},
        {'rw-special-serv': 0, 'rw-special': 1}
    ],
    'rail_tram': [
        {'rw-tram': 0},
        {'rw-tram-serv': 0, 'rw-tram': 0}
    ],
    'rail_subway': [
        {'rw-subway': 0},
        {'rw-subway-serv': 0, 'rw-subway': 0}
    ],
    # rail bridges
    'rail_normal_bridge': [
        {'rw-bridge-1-rail-weak-bottom': 0, 'rw-bridge-1-rail': 0, 'rw-bridge-2-rail-weak-bottom': 0,
         'rw-bridge-2-rail': 0, 'rw-bridge-3-rail-weak-bottom': 0, 'rw-bridge-3-rail': 0,
         'rw-bridge-4-rail-weak-bottom': 0, 'rw-bridge-4-rail': 0, 'rw-bridge-5-rail-weak-bottom': 0,
         'rw-bridge-5-rail': 0},
        {'rw-bridge-1-rail-bottom': 0, 'rw-bridge-1-rail-top': 0, 'rw-bridge-1-rail': 1, 'rw-bridge-2-rail-bottom': 0,
         'rw-bridge-2-rail-top': 0, 'rw-bridge-2-rail': 1, 'rw-bridge-3-rail-bottom': 0, 'rw-bridge-3-rail-top': 0,
         'rw-bridge-3-rail': 1, 'rw-bridge-4-rail-bottom': 0, 'rw-bridge-4-rail-top': 0, 'rw-bridge-4-rail': 1,
         'rw-bridge-5-rail-bottom': 0, 'rw-bridge-5-rail-top': 0, 'rw-bridge-5-rail': 1},
        {'rw-bridge-1-rail-service-bottom': 0, 'rw-bridge-1-rail-bottom': 0, 'rw-bridge-1-rail-service-top': 0,
         'rw-bridge-1-rail-top': 0, 'rw-bridge-1-rail-service': 0, 'rw-bridge-1-rail': 1,
         'rw-bridge-2-rail-service-bottom': 0, 'rw-bridge-2-rail-bottom': 0, 'rw-bridge-2-rail-service-top': 0,
         'rw-bridge-2-rail-top': 0, 'rw-bridge-2-rail-service': 0, 'rw-bridge-2-rail': 1,
         'rw-bridge-3-rail-service-bottom': 0, 'rw-bridge-3-rail-bottom': 0, 'rw-bridge-3-rail-service-top': 0,
         'rw-bridge-3-rail-top': 0, 'rw-bridge-3-rail-service': 0, 'rw-bridge-3-rail': 1,
         'rw-bridge-4-rail-service-bottom': 0, 'rw-bridge-4-rail-bottom': 0, 'rw-bridge-4-rail-service-top': 0,
         'rw-bridge-4-rail-top': 0, 'rw-bridge-4-rail-service': 0, 'rw-bridge-4-rail': 1,
         'rw-bridge-5-rail-service-bottom': 0, 'rw-bridge-5-rail-bottom': 0, 'rw-bridge-5-rail-service-top': 0,
         'rw-bridge-5-rail-top': 0, 'rw-bridge-5-rail-service': 0, 'rw-bridge-5-rail': 1}
    ],
    'rail_special_bridge': [
        {'rw-bridge-1-special-weak-bottom': 0, 'rw-bridge-1-special': 0, 'rw-bridge-2-special-weak-bottom': 0,
         'rw-bridge-2-special': 0, 'rw-bridge-3-special-weak-bottom': 0, 'rw-bridge-3-special': 0,
         'rw-bridge-4-special-weak-bottom': 0, 'rw-bridge-4-special': 0, 'rw-bridge-5-special-weak-bottom': 0,
         'rw-bridge-5-special': 0},
        {'rw-bridge-1-special-bottom': 0, 'rw-bridge-1-special-top': 0, 'rw-bridge-1-special': 1,
         'rw-bridge-2-special-bottom': 0, 'rw-bridge-2-special-top': 0, 'rw-bridge-2-special': 1,
         'rw-bridge-3-special-bottom': 0, 'rw-bridge-3-special-top': 0, 'rw-bridge-3-special': 1,
         'rw-bridge-4-special-bottom': 0, 'rw-bridge-4-special-top': 0, 'rw-bridge-4-special': 1,
         'rw-bridge-5-special-bottom': 0, 'rw-bridge-5-special-top': 0, 'rw-bridge-5-special': 1},
        {'rw-bridge-1-special-service-bottom': 0, 'rw-bridge-1-special-bottom': 0, 'rw-bridge-1-special-service-top': 0,
         'rw-bridge-1-special-top': 0, 'rw-bridge-1-special-service': 0, 'rw-bridge-1-special': 1,
         'rw-bridge-2-special-service-bottom': 0, 'rw-bridge-2-special-bottom': 0, 'rw-bridge-2-special-service-top': 0,
         'rw-bridge-2-special-top': 0, 'rw-bridge-2-special-service': 0, 'rw-bridge-2-special': 1,
         'rw-bridge-3-special-service-bottom': 0, 'rw-bridge-3-special-bottom': 0, 'rw-bridge-3-special-service-top': 0,
         'rw-bridge-3-special-top': 0, 'rw-bridge-3-special-service': 0, 'rw-bridge-3-special': 1,
         'rw-bridge-4-special-service-bottom': 0, 'rw-bridge-4-special-bottom': 0, 'rw-bridge-4-special-service-top': 0,
         'rw-bridge-4-special-top': 0, 'rw-bridge-4-special-service': 0, 'rw-bridge-4-special': 1,
         'rw-bridge-5-special-service-bottom': 0, 'rw-bridge-5-special-bottom': 0, 'rw-bridge-5-special-service-top': 0,
         'rw-bridge-5-special-top': 0, 'rw-bridge-5-special-service': 0, 'rw-bridge-5-special': 1}
    ],
    'rail_tram_bridge': [
        {'rw-bridge-1-tram-bottom': 0, 'rw-bridge-1-tram-top': 0, 'rw-bridge-1-tram': 0, 'rw-bridge-2-tram-bottom': 0,
         'rw-bridge-2-tram-top': 0, 'rw-bridge-2-tram': 0, 'rw-bridge-3-tram-bottom': 0, 'rw-bridge-3-tram-top': 0,
         'rw-bridge-3-tram': 0, 'rw-bridge-4-tram-bottom': 0, 'rw-bridge-4-tram-top': 0, 'rw-bridge-4-tram': 0,
         'rw-bridge-5-tram-bottom': 0, 'rw-bridge-5-tram-top': 0, 'rw-bridge-5-tram': 0},
        {'rw-bridge-1-tram-bottom': 0, 'rw-bridge-1-tram-top': 0, 'rw-bridge-1-tram': 0, 'rw-bridge-2-tram-bottom': 0,
         'rw-bridge-2-tram-top': 0, 'rw-bridge-2-tram': 0, 'rw-bridge-3-tram-bottom': 0, 'rw-bridge-3-tram-top': 0,
         'rw-bridge-3-tram': 0, 'rw-bridge-4-tram-bottom': 0, 'rw-bridge-4-tram-top': 0, 'rw-bridge-4-tram': 0,
         'rw-bridge-5-tram-bottom': 0, 'rw-bridge-5-tram-top': 0, 'rw-bridge-5-tram': 0,
         'rw-bridge-1-tram-service-bottom': 0, 'rw-bridge-1-tram-service-top': 0, 'rw-bridge-1-tram-service': 0,
         'rw-bridge-2-tram-service-bottom': 0, 'rw-bridge-2-tram-service-top': 0, 'rw-bridge-2-tram-service': 0,
         'rw-bridge-3-tram-service-bottom': 0, 'rw-bridge-3-tram-service-top': 0, 'rw-bridge-3-tram-service': 0,
         'rw-bridge-4-tram-service-bottom': 0, 'rw-bridge-4-tram-service-top': 0, 'rw-bridge-4-tram-service': 0,
         'rw-bridge-5-tram-service-bottom': 0, 'rw-bridge-5-tram-service-top': 0, 'rw-bridge-5-tram-service': 0}
    ],
    'rail_subway_bridge': [
        {'rw-bridge-1-subway-bottom': 0, 'rw-bridge-1-subway-top': 0, 'rw-bridge-1-subway': 0,
         'rw-bridge-2-subway-bottom': 0, 'rw-bridge-2-subway-top': 0, 'rw-bridge-2-subway': 0,
         'rw-bridge-3-subway-bottom': 0, 'rw-bridge-3-subway-top': 0, 'rw-bridge-3-subway': 0,
         'rw-bridge-4-subway-bottom': 0, 'rw-bridge-4-subway-top': 0, 'rw-bridge-4-subway': 0,
         'rw-bridge-5-subway-bottom': 0, 'rw-bridge-5-subway-top': 0, 'rw-bridge-5-subway': 0},
        {'rw-bridge-1-subway-bottom': 0, 'rw-bridge-1-subway-top': 0, 'rw-bridge-1-subway': 0,
         'rw-bridge-2-subway-bottom': 0, 'rw-bridge-2-subway-top': 0, 'rw-bridge-2-subway': 0,
         'rw-bridge-3-subway-bottom': 0, 'rw-bridge-3-subway-top': 0, 'rw-bridge-3-subway': 0,
         'rw-bridge-4-subway-bottom': 0, 'rw-bridge-4-subway-top': 0, 'rw-bridge-4-subway': 0,
         'rw-bridge-5-subway-bottom': 0, 'rw-bridge-5-subway-top': 0, 'rw-bridge-5-subway': 0,
         'rw-bridge-1-subway-service-bottom': 0, 'rw-bridge-1-subway-service-top': 0, 'rw-bridge-1-subway-service': 0,
         'rw-bridge-2-subway-service-bottom': 0, 'rw-bridge-2-subway-service-top': 0, 'rw-bridge-2-subway-service': 0,
         'rw-bridge-3-subway-service-bottom': 0, 'rw-bridge-3-subway-service-top': 0, 'rw-bridge-3-subway-service': 0,
         'rw-bridge-4-subway-service-bottom': 0, 'rw-bridge-4-subway-service-top': 0, 'rw-bridge-4-subway-service': 0,
         'rw-bridge-5-subway-service-bottom': 0, 'rw-bridge-5-subway-service-top': 0, 'rw-bridge-5-subway-service': 0}
    ],
    'rail_disused_bridge': [
        {'rw-bridge-1-disused-bottom': 0, 'rw-bridge-1-disused-top': 0, 'rw-bridge-1-disused': 0,
         'rw-bridge-2-disused-bottom': 0, 'rw-bridge-2-disused-top': 0, 'rw-bridge-2-disused': 0,
         'rw-bridge-3-disused-bottom': 0, 'rw-bridge-3-disused-top': 0, 'rw-bridge-3-disused': 0,
         'rw-bridge-4-disused-bottom': 0, 'rw-bridge-4-disused-top': 0, 'rw-bridge-4-disused': 0,
         'rw-bridge-5-disused-bottom': 0, 'rw-bridge-5-disused-top': 0, 'rw-bridge-5-disused': 0}
    ],
    'rail_construction_bridge': [
        {'rw-bridge-1-construction-bottom': 0, 'rw-bridge-1-construction-top': 0, 'rw-bridge-1-construction': 0,
         'rw-bridge-2-construction-bottom': 0, 'rw-bridge-2-construction-top': 0, 'rw-bridge-2-construction': 0,
         'rw-bridge-3-construction-bottom': 0, 'rw-bridge-3-construction-top': 0, 'rw-bridge-3-construction': 0,
         'rw-bridge-4-construction-bottom': 0, 'rw-bridge-4-construction-top': 0, 'rw-bridge-4-construction': 0,
         'rw-bridge-5-construction-bottom': 0, 'rw-bridge-5-construction-top': 0, 'rw-bridge-5-construction': 0}
    ],
    # rail tunnels
    'rail_normal_tunnel': [
        {'rw-tunnel-rail': 0},
        {'rw-tunnel-rail': 1},
        {'rw-tunnel-rail-serv': 0, 'rw-tunnel-rail': 1}
    ],
    'rail_special_tunnel': [
        {'rw-tunnel-special': 0},
        {'rw-tunnel-special': 1},
        {'rw-tunnel-special-serv': 0, 'rw-tunnel-special': 1}
    ],
    'rail_tram_tunnel': [
        {'rw-tunnel-tram': 0},
        {'rw-tunnel-tram-serv': 0, 'rw-tunnel-tram': 0}
    ],
    'rail_subway_tunnel': [
        {'rw-tunnel-subway': 0},
        {'rw-tunnel-subway-serv': 0, 'rw-tunnel-subway': 0}
    ],
    'rail_disused_tunnel': [
        {'rw-tunnel-disused': 0}
    ],
    'rail_construction': [
        {'rw-construction': 0}
    ],
    'rail_disused': [
        {'rw-disused': 0}
    ],
    'rail_station': [
        {'rw-item-station': 0},
        {'rw-item-station': 1},
        {'rw-item-station': 1, 'railway-area-platform': 0, 'railway-way-platform': 0, 'rw-item-crossing': 0}
    ],
    'rail_tram_stop': [
        {'rw-item-tram_stop': 0},
        {'rw-item-tram_stop': 1}
    ],
    # rw name
    'rail_normal_bridge_name': [
        {'rw-bridge-rail-detail': 0},
        {'rw-bridge-rail-detail': 1}
    ],
    'rail_special_bridge_name': [
        {'rw-bridge-special-detail': 0},
        {'rw-bridge-special-detail': 1}
    ],
    'rail_tram_bridge_name': [
        {'rw-bridge-tram-detail': 0},
        {'rw-bridge-tram-detail': 1}
    ],
    'rail_normal_tunnel_name': [
        {'rw-tunnel-rail-detail': 0},
        {'rw-tunnel-rail-detail': 1}
    ],
    'rail_special_tunnel_name': [
        {'rw-tunnel-special-detail': 0},
        {'rw-tunnel-special-detail': 1}
    ],
    'rail_tram_tunnel_name': [
        {'rw-tunnel-tram-detail': 0},
        {'rw-tunnel-tram-detail': 1}
    ],

    # built
    'built_buildings': [
        {'man_made-area-building': 0, 'building-area': 0},
        {'man_made-area-building': 0, 'building-area': 0, 'building-area-name': 0},
        {'man_made-area-building': 0, 'building-area': 0, 'building-area-name': 0, 'building-area-number': 0,
         'building-item-number': 0}
    ],
    'built_aerial': [
        {'man_made-way-conveyor': 0, 'aerial-way': 0},
        {'man_made-way-conveyor': 0, 'aerial-way': 0, 'aerial-way-name': 0}
    ],
    'built_statue': [
        {'tourism-item-art': 0, 'man_made-item-obelisk': 0, 'man_made-area-obelisk': 0,
         'man_made-area-tower-historic': 0,  'man_made-item-tower-historic': 0, 'amenity-item-fountain': 0,
         'amenity-area-fountain': 0},
        {'tourism-item-art': 1, 'man_made-item-obelisk': 1, 'man_made-area-obelisk': 1,
         'man_made-area-tower-historic': 1, 'man_made-item-tower-historic': 1, 'amenity-item-fountain': 1,
         'amenity-area-fountain': 1}
    ],
    'built_tower': [
        {'man_made-area-tower': 0, 'man_made-area-tall_building': 0, 'man_made-item-tower': 0,
         'man_made-item-tall_building': 0},
        {'man_made-area-tower': 1, 'man_made-area-tall_building': 0, 'man_made-item-tower': 1,
         'man_made-item-tall_building': 0}
    ],
    'built_barrier': [
        {'man_made-way-embankment': 0, 'institution-area-border': 0, 'man_made-area-bridge': 0, 'barrier-way': 0}
    ],
    'built_gate': [
        {'barrier-item': 0}
    ],
    'built_city': [
        {'amenity-area-city': 0, 'amenity-item-city': 0, 'emergency-area': 0, 'emergency-item': 0,
         'amenity-area-bin': 0, 'amenity-item-bin': 0}
    ],
    'built_nature': [
        {'tourism-item-guidepost': 0, 'leisure-area-nature': 0, 'leisure-item-nature': 0,
         'amenity-area-nature': 0, 'amenity-item-nature': 0}
    ],

    # amenity
    'amenity_shop': [
        {'shop-area-a': 0, 'shop-item-a': 0, 'shop-area-b': 0, 'shop-item-b': 0,
         'amenity-area-market': 0, 'amenity-item-market': 0, 'shop-area-c': 0,
         'shop-item-c': 0},
        {'shop-area-a': 1, 'shop-item-a': 1, 'shop-area-b': 1, 'shop-item-b': 1,
         'amenity-area-market': 1, 'amenity-item-market': 1, 'shop-area-c': 0,
         'shop-item-c': 0}
    ],
    'amenity_education': [
        {'amenity-area-school-a': 0, 'amenity-area-school-b': 0, 'amenity-area-school-c': 0,
         'amenity-item-school-a': 0, 'amenity-item-school-b': 0, 'amenity-item-school-c': 0,
         'amenity-area-library': 0, 'amenity-item-library': 0},
        {'amenity-area-school-a': 1, 'amenity-area-school-b': 1, 'amenity-area-school-c': 1,
         'amenity-item-school-a': 1, 'amenity-item-school-b': 1, 'amenity-item-school-c': 1,
         'amenity-area-library': 1, 'amenity-item-library': 1}
    ],
    'amenity_art': [
        {'amenity-area-art': 0, 'amenity-item-art': 0, 'tourism-area-museum': 0, 'tourism-item-museum': 0},
        {'amenity-area-art': 1, 'amenity-item-art': 1, 'tourism-area-museum': 1, 'tourism-item-museum': 1}
    ],
    'amenity_religion': [
        {'amenity-area-religion': 0, 'amenity-item-religion': 0},
        {'amenity-area-religion': 1, 'amenity-item-religion': 1}
    ],
    'amenity_office': [
        {'amenity-area-office': 0, 'amenity-item-office': 0, 'amenity-item-post_box': 0},
        {'amenity-area-office': 1, 'amenity-item-office': 1, 'amenity-item-post_box': 0}
    ],
    'amenity_medical': [
        {'amenity-area-health-a': 0, 'amenity-item-health-a': 0, 'amenity-area-health-b': 0,
         'amenity-item-health-b': 0},
        {'amenity-area-health-a': 1, 'amenity-item-health-a': 1, 'amenity-area-health-b': 1,
         'amenity-item-health-b': 1}
    ],
    'amenity_forces': [
        {'amenity-area-forces': 0, 'amenity-item-forces': 0},
        {'amenity-area-forces': 1, 'amenity-item-forces': 1}
    ],
    'amenity_finance': [
        {'amenity-area-bank': 0, 'amenity-item-bank': 0, 'amenity-item-atm': 0},
        {'amenity-area-bank': 1, 'amenity-item-bank': 1, 'amenity-item-atm': 0}
    ],
    'amenity_law': [
        {'amenity-area-law': 0, 'amenity-item-law': 0},
        {'amenity-area-law': 1, 'amenity-item-law': 1}
    ],
    'amenity_social': [
        {'amenity-area-social': 0, 'amenity-item-social': 0},
        {'amenity-area-social': 1, 'amenity-item-social': 1}
    ],
    'amenity_food': [
        {'amenity-area-food-a': 0, 'amenity-area-food-b': 0, 'amenity-area-food-c': 0, 'amenity-item-food-a': 0,
         'amenity-item-food-b': 0, 'amenity-item-food-c': 0, 'tourism-item-picnic': 0},
        {'amenity-area-food-a': 1, 'amenity-area-food-b': 1, 'amenity-area-food-c': 0, 'amenity-item-food-a': 1,
         'amenity-item-food-b': 1, 'amenity-item-food-c': 0, 'tourism-item-picnic': 0}
    ],
    'amenity_hotel': [
        {'tourism-area-hotel': 0, 'tourism-area-hostel': 0, 'tourism-item-hotel': 0, 'tourism-item-hostel': 0},
        {'tourism-area-hotel': 1, 'tourism-area-hostel': 1, 'tourism-item-hotel': 1, 'tourism-item-hostel': 1}
    ],
    'amenity_hut': [
        {'tourism-area-hut': 0, 'tourism-area-chalet': 0, 'tourism-item-hut': 0, 'tourism-item-chalet': 0},
        {'tourism-area-hut': 1, 'tourism-area-chalet': 0, 'tourism-item-hut': 1, 'tourism-item-chalet': 0}
    ],
    'amenity_parks': [
        {'leisure-area-park': 0},
        {'leisure-area-park': 0, 'leisure-area-park-detail': 0, 'leisure-item-park': 0}
    ],
    'amenity_playground': [
        {'leisure-area-playground': 0},
        {'leisure-area-playground': 0, 'leisure-area-playground-detail': 0, 'leisure-item-playground': 0}
    ],
    'amenity_pool': [
        {'leisure-area-aquapark': 0, 'leisure-area-pool': 0},
        {'leisure-area-aquapark': 0, 'leisure-area-pool': 0, 'leisure-area-pool-detail': 0, 'leisure-item-pool': 0},
        {'leisure-area-aquapark': 0, 'leisure-area-pool': 0, 'leisure-area-pool-detail': 1, 'leisure-item-pool': 1}
    ],
    'amenity_theme': [
        {'tourism-area-theme': 0},
        {'tourism-area-theme': 0, 'tourism-area-theme-name': 0}
    ],
    'amenity_castle': [
        {'historic-area': 0, 'historic-item': 0},
        {'historic-area': 1, 'historic-item': 1},
    ],
    'amenity_bus': [
        {'amenity-area-bus': 0, 'amenity-item-bus': 0, 'hw-item-bus_stop': 0, 'amenity-item-bus_tickets': 0},
        {'amenity-area-bus': 1, 'amenity-item-bus': 1, 'hw-item-bus_stop': 1, 'amenity-item-bus_tickets': 0}
    ],
    'amenity_parking': [
        {'amenity-item-parking': 0, 'amenity-item-parking_tickets': 0}
    ],
    'amenity_gas': [
        {'amenity-area-fuel-a': 0, 'amenity-item-fuel-a': 0, 'amenity-area-fuel-b': 0, 'amenity-item-fuel-b': 0},
        {'amenity-area-fuel-a': 1, 'amenity-item-fuel-a': 1, 'amenity-area-fuel-b': 1, 'amenity-item-fuel-b': 1}
    ],
    'amenity_aero': [
        {'aero-area-bottom': 0, 'aero-area-top': 0, 'aero-way': 0},
        {'aero-area-bottom': 0, 'aero-area-top': 0, 'aero-way': 0, 'aero-area-a': 0, 'aero-area-b': 0,
         'aero-item-b': 0},
        {'aero-area-bottom': 0, 'aero-area-top': 0, 'aero-way': 0, 'aero-area-a': 1, 'aero-area-b': 1,
         'aero-item-b': 1}
    ],
    'amenity_military': [
        {'military-area': 0},
        {'military-area': 0, 'military-area-name': 0}
    ],
    'amenity_waste': [
        {'land_use-landfill-bottom': 0},
        {'land_use-landfill-bottom': 0, 'amenity-area-waste': 0, 'amenity-item-waste': 0},
        {'land_use-landfill-bottom': 0, 'amenity-area-waste': 1, 'amenity-item-waste': 1}
    ],
    'amenity_quarry': [
        {'land_use-quarry-bottom': 0},
        {'land_use-quarry-bottom': 0, 'land_use-quarry-name': 0}
    ],
    'amenity_cemetery': [
        {'land_use-cemetery-bottom': 0},
        {'land_use-cemetery-bottom': 0, 'land_use-cemetery-name': 0}
    ],

    # sport
    'sport_racetrack': [
        {'hw-racetrack': 0}
    ],
    'sport_stadium': [
        {'leisure-area-stadium': 0},
        {'leisure-area-stadium': 0, 'leisure-area-stadium-detail': 0, 'leisure-item-stadium': 0},
        {'leisure-area-stadium': 0, 'leisure-area-stadium-detail': 1, 'leisure-item-stadium': 1}
    ],
    'sport_pitch': [
        {'leisure-area-pitch': 0},
        {'leisure-area-pitch': 0, 'leisure-area-pitch-detail': 0, 'leisure-area-fitness': 0,
         'leisure-area-horse-detail': 0, 'leisure-item-pitch': 0, 'leisure-item-fitness': 0, 'leisure-item-horse': 0},
        {'leisure-area-pitch': 0, 'leisure-area-pitch-detail': 1, 'leisure-area-fitness': 0,
         'leisure-area-horse-detail': 1, 'leisure-item-pitch': 1, 'leisure-item-fitness': 0, 'leisure-item-horse': 1}
    ],
    'sport_athletic': [
        {'leisure-area-track': 0, 'leisure-way-track': 0},
        {'leisure-area-track': 0, 'leisure-way-track': 0}
    ],
    'sport_hike': [
        {'route-hiking-red': 1, 'route-hiking-blue': 1, 'route-hiking-green': 1, 'route-hiking-yellow': 1,
         'route-hiking-other': 1},
        {'route-hiking-red': 1, 'route-hiking-blue': 1, 'route-hiking-green': 1, 'route-hiking-yellow': 1,
         'route-hiking-other': 1, 'route-hiking-red-name': 0, 'route-hiking-blue-name': 0, 'route-hiking-green-name': 0,
         'route-hiking-yellow-name': 0, 'route-hiking-other-name': 0},

        {'route-hiking-red': 0, 'route-hiking-blue': 0, 'route-hiking-green': 0, 'route-hiking-yellow': 0,
         'route-hiking-other': 0},
        {'route-hiking-red': 0, 'route-hiking-blue': 0, 'route-hiking-green': 0, 'route-hiking-yellow': 0,
         'route-hiking-other': 0, 'route-hiking-red-name': 0, 'route-hiking-blue-name': 0, 'route-hiking-green-name': 0,
         'route-hiking-yellow-name': 0, 'route-hiking-other-name': 0}
    ],
    'sport_bike': [
        {'route-cycling-generic': 0},
        {'route-cycling-black': 0, 'route-cycling-red': 0, 'route-cycling-blue': 0, 'route-cycling-green': 0,
         'route-cycling-yellow': 0, 'route-cycling-other': 0},
        {'route-cycling-generic': 0, 'route-cycling-name': 0},
        {'route-cycling-black': 0, 'route-cycling-red': 0, 'route-cycling-blue': 0, 'route-cycling-green': 0,
         'route-cycling-yellow': 0, 'route-cycling-other': 0, 'route-cycling-name': 0},

        {'route-cycling-generic': 1},
        {'route-cycling-black': 1, 'route-cycling-red': 1, 'route-cycling-blue': 1, 'route-cycling-green': 1,
         'route-cycling-yellow': 1, 'route-cycling-other': 1},
        {'route-cycling-generic': 1, 'route-cycling-name': 0},
        {'route-cycling-black': 1, 'route-cycling-red': 1, 'route-cycling-blue': 1, 'route-cycling-green': 1,
         'route-cycling-yellow': 1, 'route-cycling-other': 1, 'route-cycling-name': 0},
    ],
    'sport_ski': [
        {'land_use-ski-detail': 0},
        {'land_use-ski-detail': 1}
    ],
    'sport_piste': [
        {'route-piste-advanced': 0, 'route-piste-intermediate': 0, 'route-piste-easy': 0, 'route-piste-novice': 0,
         'ski-snow_park': 0},
        {'route-piste-advanced': 0, 'route-piste-intermediate': 0, 'route-piste-easy': 0, 'route-piste-novice': 0,
         'ski-snow_park': 0, 'route-piste-advanced-name': 0, 'route-piste-intermediate-name': 0,
         'route-piste-easy-name': 0, 'route-piste-novice-name': 0, 'ski-snow_park-name': 0}
    ],
    'sport_xcountry': [
        {'route-xcountry': 0, 'route-ski_alp': 0},
        {'route-xcountry': 0, 'route-ski_alp': 0, 'route-xcountry-name': 0, 'route-ski_alp-name': 0}
    ],
    'sport_golf': [
        {'leisure-area-golf': 0, 'leisure-area-golf-detail': 0, 'leisure-item-golf': 0},
        {'leisure-area-golf': 0, 'leisure-area-golf-detail': 1, 'leisure-item-golf': 1}
    ]
}

# dictionary with data for all available layers
layers = {
    'aero-area-bottom': {
        'order': 1,
        'styles': ['aero_way_area_bottom-basic'],
        'query': '(select way from planet_osm_polygon where "aeroway"=\'aerodrome\')'
    },
    'land_use-farm-bottom': {
        'order': 2,
        'styles': ['land_use-farm-not', 'land_use-farm-basic', 'land_use-farm-detail'],
        'query': '(select way, "landuse" from planet_osm_polygon where "landuse" in (\'farmland\', \'vineyard\', '
                 '\'orchard\', \'allotments\', \'flowerbed\', \'plant_nursery\'))'
    },
    'land_use-built-bottom': {
        'order': 3,
        'styles': ['land_use-built-basic'],
        'query': '(select way, "landuse" from planet_osm_polygon where "landuse" in (\'residential\', \'greenfield\', '
                 '\'depot\', \'garages\', \'railway\', \'religious\'))'
    },
    'land_use-built-top': {
        'order': 4,
        'styles': ['land_use-built-basic', 'land_use-built-detail'],
        'query': '(select way, "landuse" from planet_osm_polygon where "landuse" in (\'commercial\', \'industrial\', '
                 '\'retail\', \'construction\', \'education\', \'brownfield\'))'
    },
    'amenity-area-bottom': {
        'order': 5,
        'styles': ['amenity-area-bottom-education'],
        'query': '(select way from planet_osm_polygon where "amenity" in (\'university\', \'school\', '
                 '\'kindergarten\')) '
    },
    'land_use-farm-top': {
        'order': 6,
        'styles': ['land_use-farm-top-not', 'land_use-farm-top'],
        'query': '(select way from planet_osm_polygon where "landuse"=\'farmyard\')'
    },
    'land_use-natural-bottom': {
        'order': 7,
        'styles': ['land_use-natural-basic', 'land_use-natural-detail'],
        'query': '(select way, "landuse" from planet_osm_polygon where "landuse" in (\'forest\', \'meadow\', '
                 '\'grass\', \'recreation_ground\', \'village_green\'))'
    },
    'man_made-way-cutline': {
        'order': 8,
        'styles': ['man_made_way-cutline'],
        'query': '(select way from planet_osm_line where "man_made"=\'cutline\')'
    },
    'land_use-landfill-bottom': {
        'order': 9,
        'styles': ['land_use-landfill'],
        'query': '(select way from planet_osm_polygon where "landuse"=\'landfill\')'
    },
    'land_use-quarry-bottom': {
        'order': 10,
        'styles': ['land_use-quarry'],
        'query': '(select way from planet_osm_polygon where "landuse"=\'quarry\')'
    },
    'land_use-cemetery-bottom': {
        'order': 11,
        'styles': ['land_use-cemetery'],
        'query': '(select way from planet_osm_polygon where "landuse"=\'cemetery\')'
    },
    'land_use-hydro-bottom': {
        'order': 12,
        'styles': ['land_use-hydro'],
        'query': '(select way from planet_osm_polygon where "landuse" in (\'aquaculture\', \'basin\', '
                 '\'reservoir\', \'salt_pond\'))'
    },
    'leisure-area-stadium': {
        'order': 13,
        'styles': ['leisure-area-bottom-stadium'],
        'query': '(select way from planet_osm_polygon where "leisure" in (\'sports_centre\', \'stadium\'))'
    },
    'leisure-area-aquapark': {
        'order': 14,
        'styles': ['leisure-area-bottom-aquapark'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'water_park\')'
    },
    'leisure-area-golf': {
        'order': 15,
        'styles': ['leisure-area-bottom-golf'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'golf_course\')'
    },
    'leisure-area-park': {
        'order': 16,
        'styles': ['leisure-area-bottom-park'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'park\')'
    },
    'natural-area': {
        'order': 17,
        'styles': ['natural_area-basic', 'natural_area-medium', 'natural_area-detail'],
        'query': '(select way, "natural" from planet_osm_polygon where "natural" in (\'wood\', \'scree\', \'shingle\', '
                 '\'scrub\', \'heath\', \'fell\', \'grassland\', \'bare_rock\', \'glacier\', \'mud\', \'sand\', '
                 '\'beach\'))'
    },
    'hydro-lake': {
        'order': 18,
        'styles': ['natural_area-hydro-lake'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and ("water" in (\'lake\', \'oxbow\', '
                 '\'lagoon\') or "water" is null))'
    },
    'hydro-reservoir': {
        'order': 19,
        'styles': ['natural_area-hydro-reservoir'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water" in (\'reservoir\', '
                 '\'pond\', \'basin\', \'reflecting_pool\', \'moat\', \'wastewater\'))'
    },
    'hydro-river': {
        'order': 20,
        'styles': ['natural_area-hydro-river'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water"=\'river\')'
    },
    'hydro-canal': {
        'order': 21,
        'styles': ['natural_area-hydro-canal'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water" in (\'canal\', '
                 '\'ditch\', \'drain\'))'
    },
    'hydro-stream': {
        'order': 22,
        'styles': ['natural_area-hydro-stream'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water"=\'stream_pool\')'
    },
    'hydro-wetland': {
        'order': 23,
        'styles': ['natural_area-hydro-wetland'],
        'query': '(select way from planet_osm_polygon where "natural"=\'wetland\')'
    },
    'leisure-area-pitch': {
        'order': 24,
        'styles': ['leisure-area-top-pitch'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'pitch\' order by ST_Area(way, true) desc)'
    },
    'leisure-area-track': {
        'order': 25,
        'styles': ['leisure-area-top-track'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'track\' and ("surface" is null or '
                 '"surface"!=\'grass\'))'
    },
    'leisure-area-garden': {
        'order': 26,
        'styles': ['leisure-area-top-garden'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'garden\')'
    },
    'leisure-area-playground': {
        'order': 27,
        'styles': ['leisure-area-top-playground'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'playground\')'
    },
    'leisure-area-pool': {
        'order': 28,
        'styles': ['leisure-area-top-pool'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'swimming_pool\')'
    },
    'leisure-way-track': {
        'order': 29,
        'styles': ['leisure-way-track'],
        'query': '(select way from planet_osm_line where "leisure"=\'track\')'
    },
    'railway-area-platform': {
        'order': 30,
        'styles': ['railway-area-basic'],
        'query': '(select way from planet_osm_polygon where "railway"=\'platform\')'
    },
    'railway-way-platform': {
        'order': 31,
        'styles': ['railway-platform-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'platform\')'
    },
    'highway-area-service': {
        'order': 32,
        'styles': ['highway-area-service-basic'],
        'query': '(select way from planet_osm_polygon where "highway"=\'service\')'
    },
    'highway-area-pedestrian': {
        'order': 33,
        'styles': ['highway-area-pedestrian-basic'],
        'query': '(select way from planet_osm_polygon where "highway" in (\'pedestrian\', \'footway\'))'
    },
    'highway-area-parking': {
        'order': 34,
        'styles': ['amenity-area-top-parking'],
        'query': '(select way from planet_osm_polygon where "amenity"=\'parking\')'
    },
    'natural-way-tree_row': {
        'order': 35,
        'styles': ['natural_way-tree_row'],
        'query': '(select way from planet_osm_line where "natural"=\'tree_row\')'
    },
    'natural-way-ridge': {
        'order': 36,
        'styles': ['natural_way-ridge'],
        'query': '(select way, "natural" from planet_osm_line where "natural" in (\'ridge\', \'arete\'))'
    },
    'natural-way-cliff': {
        'order': 37,
        'styles': ['natural_way-cliff'],
        'query': '(select way from planet_osm_line where "natural"=\'cliff\')'
    },
    'waterway-area-dam': {
        'order': 38,
        'styles': ['waterway-area-dam'],
        'query': '(select way from planet_osm_polygon where "waterway"=\'dam\')'
    },
    'waterway-river-bottom': {
        'order': 39,
        'styles': ['waterway-river-bottom'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway"=\'river\')'
    },
    'waterway-stream-bottom': {
        'order': 40,
        'styles': ['waterway-stream-bottom'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway"=\'stream\')'
    },
    'waterway-canal-bottom': {
        'order': 41,
        'styles': ['waterway-stream-bottom'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway"=\'canal\')'
    },
    'waterway-ditch-bottom': {
        'order': 42,
        'styles': ['waterway-ditch-bottom'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway" in (\'ditch\', \'drain\'))'
    },
    'waterway-river-top': {
        'order': 43,
        'styles': ['waterway-river-top'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway"=\'river\')'
    },
    'waterway-stream-top': {
        'order': 44,
        'styles': ['waterway-stream-top'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway"=\'stream\')'
    },
    'waterway-canal-top': {
        'order': 45,
        'styles': ['waterway-stream-top'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway"=\'canal\')'
    },
    'waterway-ditch-top': {
        'order': 46,
        'styles': ['waterway-ditch-top'],
        'query': '(select way, "tunnel" from planet_osm_line where "waterway" in (\'ditch\', \'drain\'))'
    },
    'waterway-dam': {
        'order': 47,
        'styles': ['waterway-dam'],
        'query': '(select way, "waterway" from planet_osm_line where "waterway" in (\'weir\', \'dam\'))'
    },
    'hydro-lake-cover': {
        'order': 48,
        'styles': ['natural_area-hydro-lake'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and ("water" in (\'lake\', \'oxbow\', '
                 '\'lagoon\') or "water" is null))'
    },
    'hydro-reservoir-cover': {
        'order': 49,
        'styles': ['natural_area-hydro-reservoir'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water" in (\'reservoir\', '
                 '\'pond\', \'basin\', \'reflecting_pool\', \'moat\', \'wastewater\'))'
    },
    'hydro-river-cover': {
        'order': 50,
        'styles': ['natural_area-hydro-river'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water"=\'river\')'
    },
    'hydro-canal-cover': {
        'order': 51,
        'styles': ['natural_area-hydro-canal'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water" in (\'canal\', '
                 '\'ditch\', \'drain\'))'
    },
    'hydro-stream-cover': {
        'order': 52,
        'styles': ['natural_area-hydro-stream'],
        'query': '(select way from planet_osm_polygon where "natural"=\'water\' and "water"=\'stream_pool\')'
    },
    'hydro-wetland-cover': {
        'order': 53,
        'styles': ['natural_area-hydro-wetland'],
        'query': '(select way from planet_osm_polygon where "natural"=\'wetland\')'
    },
    'man_made-area-breakwater': {
        'order': 54,
        'styles': ['man_made_area-top-breakwater'],
        'query': '(select way from planet_osm_polygon where "man_made"=\'breakwater\')'
    },
    'man_made-area-building': {
        'order': 55,
        'styles': ['man_made_area-top-building'],
        'query': '(select way from planet_osm_polygon where "man_made" in (\'gasometer\', \'reservoir_covered\', '
                 '\'silo\'))'
    },
    'man_made-way-breakwater': {
        'order': 56,
        'styles': ['man_made_way-breakwater'],
        'query': '(select way, "man_made" from planet_osm_line where "man_made" in(\'breakwater\', \'pier\', \'groyne\'))'
    },
    'leisure-area-marina': {
        'order': 57,
        'styles': ['leisure-area-top-marina'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'marina\')'
    },
    'man_made-area-bridge': {
        'order': 58,
        'styles': ['man_made_area-bottom-bridge'],
        'query': '(select way from planet_osm_polygon where "man_made"=\'bridge\')'
    },
    'aero-area-top': {
        'order': 59,
        'styles': ['aero_way_area_top-basic'],
        'query': '(select way, "aeroway" from planet_osm_polygon where "aeroway" in (\'apron\', \'helipad\'))'
    },
    'building-area': {
        'order': 60,
        'styles': ['building-area-basic'],
        'query': '(select way from planet_osm_polygon where "building" is not null)'
    },
    'hw-tunnel-link-tertiary-weak': {
        'order': 61,
        'styles': ['hw-tunnel-link-tertiary-weak', 'hw-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-secondary-weak': {
        'order': 62,
        'styles': ['hw-tunnel-link-secondary-weak', 'hw-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-primary-weak': {
        'order': 63,
        'styles': ['hw-tunnel-link-primary-weak', 'hw-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-highway-weak': {
        'order': 64,
        'styles': ['hw-tunnel-link-highway-weak', 'hw-link-highway-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') '
                 'and ("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-service-weak': {
        'order': 65,
        'styles': ['hw-tunnel-service-weak', 'hw-service-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-pedestrian-weak': {
        'order': 66,
        'styles': ['hw-tunnel-pedestrian-weak', 'hw-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-residential-weak': {
        'order': 67,
        'styles': ['hw-tunnel-residential-weak', 'hw-residential-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-tertiary-weak': {
        'order': 68,
        'styles': ['hw-tunnel-tertiary-weak', 'hw-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-secondary-weak': {
        'order': 69,
        'styles': ['hw-tunnel-secondary-weak', 'hw-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-primary-weak': {
        'order': 70,
        'styles': ['hw-tunnel-primary-weak', 'hw-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-trunk-weak': {
        'order': 71,
        'styles': ['hw-tunnel-trunk-weak', 'hw-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-motorway-weak': {
        'order': 72,
        'styles': ['hw-tunnel-motorway-weak', 'hw-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-pavement': {
        'order': 73,
        'styles': ['hw-tunnel-pavement-basic', 'hw-tunnel-pavement-detail', 'hw-pavement-basic', 'hw-pavement-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'footway\', \'steps\') and '
                 '("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-path': {
        'order': 74,
        'styles': ['hw-tunnel-path-basic', 'hw-tunnel-path-detail', 'hw-path-basic', 'hw-path-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'path\', \'bridleway\', '
                 '\'cycleway\') and ("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-track': {
        'order': 75,
        'styles': ['hw-tunnel-track', 'hw-track'],
        'query': '(select way, "highway" from planet_osm_line where "highway"=\'track\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-tertiary-bottom': {
        'order': 76,
        'styles': ['hw-tunnel-link-tertiary-bottom', 'hw-link-tertiary-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway"=\'tertiary_link\' and ("tunnel" is not '
                 'null or "covered" is not null))'
    },
    'hw-tunnel-link-secondary-bottom': {
        'order': 77,
        'styles': ['hw-tunnel-link-secondary-bottom-basic', 'hw-tunnel-link-secondary-bottom',
                   'hw-link-secondary-bottom-basic', 'hw-link-secondary-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway"=\'secondary_link\' and ("tunnel" is not '
                 'null or "covered" is not null))'
    },
    'hw-tunnel-link-primary-bottom': {
        'order': 78,
        'styles': ['hw-tunnel-link-primary-bottom-basic', 'hw-tunnel-link-primary-bottom',
                   'hw-link-primary-bottom-basic', 'hw-link-primary-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway"=\'primary_link\' and ("tunnel" is not '
                 'null or "covered" is not null))'
    },
    'hw-tunnel-link-highway-bottom': {
        'order': 79,
        'styles': ['hw-tunnel-link-highway-bottom-basic', 'hw-tunnel-link-highway-bottom',
                   'hw-link-highway-bottom-basic', 'hw-link-highway-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') '
                 'and ("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-service-bottom': {
        'order': 80,
        'styles': ['hw-tunnel-service-bottom', 'hw-service-bottom'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-pedestrian-bottom': {
        'order': 81,
        'styles': ['hw-tunnel-pedestrian-bottom', 'hw-pedestrian-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-residential-bottom': {
        'order': 82,
        'styles': ['hw-tunnel-residential-bottom', 'hw-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-tertiary-bottom': {
        'order': 83,
        'styles': ['hw-tunnel-tertiary-bottom', 'hw-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-secondary-bottom': {
        'order': 84,
        'styles': ['hw-tunnel-secondary-bottom-basic', 'hw-tunnel-secondary-bottom',
                   'hw-secondary-bottom-basic', 'hw-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-primary-bottom': {
        'order': 85,
        'styles': ['hw-tunnel-primary-bottom-basic', 'hw-tunnel-primary-bottom',
                   'hw-primary-bottom-basic', 'hw-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-trunk-bottom': {
        'order': 86,
        'styles': ['hw-tunnel-trunk-bottom-basic', 'hw-tunnel-trunk-bottom',
                   'hw-trunk-bottom-basic', 'hw-trunk-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-motorway-bottom': {
        'order': 87,
        'styles': ['hw-tunnel-motorway-bottom-basic', 'hw-tunnel-motorway-bottom',
                   'hw-motorway-bottom-basic', 'hw-motorway-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-tertiary-top': {
        'order': 88,
        'styles': ['hw-tunnel-link-tertiary-top', 'hw-link-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-secondary-top': {
        'order': 89,
        'styles': ['hw-tunnel-link-secondary-top-basic', 'hw-tunnel-link-secondary-top',
                   'hw-link-secondary-top-basic', 'hw-link-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-primary-top': {
        'order': 90,
        'styles': ['hw-tunnel-link-primary-top-basic', 'hw-tunnel-link-primary-top',
                   'hw-link-primary-top-basic', 'hw-link-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-link-highway-top': {
        'order': 91,
        'styles': ['hw-tunnel-link-highway-top-basic', 'hw-tunnel-link-highway-top',
                   'hw-link-highway-top-basic', 'hw-link-highway-top'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') '
                 'and ("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-service-top': {
        'order': 92,
        'styles': ['hw-tunnel-service-top', 'hw-service-top'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-service-private': {
        'order': 93,
        'styles': ['hw-service-private'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') '
                 'and ("tunnel" is not null or "covered" is not null) and "access"=\'private\')'
    },
    'hw-tunnel-pedestrian-top': {
        'order': 94,
        'styles': ['hw-tunnel-pedestrian-top', 'hw-pedestrian-top'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-residential-top': {
        'order': 95,
        'styles': ['hw-tunnel-residential-top', 'hw-residential-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '("tunnel" is not null or "covered" is not null))'
    },
    'hw-tunnel-residential-private': {
        'order': 96,
        'styles': ['hw-residential-private'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '("tunnel" is not null or "covered" is not null) and "access"=\'private\')'
    },
    'hw-tunnel-tertiary-top': {
        'order': 97,
        'styles': ['hw-tunnel-tertiary-top', 'hw-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-secondary-top': {
        'order': 98,
        'styles': ['hw-tunnel-secondary-top-basic', 'hw-tunnel-secondary-top',
                   'hw-secondary-top-basic', 'hw-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-primary-top': {
        'order': 99,
        'styles': ['hw-tunnel-primary-top-basic', 'hw-tunnel-primary-top',
                   'hw-primary-top-basic', 'hw-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-trunk-top': {
        'order': 100,
        'styles': ['hw-tunnel-trunk-top-basic', 'hw-tunnel-trunk-top',
                   'hw-trunk-top-basic', 'hw-trunk-top'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'hw-tunnel-motorway-top': {
        'order': 101,
        'styles': ['hw-tunnel-motorway-top-basic', 'hw-tunnel-motorway-top',
                   'hw-motorway-top-basic', 'hw-motorway-top'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'rw-tunnel-disused': {
        'order': 102,
        'styles': ['rw-tunnel-disused'],
        'query': '(select way from planet_osm_line where "railway" in (\'disused\', \'abandoned\') and ("tunnel" is not null or '
                 '"covered" is not null))'
    },
    'rw-tunnel-subway-serv': {
        'order': 103,
        'styles': ['rw-tunnel-subway-serv'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and ("tunnel" is not null or '
                 '"covered" is not null) and "service" is not null)'
    },
    'rw-tunnel-tram-serv': {
        'order': 104,
        'styles': ['rw-tunnel-tram-serv'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and ("tunnel" is not null or '
                 '"covered" is not null) and "service" is not null)'
    },
    'rw-tunnel-special-serv': {
        'order': 105,
        'styles': ['rw-tunnel-special-serv'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and ("tunnel" is not null or "covered" is not null) and "service" '
                 'is not null)'
    },
    'rw-tunnel-rail-serv': {
        'order': 106,
        'styles': ['rw-tunnel-rail-serv'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and ("tunnel" is not null or '
                 '"covered" is not null) and "service" is not null)'
    },
    'rw-tunnel-subway': {
        'order': 107,
        'styles': ['rw-tunnel-subway'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and ("tunnel" is not null or '
                 '"covered" is not null) and "service" is null)'
    },
    'rw-tunnel-tram': {
        'order': 108,
        'styles': ['rw-tunnel-tram'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and ("tunnel" is not null or '
                 '"covered" is not null) and "service" is null)'
    },
    'rw-tunnel-special': {
        'order': 109,
        'styles': ['rw-tunnel-special-weak', 'rw-tunnel-special'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and ("tunnel" is not null or "covered" is not null) and "service" '
                 'is null)'
    },
    'rw-tunnel-rail': {
        'order': 110,
        'styles': ['rw-tunnel-rail-weak', 'rw-tunnel-rail'],

        'query': '(select way from planet_osm_line where "railway"=\'rail\' and ("tunnel" is not null or '
                 '"covered" is not null) and "service" is null)'
    },
    'man_made-way-embankment': {
        'order': 111,
        'styles': ['man_made_way-embankment'],
        'query': '(select way, "man_made" from planet_osm_line where "man_made" in (\'embankment\', \'snow_fence\'))'
    },
    'institution-area-border': {
        'order': 112,
        'styles': ['institution_area-border'],
        'query': '(select way from planet_osm_polygon where ("amenity" is not null or "leisure" is not null) and'
                 '"barrier" is not null)'
    },
    'barrier-way': {
        'order': 113,
        'styles': ['barrier-basic'],
        'query': '(select way, "barrier" from planet_osm_line where "barrier" in (\'city_wall\', \'wall\', '
                 '\'retaining_wall\', \'fence\', \'hedge\'))'
    },
    'aero-way': {
        'order': 114,
        'styles': ['aero_way-basic'],
        'query': '(select way, "aeroway" from planet_osm_line where "aeroway" in (\'runway\', \'taxiway\'))'
    },
    'route-hydro': {
        'order': 115,
        'styles': ['route-hydro'],
        'query': '(select way from planet_osm_line where "route"=\'ferry\')'
    },
    'hw-const-link-tertiary-weak': {
        'order': 116,
        'styles': ['hw-const-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-secondary-weak': {
        'order': 117,
        'styles': ['hw-const-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-primary-weak': {
        'order': 118,
        'styles': ['hw-const-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-highway-weak': {
        'order': 119,
        'styles': ['hw-const-link-highway-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\'){})',
        'hw_bridge': True
    },
    'hw-const-service-weak': {
        'order': 120,
        'styles': ['hw-const-service-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\'){})',
        'hw_bridge': True
    },
    'hw-const-pedestrian-weak': {
        'order': 121,
        'styles': ['hw-const-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'pedestrian\'{})',
        'hw_bridge': True
    },
    'hw-const-residential-weak': {
        'order': 122,
        'styles': ['hw-const-residential-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\'){})',
        'hw_bridge': True
    },
    'hw-const-tertiary-weak': {
        'order': 123,
        'styles': ['hw-const-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\'{})',
        'hw_bridge': True
    },
    'hw-const-secondary-weak': {
        'order': 124,
        'styles': ['hw-const-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\'{})',
        'hw_bridge': True
    },
    'hw-const-primary-weak': {
        'order': 125,
        'styles': ['hw-const-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\'{})',
        'hw_bridge': True
    },
    'hw-const-trunk-weak': {
        'order': 126,
        'styles': ['hw-const-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'trunk\'{})',
        'hw_bridge': True
    },
    'hw-const-motorway-weak': {
        'order': 127,
        'styles': ['hw-const-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'motorway\'{})',
        'hw_bridge': True
    },
    'hw-link-tertiary-weak': {
        'order': 128,
        'styles': ['hw-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-secondary-weak': {
        'order': 129,
        'styles': ['hw-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-primary-weak': {
        'order': 130,
        'styles': ['hw-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-highway-weak': {
        'order': 131,
        'styles': ['hw-link-highway-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-service-weak': {
        'order': 132,
        'styles': ['hw-service-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-pedestrian-weak': {
        'order': 133,
        'styles': ['hw-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-residential-weak': {
        'order': 134,
        'styles': ['hw-residential-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-tertiary-weak': {
        'order': 135,
        'styles': ['hw-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-secondary-weak': {
        'order': 136,
        'styles': ['hw-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-primary-weak': {
        'order': 137,
        'styles': ['hw-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-trunk-weak': {
        'order': 138,
        'styles': ['hw-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-motorway-weak': {
        'order': 139,
        'styles': ['hw-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-pavement': {
        'order': 140,
        'styles': ['hw-pavement-basic', 'hw-pavement-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'footway\', \'steps\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-path': {
        'order': 141,
        'styles': ['hw-path-basic', 'hw-path-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'path\', \'bridleway\', '
                 '\'cycleway\') {}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-track': {
        'order': 142,
        'styles': ['hw-track'],
        'query': '(select way from planet_osm_line where "highway"=\'track\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-const-link-tertiary-bottom': {
        'order': 143,
        'styles': ['hw-construction-tertiary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-secondary-bottom': {
        'order': 144,
        'styles': ['hw-construction-secondary-link-bottom-basic', 'hw-construction-secondary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-primary-bottom': {
        'order': 145,
        'styles': ['hw-construction-primary-link-bottom-basic', 'hw-construction-primary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-highway-bottom': {
        'order': 146,
        'styles': ['hw-construction-highway-link-bottom-basic', 'hw-construction-highway-link-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" '
                 'in (\'trunk_link\', \'motorway_link\'){})',
        'hw_bridge': True
    },
    'hw-const-service-bottom': {
        'order': 147,
        'styles': ['hw-construction-service-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\'){})',
        'hw_bridge': True
    },
    'hw-const-residential-bottom': {
        'order': 148,
        'styles': ['hw-construction-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\', \'pedestrian\'){})',
        'hw_bridge': True
    },
    'hw-const-tertiary-bottom': {
        'order': 149,
        'styles': ['hw-construction-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\'{})',
        'hw_bridge': True
    },
    'hw-const-secondary-bottom': {
        'order': 150,
        'styles': ['hw-construction-secondary-bottom-basic', 'hw-construction-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\'{})',
        'hw_bridge': True
    },
    'hw-const-primary-bottom': {
        'order': 151,
        'styles': ['hw-construction-primary-bottom-basic', 'hw-construction-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\'{})',
        'hw_bridge': True
    },
    'hw-const-highway-bottom': {
        'order': 152,
        'styles': ['hw-construction-highway-bottom-basic', 'hw-construction-highway-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" '
                 'in (\'trunk\', \'motorway\'){})',
        'hw_bridge': True
    },
    'hw-link-tertiary-bottom': {
        'order': 153,
        'styles': ['hw-link-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-secondary-bottom': {
        'order': 154,
        'styles': ['hw-link-secondary-bottom-basic', 'hw-link-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-primary-bottom': {
        'order': 155,
        'styles': ['hw-link-primary-bottom-basic', 'hw-link-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-highway-bottom': {
        'order': 156,
        'styles': ['hw-link-highway-bottom-basic', 'hw-link-highway-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-service-bottom': {
        'order': 157,
        'styles': ['hw-service-bottom'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-pedestrian-bottom': {
        'order': 158,
        'styles': ['hw-pedestrian-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-residential-bottom': {
        'order': 159,
        'styles': ['hw-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-tertiary-bottom': {
        'order': 160,
        'styles': ['hw-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-secondary-bottom': {
        'order': 161,
        'styles': ['hw-secondary-bottom-basic', 'hw-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-primary-bottom': {
        'order': 162,
        'styles': ['hw-primary-bottom-basic', 'hw-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-trunk-bottom': {
        'order': 163,
        'styles': ['hw-trunk-bottom-basic', 'hw-trunk-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-motorway-bottom': {
        'order': 164,
        'styles': ['hw-motorway-bottom-basic', 'hw-motorway-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-const-link-tertiary-middle': {
        'order': 165,
        'styles': ['hw-construction-tertiary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-secondary-middle': {
        'order': 166,
        'styles': ['hw-construction-secondary-link-middle-basic', 'hw-construction-secondary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-primary-middle': {
        'order': 167,
        'styles': ['hw-construction-primary-link-middle-basic', 'hw-construction-primary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-highway-middle': {
        'order': 168,
        'styles': ['hw-construction-highway-link-middle-basic', 'hw-construction-highway-link-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" '
                 'in (\'trunk_link\', \'motorway_link\'){})',
        'hw_bridge': True
    },
    'hw-const-service-middle': {
        'order': 169,
        'styles': ['hw-construction-service-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\'){})',
        'hw_bridge': True
    },
    'hw-const-residential-middle': {
        'order': 170,
        'styles': ['hw-construction-residential-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\', \'pedestrian\'){})',
        'hw_bridge': True
    },
    'hw-const-tertiary-middle': {
        'order': 171,
        'styles': ['hw-construction-tertiary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\'{})',
        'hw_bridge': True
    },
    'hw-const-secondary-middle': {
        'order': 172,
        'styles': ['hw-construction-secondary-middle-basic', 'hw-construction-secondary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\'{})',
        'hw_bridge': True
    },
    'hw-const-primary-middle': {
        'order': 173,
        'styles': ['hw-construction-primary-middle-basic', 'hw-construction-primary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\'{})',
        'hw_bridge': True
    },
    'hw-const-highway-middle': {
        'order': 174,
        'styles': ['hw-construction-highway-middle-basic', 'hw-construction-highway-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" '
                 'in (\'trunk\', \'motorway\'){})',
        'hw_bridge': True
    },
    'hw-const-link-tertiary-top': {
        'order': 175,
        'styles': ['hw-construction-tertiary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-secondary-top': {
        'order': 176,
        'styles': ['hw-construction-secondary-link-top-basic', 'hw-construction-secondary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-primary-top': {
        'order': 177,
        'styles': ['hw-construction-primary-link-top-basic', 'hw-construction-primary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\'{})',
        'hw_bridge': True
    },
    'hw-const-link-highway-top': {
        'order': 178,
        'styles': ['hw-construction-highway-link-top-basic', 'hw-construction-highway-link-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" '
                 'in (\'trunk_link\', \'motorway_link\'){})',
        'hw_bridge': True
    },
    'hw-const-service-top': {
        'order': 179,
        'styles': ['hw-construction-service-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\'){})',
        'hw_bridge': True
    },
    'hw-const-residential-top': {
        'order': 180,
        'styles': ['hw-construction-residential-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\', \'pedestrian\'){})',
        'hw_bridge': True
    },
    'hw-const-tertiary-top': {
        'order': 181,
        'styles': ['hw-construction-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\'{})',
        'hw_bridge': True
    },
    'hw-const-secondary-top': {
        'order': 182,
        'styles': ['hw-construction-secondary-top-basic', 'hw-construction-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\'{})',
        'hw_bridge': True
    },
    'hw-const-primary-top': {
        'order': 183,
        'styles': ['hw-construction-primary-top-basic', 'hw-construction-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\'{})',
        'hw_bridge': True
    },
    'hw-const-highway-top': {
        'order': 184,
        'styles': ['hw-construction-highway-top-basic', 'hw-construction-highway-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" '
                 'in (\'trunk\', \'motorway\'){})',
        'hw_bridge': True
    },
    'hw-link-tertiary-top': {
        'order': 185,
        'styles': ['hw-link-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-secondary-top': {
        'order': 186,
        'styles': ['hw-link-secondary-top-basic', 'hw-link-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-primary-top': {
        'order': 187,
        'styles': ['hw-link-primary-top-basic', 'hw-link-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-link-highway-top': {
        'order': 188,
        'styles': ['hw-link-highway-top-basic', 'hw-link-highway-top'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-service-top': {
        'order': 189,
        'styles': ['hw-service-top'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-service-private': {
        'order': 190,
        'styles': ['hw-service-private'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') '
                 'and "access"=\'private\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-pedestrian-top': {
        'order': 191,
        'styles': ['hw-pedestrian-top'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-residential-top': {
        'order': 192,
        'styles': ['hw-residential-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\'){}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-residential-private': {
        'order': 193,
        'styles': ['hw-residential-private'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"access"=\'private\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-tertiary-top': {
        'order': 194,
        'styles': ['hw-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-secondary-top': {
        'order': 195,
        'styles': ['hw-secondary-top-basic', 'hw-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-primary-top': {
        'order': 196,
        'styles': ['hw-primary-top-basic', 'hw-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-trunk-top': {
        'order': 197,
        'styles': ['hw-trunk-top-basic', 'hw-trunk-top'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-motorway-top': {
        'order': 198,
        'styles': ['hw-motorway-top-basic', 'hw-motorway-top'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\'{}{})',
        'hw_tunnel': True,
        'hw_bridge': True
    },
    'hw-racetrack': {
        'order': 199,
        'styles': ['hw-racetrack'],
        'query': '(select way from planet_osm_line where "highway"=\'raceway\')'
    },
    'rw-disused': {
        'order': 200,
        'styles': ['railway-disused-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'disused\', \'abandoned\'){}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-construction': {
        'order': 201,
        'styles': ['railway-construction-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'construction\'{})',
        'rw_bridge': True
    },
    'rw-subway-serv': {
        'order': 202,
        'styles': ['railway-subway-service'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "service" is not null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-tram-serv': {
        'order': 203,
        'styles': ['railway-tram-service'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "service" is not null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-special-serv': {
        'order': 204,
        'styles': ['railway-special-service'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "service" is not null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-rail-serv': {
        'order': 205,
        'styles': ['railway-rail-service'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "service" is not null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-subway': {
        'order': 206,
        'styles': ['railway-subway-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "service" is null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-tram': {
        'order': 207,
        'styles': ['railway-tram-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "service" is null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-special': {
        'order': 208,
        'styles': ['railway-special-weak', 'railway-special-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "service" is null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-rail': {
        'order': 209,
        'styles': ['railway-rail-weak', 'railway-rail-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "service" is null{}{})',
        'rw_tunnel': True,
        'rw_bridge': True
    },
    'rw-bridge-1-special-weak-bottom': {
        'order': 210,
        'styles': ['rw-bridge-special-weak'],
        'query': '(select way from planet_osm_line where "bridge" is not null and (("railway" in (\'funicular\', '
                 '\'light_rail\', \'narrow_gauge\', \'preserved\', \'construction\') and "service" is null) or '
                 '("railway"=\'rail\' and "service" is not null)) and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-rail-weak-bottom': {
        'order': 211,
        'styles': ['rw-bridge-rail-weak'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-disused-bottom': {
        'order': 212,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-construction-bottom': {
        'order': 213,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-subway-service-bottom': {
        'order': 214,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-tram-service-bottom': {
        'order': 215,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-special-service-bottom': {
        'order': 216,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-rail-service-bottom': {
        'order': 217,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-subway-bottom': {
        'order': 218,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-tram-bottom': {
        'order': 219,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-special-bottom': {
        'order': 220,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-rail-bottom': {
        'order': 221,
        'styles': ['rw-bridge-rail-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-disused-top': {
        'order': 222,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-construction-top': {
        'order': 223,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-subway-service-top': {
        'order': 224,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-tram-service-top': {
        'order': 225,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-special-service-top': {
        'order': 226,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-rail-service-top': {
        'order': 227,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-subway-top': {
        'order': 228,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-tram-top': {
        'order': 229,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-special-top': {
        'order': 230,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-rail-top': {
        'order': 231,
        'styles': ['rw-bridge-rail-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-tertiary-weak-bottom': {
        'order': 232,
        'styles': ['hw-link-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-secondary-weak-bottom': {
        'order': 233,
        'styles': ['hw-link-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-primary-weak-bottom': {
        'order': 234,
        'styles': ['hw-link-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-highway-weak-bottom': {
        'order': 235,
        'styles': ['hw-link-highway-bridge-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-service-weak-bottom': {
        'order': 236,
        'styles': ['hw-service-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-pedestrian-weak-bottom': {
        'order': 237,
        'styles': ['hw-pedestrian-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-residential-weak-bottom': {
        'order': 238,
        'styles': ['hw-residential-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-tertiary-weak-bottom': {
        'order': 239,
        'styles': ['hw-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-secondary-weak-bottom': {
        'order': 240,
        'styles': ['hw-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-primary-weak-bottom': {
        'order': 241,
        'styles': ['hw-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-trunk-weak-bottom': {
        'order': 242,
        'styles': ['hw-trunk-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-motorway-weak-bottom': {
        'order': 243,
        'styles': ['hw-motorway-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-tertiary-weak': {
        'order': 244,
        'styles': ['hw-const-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-secondary-weak': {
        'order': 245,
        'styles': ['hw-const-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-primary-weak': {
        'order': 246,
        'styles': ['hw-const-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-highway-weak': {
        'order': 247,
        'styles': ['hw-const-link-highway-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-service-weak': {
        'order': 248,
        'styles': ['hw-const-service-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-pedestrian-weak': {
        'order': 249,
        'styles': ['hw-const-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'pedestrian\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-residential-weak': {
        'order': 250,
        'styles': ['hw-const-residential-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-tertiary-weak': {
        'order': 251,
        'styles': ['hw-const-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-secondary-weak': {
        'order': 252,
        'styles': ['hw-const-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-primary-weak': {
        'order': 253,
        'styles': ['hw-const-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-trunk-weak': {
        'order': 254,
        'styles': ['hw-const-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'trunk\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-motorway-weak': {
        'order': 255,
        'styles': ['hw-const-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'motorway\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-tertiary-weak': {
        'order': 256,
        'styles': ['hw-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-secondary-weak': {
        'order': 257,
        'styles': ['hw-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-primary-weak': {
        'order': 258,
        'styles': ['hw-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-highway-weak': {
        'order': 259,
        'styles': ['hw-link-highway-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-service-weak': {
        'order': 260,
        'styles': ['hw-service-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-pedestrian-weak': {
        'order': 261,
        'styles': ['hw-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-residential-weak': {
        'order': 262,
        'styles': ['hw-residential-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-tertiary-weak': {
        'order': 263,
        'styles': ['hw-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-secondary-weak': {
        'order': 264,
        'styles': ['hw-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-primary-weak': {
        'order': 265,
        'styles': ['hw-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-trunk-weak': {
        'order': 266,
        'styles': ['hw-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-motorway-weak': {
        'order': 267,
        'styles': ['hw-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-pavement-bottom': {
        'order': 268,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-path-bottom': {
        'order': 269,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-track-bottom': {
        'order': 270,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-tertiary-bottom': {
        'order': 271,
        'styles': ['hw-construction-tertiary-link-bridge', 'hw-construction-tertiary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-secondary-bottom': {
        'order': 272,
        'styles': ['hw-construction-secondary-link-bridge', 'hw-construction-secondary-link-bottom-basic',
                   'hw-construction-secondary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-primary-bottom': {
        'order': 273,
        'styles': ['hw-construction-primary-link-bridge', 'hw-construction-primary-link-bottom-basic',
                   'hw-construction-primary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-highway-bottom': {
        'order': 274,
        'styles': ['hw-construction-highway-link-bridge', 'hw-construction-highway-link-bottom-basic',
                   'hw-construction-highway-link-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-service-bottom': {
        'order': 275,
        'styles': ['hw-construction-service-bridge', 'hw-construction-service-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-residential-bottom': {
        'order': 276,
        'styles': ['hw-construction-residential-bridge', 'hw-construction-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-tertiary-bottom': {
        'order': 277,
        'styles': ['hw-construction-tertiary-bridge', 'hw-construction-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-secondary-bottom': {
        'order': 278,
        'styles': ['hw-construction-secondary-bridge', 'hw-construction-secondary-bottom-basic',
                   'hw-construction-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-primary-bottom': {
        'order': 279,
        'styles': ['hw-construction-primary-bridge', 'hw-construction-primary-bottom-basic',
                   'hw-construction-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-highway-bottom': {
        'order': 280,
        'styles': ['hw-construction-highway-bridge', 'hw-construction-highway-bottom-basic',
                   'hw-construction-highway-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-tertiary-bottom': {
        'order': 281,
        'styles': ['hw-link-tertiary-bridge', 'hw-link-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-secondary-bottom': {
        'order': 282,
        'styles': ['hw-link-secondary-bridge', 'hw-link-secondary-bottom-basic', 'hw-link-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-primary-bottom': {
        'order': 283,
        'styles': ['hw-link-primary-bridge', 'hw-link-primary-bottom-basic', 'hw-link-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-highway-bottom': {
        'order': 284,
        'styles': ['hw-link-highway-bridge', 'hw-link-highway-bottom-basic', 'hw-link-highway-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-service-bottom': {
        'order': 285,
        'styles': ['hw-service-bridge', 'hw-service-bottom'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-residential-bottom': {
        'order': 286,
        'styles': ['hw-residential-bridge', 'hw-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'pedestrian\', \'residential\', '
                 '\'living_street\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-tertiary-bottom': {
        'order': 287,
        'styles': ['hw-tertiary-bridge', 'hw-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-secondary-bottom': {
        'order': 288,
        'styles': ['hw-secondary-bridge', 'hw-secondary-bottom-basic', 'hw-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-primary-bottom': {
        'order': 289,
        'styles': ['hw-primary-bridge', 'hw-primary-bottom-basic', 'hw-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-trunk-bottom': {
        'order': 290,
        'styles': ['hw-trunk-bridge', 'hw-trunk-bottom-basic', 'hw-trunk-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-motorway-bottom': {
        'order': 291,
        'styles': ['hw-motorway-bridge', 'hw-motorway-bottom-basic', 'hw-motorway-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-pavement-middle': {
        'order': 292,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-path-middle': {
        'order': 293,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-track-middle': {
        'order': 294,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-pavement': {
        'order': 295,
        'styles': ['hw-pavement-basic', 'hw-pavement-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'footway\', \'steps\') and '
                 '"bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-path': {
        'order': 296,
        'styles': ['hw-path-basic', 'hw-path-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'path\', \'bridleway\', '
                 '\'cycleway\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-track': {
        'order': 297,
        'styles': ['hw-track'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-tertiary-middle': {
        'order': 298,
        'styles': ['hw-construction-tertiary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-secondary-middle': {
        'order': 299,
        'styles': ['hw-construction-secondary-link-middle-basic', 'hw-construction-secondary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-primary-middle': {
        'order': 300,
        'styles': ['hw-construction-primary-link-middle-basic', 'hw-construction-primary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-highway-middle': {
        'order': 301,
        'styles': ['hw-construction-highway-link-middle-basic', 'hw-construction-highway-link-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-service-middle': {
        'order': 302,
        'styles': ['hw-construction-service-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-residential-middle': {
        'order': 303,
        'styles': ['hw-construction-residential-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-tertiary-middle': {
        'order': 304,
        'styles': ['hw-construction-tertiary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-secondary-middle': {
        'order': 305,
        'styles': ['hw-construction-secondary-middle-basic', 'hw-construction-secondary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-primary-middle': {
        'order': 306,
        'styles': ['hw-construction-primary-middle-basic', 'hw-construction-primary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-highway-middle': {
        'order': 307,
        'styles': ['hw-construction-highway-middle-basic', 'hw-construction-highway-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-tertiary-top': {
        'order': 308,
        'styles': ['hw-construction-tertiary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-secondary-top': {
        'order': 309,
        'styles': ['hw-construction-secondary-link-top-basic', 'hw-construction-secondary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-primary-top': {
        'order': 310,
        'styles': ['hw-construction-primary-link-top-basic', 'hw-construction-primary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-link-highway-top': {
        'order': 311,
        'styles': ['hw-construction-highway-link-top-basic', 'hw-construction-highway-link-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-service-top': {
        'order': 312,
        'styles': ['hw-construction-service-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-residential-top': {
        'order': 313,
        'styles': ['hw-construction-residential-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-tertiary-top': {
        'order': 314,
        'styles': ['hw-construction-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-secondary-top': {
        'order': 315,
        'styles': ['hw-construction-secondary-top-basic', 'hw-construction-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-primary-top': {
        'order': 316,
        'styles': ['hw-construction-primary-top-basic', 'hw-construction-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-const-highway-top': {
        'order': 317,
        'styles': ['hw-construction-highway-top-basic', 'hw-construction-highway-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-tertiary-top': {
        'order': 318,
        'styles': ['hw-link-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-secondary-top': {
        'order': 319,
        'styles': ['hw-link-secondary-top-basic', 'hw-link-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-primary-top': {
        'order': 320,
        'styles': ['hw-link-primary-top-basic', 'hw-link-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-link-highway-top': {
        'order': 321,
        'styles': ['hw-link-highway-top-basic', 'hw-link-highway-top'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-service-top': {
        'order': 322,
        'styles': ['hw-service-top'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-service-private': {
        'order': 323,
        'styles': ['hw-service-private'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '"bridge" is not null and "access"=\'private\' and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-pedestrian-top': {
        'order': 324,
        'styles': ['hw-pedestrian-top'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-residential-top': {
        'order': 325,
        'styles': ['hw-residential-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-residential-private': {
        'order': 326,
        'styles': ['hw-residential-private'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "access"=\'private\' and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-tertiary-top': {
        'order': 327,
        'styles': ['hw-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-secondary-top': {
        'order': 328,
        'styles': ['hw-secondary-top-basic', 'hw-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-primary-top': {
        'order': 329,
        'styles': ['hw-primary-top-basic', 'hw-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-trunk-top': {
        'order': 330,
        'styles': ['hw-trunk-top-basic', 'hw-trunk-top'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'hw-bridge-1-motorway-top': {
        'order': 331,
        'styles': ['hw-motorway-top-basic', 'hw-motorway-top'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-disused': {
        'order': 332,
        'styles': ['railway-disused-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'disused\', \'abandoned\') and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-construction': {
        'order': 333,
        'styles': ['railway-construction-weak', 'railway-construction-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'construction\' and "bridge" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-subway-service': {
        'order': 334,
        'styles': ['railway-subway-service'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and "service" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-tram-service': {
        'order': 335,
        'styles': ['railway-tram-service'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and "service" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-special-service': {
        'order': 336,
        'styles': ['railway-special-service'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-rail-service': {
        'order': 337,
        'styles': ['railway-rail-service'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is not null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-subway': {
        'order': 338,
        'styles': ['railway-subway-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and '
                 '"service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-tram': {
        'order': 339,
        'styles': ['railway-tram-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and '
                 '"service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-special': {
        'order': 340,
        'styles': ['railway-special-weak', 'railway-special-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-1-rail': {
        'order': 341,
        'styles': ['railway-rail-weak', 'railway-rail-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and '
                 '"service" is null and ("layer"=\'1\' or "layer" is null))'
    },
    'rw-bridge-2-special-weak-bottom': {
        'order': 342,
        'styles': ['rw-bridge-special-weak'],
        'query': '(select way from planet_osm_line where "bridge" is not null and (("railway" in (\'funicular\', '
                 '\'light_rail\', \'narrow_gauge\', \'preserved\', \'construction\') and "service" is null) or '
                 '("railway"=\'rail\' and "service" is not null)) and "layer"=\'2\')'
    },
    'rw-bridge-2-rail-weak-bottom': {
        'order': 343,
        'styles': ['rw-bridge-rail-weak'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is null and "layer"=\'2\')'
    },
    'rw-bridge-2-disused-bottom': {
        'order': 344,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'2\')'
    },
    'rw-bridge-2-construction-bottom': {
        'order': 345,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'2\')'
    },
    'rw-bridge-2-subway-service-bottom': {
        'order': 346,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-tram-service-bottom': {
        'order': 347,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-special-service-bottom': {
        'order': 348,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-rail-service-bottom': {
        'order': 349,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-subway-bottom': {
        'order': 350,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-tram-bottom': {
        'order': 351,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-special-bottom': {
        'order': 352,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-rail-bottom': {
        'order': 353,
        'styles': ['rw-bridge-rail-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'2\')'
    },
    'rw-bridge-2-disused-top': {
        'order': 354,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'2\')'
    },
    'rw-bridge-2-construction-top': {
        'order': 355,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'2\')'
    },
    'rw-bridge-2-subway-service-top': {
        'order': 356,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-tram-service-top': {
        'order': 357,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-special-service-top': {
        'order': 358,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-rail-service-top': {
        'order': 359,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-subway-top': {
        'order': 360,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-tram-top': {
        'order': 361,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-special-top': {
        'order': 362,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-rail-top': {
        'order': 363,
        'styles': ['rw-bridge-rail-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-tertiary-weak-bottom': {
        'order': 364,
        'styles': ['hw-link-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-secondary-weak-bottom': {
        'order': 365,
        'styles': ['hw-link-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-primary-weak-bottom': {
        'order': 366,
        'styles': ['hw-link-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-highway-weak-bottom': {
        'order': 367,
        'styles': ['hw-link-highway-bridge-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-service-weak-bottom': {
        'order': 368,
        'styles': ['hw-service-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-pedestrian-weak-bottom': {
        'order': 369,
        'styles': ['hw-pedestrian-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-residential-weak-bottom': {
        'order': 370,
        'styles': ['hw-residential-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-tertiary-weak-bottom': {
        'order': 371,
        'styles': ['hw-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-secondary-weak-bottom': {
        'order': 372,
        'styles': ['hw-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-primary-weak-bottom': {
        'order': 373,
        'styles': ['hw-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-trunk-weak-bottom': {
        'order': 374,
        'styles': ['hw-trunk-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-motorway-weak-bottom': {
        'order': 375,
        'styles': ['hw-motorway-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-tertiary-weak': {
        'order': 376,
        'styles': ['hw-const-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-secondary-weak': {
        'order': 377,
        'styles': ['hw-const-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-primary-weak': {
        'order': 378,
        'styles': ['hw-const-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-highway-weak': {
        'order': 379,
        'styles': ['hw-const-link-highway-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-service-weak': {
        'order': 380,
        'styles': ['hw-const-service-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-pedestrian-weak': {
        'order': 381,
        'styles': ['hw-const-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'pedestrian\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-residential-weak': {
        'order': 382,
        'styles': ['hw-const-residential-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-tertiary-weak': {
        'order': 383,
        'styles': ['hw-const-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-secondary-weak': {
        'order': 384,
        'styles': ['hw-const-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-primary-weak': {
        'order': 385,
        'styles': ['hw-const-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-trunk-weak': {
        'order': 386,
        'styles': ['hw-const-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'trunk\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-motorway-weak': {
        'order': 387,
        'styles': ['hw-const-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'motorway\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-tertiary-weak': {
        'order': 388,
        'styles': ['hw-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-secondary-weak': {
        'order': 389,
        'styles': ['hw-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-primary-weak': {
        'order': 390,
        'styles': ['hw-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-highway-weak': {
        'order': 391,
        'styles': ['hw-link-highway-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-service-weak': {
        'order': 392,
        'styles': ['hw-service-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-pedestrian-weak': {
        'order': 393,
        'styles': ['hw-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-residential-weak': {
        'order': 394,
        'styles': ['hw-residential-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-tertiary-weak': {
        'order': 395,
        'styles': ['hw-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-secondary-weak': {
        'order': 396,
        'styles': ['hw-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-primary-weak': {
        'order': 397,
        'styles': ['hw-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-trunk-weak': {
        'order': 398,
        'styles': ['hw-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-motorway-weak': {
        'order': 399,
        'styles': ['hw-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-pavement-bottom': {
        'order': 400,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'2\')'
    },
    'hw-bridge-2-path-bottom': {
        'order': 401,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-track-bottom': {
        'order': 402,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-tertiary-bottom': {
        'order': 403,
        'styles': ['hw-construction-tertiary-link-bridge', 'hw-construction-tertiary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-secondary-bottom': {
        'order': 404,
        'styles': ['hw-construction-secondary-link-bridge', 'hw-construction-secondary-link-bottom-basic',
                   'hw-construction-secondary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-primary-bottom': {
        'order': 405,
        'styles': ['hw-construction-primary-link-bridge', 'hw-construction-primary-link-bottom-basic',
                   'hw-construction-primary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-highway-bottom': {
        'order': 406,
        'styles': ['hw-construction-highway-link-bridge', 'hw-construction-highway-link-bottom-basic',
                   'hw-construction-highway-link-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-service-bottom': {
        'order': 407,
        'styles': ['hw-construction-service-bridge', 'hw-construction-service-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-residential-bottom': {
        'order': 408,
        'styles': ['hw-construction-residential-bridge', 'hw-construction-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-tertiary-bottom': {
        'order': 409,
        'styles': ['hw-construction-tertiary-bridge', 'hw-construction-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-secondary-bottom': {
        'order': 410,
        'styles': ['hw-construction-secondary-bridge', 'hw-construction-secondary-bottom-basic',
                   'hw-construction-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-primary-bottom': {
        'order': 411,
        'styles': ['hw-construction-primary-bridge', 'hw-construction-primary-bottom-basic',
                   'hw-construction-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-highway-bottom': {
        'order': 412,
        'styles': ['hw-construction-highway-bridge', 'hw-construction-highway-bottom-basic',
                   'hw-construction-highway-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-tertiary-bottom': {
        'order': 413,
        'styles': ['hw-link-tertiary-bridge', 'hw-link-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-secondary-bottom': {
        'order': 414,
        'styles': ['hw-link-secondary-bridge', 'hw-link-secondary-bottom-basic', 'hw-link-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-primary-bottom': {
        'order': 415,
        'styles': ['hw-link-primary-bridge', 'hw-link-primary-bottom-basic', 'hw-link-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-highway-bottom': {
        'order': 416,
        'styles': ['hw-link-highway-bridge', 'hw-link-highway-bottom-basic', 'hw-link-highway-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-service-bottom': {
        'order': 417,
        'styles': ['hw-service-bridge', 'hw-service-bottom'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-residential-bottom': {
        'order': 418,
        'styles': ['hw-residential-bridge', 'hw-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'pedestrian\', \'residential\', '
                 '\'living_street\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-tertiary-bottom': {
        'order': 419,
        'styles': ['hw-tertiary-bridge', 'hw-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-secondary-bottom': {
        'order': 420,
        'styles': ['hw-secondary-bridge', 'hw-secondary-bottom-basic', 'hw-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-primary-bottom': {
        'order': 421,
        'styles': ['hw-primary-bridge', 'hw-primary-bottom-basic', 'hw-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-trunk-bottom': {
        'order': 422,
        'styles': ['hw-trunk-bridge', 'hw-trunk-bottom-basic', 'hw-trunk-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-motorway-bottom': {
        'order': 423,
        'styles': ['hw-motorway-bridge', 'hw-motorway-bottom-basic', 'hw-motorway-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-pavement-middle': {
        'order': 424,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'2\')'
    },
    'hw-bridge-2-path-middle': {
        'order': 425,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-track-middle': {
        'order': 426,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-pavement': {
        'order': 427,
        'styles': ['hw-pavement-basic', 'hw-pavement-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'footway\', \'steps\') and '
                 '"bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-path': {
        'order': 428,
        'styles': ['hw-path-basic', 'hw-path-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'path\', \'bridleway\', '
                 '\'cycleway\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-track': {
        'order': 429,
        'styles': ['hw-track'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-tertiary-middle': {
        'order': 430,
        'styles': ['hw-construction-tertiary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-secondary-middle': {
        'order': 431,
        'styles': ['hw-construction-secondary-link-middle-basic', 'hw-construction-secondary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-primary-middle': {
        'order': 432,
        'styles': ['hw-construction-primary-link-middle-basic', 'hw-construction-primary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-highway-middle': {
        'order': 433,
        'styles': ['hw-construction-highway-link-middle-basic', 'hw-construction-highway-link-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-service-middle': {
        'order': 434,
        'styles': ['hw-construction-service-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-residential-middle': {
        'order': 435,
        'styles': ['hw-construction-residential-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-tertiary-middle': {
        'order': 436,
        'styles': ['hw-construction-tertiary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-secondary-middle': {
        'order': 437,
        'styles': ['hw-construction-secondary-middle-basic', 'hw-construction-secondary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-primary-middle': {
        'order': 438,
        'styles': ['hw-construction-primary-middle-basic', 'hw-construction-primary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-highway-middle': {
        'order': 439,
        'styles': ['hw-construction-highway-middle-basic', 'hw-construction-highway-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-tertiary-top': {
        'order': 440,
        'styles': ['hw-construction-tertiary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-secondary-top': {
        'order': 441,
        'styles': ['hw-construction-secondary-link-top-basic', 'hw-construction-secondary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-primary-top': {
        'order': 442,
        'styles': ['hw-construction-primary-link-top-basic', 'hw-construction-primary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-link-highway-top': {
        'order': 443,
        'styles': ['hw-construction-highway-link-top-basic', 'hw-construction-highway-link-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-service-top': {
        'order': 444,
        'styles': ['hw-construction-service-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-residential-top': {
        'order': 445,
        'styles': ['hw-construction-residential-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-tertiary-top': {
        'order': 446,
        'styles': ['hw-construction-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-secondary-top': {
        'order': 447,
        'styles': ['hw-construction-secondary-top-basic', 'hw-construction-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-primary-top': {
        'order': 448,
        'styles': ['hw-construction-primary-top-basic', 'hw-construction-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-const-highway-top': {
        'order': 449,
        'styles': ['hw-construction-highway-top-basic', 'hw-construction-highway-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-tertiary-top': {
        'order': 450,
        'styles': ['hw-link-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-secondary-top': {
        'order': 451,
        'styles': ['hw-link-secondary-top-basic', 'hw-link-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-primary-top': {
        'order': 452,
        'styles': ['hw-link-primary-top-basic', 'hw-link-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-link-highway-top': {
        'order': 453,
        'styles': ['hw-link-highway-top-basic', 'hw-link-highway-top'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-service-top': {
        'order': 454,
        'styles': ['hw-service-top'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-service-private': {
        'order': 455,
        'styles': ['hw-service-private'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'2\')'
    },
    'hw-bridge-2-pedestrian-top': {
        'order': 456,
        'styles': ['hw-pedestrian-top'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-residential-top': {
        'order': 457,
        'styles': ['hw-residential-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-residential-private': {
        'order': 458,
        'styles': ['hw-residential-private'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'2\')'
    },
    'hw-bridge-2-tertiary-top': {
        'order': 459,
        'styles': ['hw-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-secondary-top': {
        'order': 460,
        'styles': ['hw-secondary-top-basic', 'hw-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-primary-top': {
        'order': 461,
        'styles': ['hw-primary-top-basic', 'hw-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-trunk-top': {
        'order': 462,
        'styles': ['hw-trunk-top-basic', 'hw-trunk-top'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'2\')'
    },
    'hw-bridge-2-motorway-top': {
        'order': 463,
        'styles': ['hw-motorway-top-basic', 'hw-motorway-top'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-disused': {
        'order': 464,
        'styles': ['railway-disused-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'disused\', \'abandoned\') and "bridge" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-construction': {
        'order': 465,
        'styles': ['railway-construction-weak', 'railway-construction-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'construction\' and "bridge" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-subway-service': {
        'order': 466,
        'styles': ['railway-subway-service'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-tram-service': {
        'order': 467,
        'styles': ['railway-tram-service'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-special-service': {
        'order': 468,
        'styles': ['railway-special-service'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-rail-service': {
        'order': 469,
        'styles': ['railway-rail-service'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'2\')'
    },
    'rw-bridge-2-subway': {
        'order': 470,
        'styles': ['railway-subway-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-tram': {
        'order': 471,
        'styles': ['railway-tram-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-special': {
        'order': 472,
        'styles': ['railway-special-weak', 'railway-special-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is null and "layer"=\'2\')'
    },
    'rw-bridge-2-rail': {
        'order': 473,
        'styles': ['railway-rail-weak', 'railway-rail-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'2\')'
    },
    'rw-bridge-3-special-weak-bottom': {
        'order': 474,
        'styles': ['rw-bridge-special-weak'],
        'query': '(select way from planet_osm_line where "bridge" is not null and (("railway" in (\'funicular\', '
                 '\'light_rail\', \'narrow_gauge\', \'preserved\', \'construction\') and "service" is null) or '
                 '("railway"=\'rail\' and "service" is not null)) and "layer"=\'3\')'
    },
    'rw-bridge-3-rail-weak-bottom': {
        'order': 475,
        'styles': ['rw-bridge-rail-weak'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is null and "layer"=\'3\')'
    },
    'rw-bridge-3-disused-bottom': {
        'order': 476,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'3\')'
    },
    'rw-bridge-3-construction-bottom': {
        'order': 477,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'3\')'
    },
    'rw-bridge-3-subway-service-bottom': {
        'order': 478,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-tram-service-bottom': {
        'order': 479,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-special-service-bottom': {
        'order': 480,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-rail-service-bottom': {
        'order': 481,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-subway-bottom': {
        'order': 482,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-tram-bottom': {
        'order': 483,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-special-bottom': {
        'order': 484,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-rail-bottom': {
        'order': 485,
        'styles': ['rw-bridge-rail-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'3\')'
    },
    'rw-bridge-3-disused-top': {
        'order': 486,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'3\')'
    },
    'rw-bridge-3-construction-top': {
        'order': 487,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'3\')'
    },
    'rw-bridge-3-subway-service-top': {
        'order': 488,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-tram-service-top': {
        'order': 489,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-special-service-top': {
        'order': 490,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-rail-service-top': {
        'order': 491,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-subway-top': {
        'order': 492,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-tram-top': {
        'order': 493,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-special-top': {
        'order': 494,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-rail-top': {
        'order': 495,
        'styles': ['rw-bridge-rail-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-tertiary-weak-bottom': {
        'order': 496,
        'styles': ['hw-link-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-secondary-weak-bottom': {
        'order': 497,
        'styles': ['hw-link-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-primary-weak-bottom': {
        'order': 498,
        'styles': ['hw-link-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-highway-weak-bottom': {
        'order': 499,
        'styles': ['hw-link-highway-bridge-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-service-weak-bottom': {
        'order': 500,
        'styles': ['hw-service-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-pedestrian-weak-bottom': {
        'order': 501,
        'styles': ['hw-pedestrian-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-residential-weak-bottom': {
        'order': 502,
        'styles': ['hw-residential-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-tertiary-weak-bottom': {
        'order': 503,
        'styles': ['hw-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-secondary-weak-bottom': {
        'order': 504,
        'styles': ['hw-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-primary-weak-bottom': {
        'order': 505,
        'styles': ['hw-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-trunk-weak-bottom': {
        'order': 506,
        'styles': ['hw-trunk-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-motorway-weak-bottom': {
        'order': 507,
        'styles': ['hw-motorway-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-tertiary-weak': {
        'order': 508,
        'styles': ['hw-const-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-secondary-weak': {
        'order': 509,
        'styles': ['hw-const-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-primary-weak': {
        'order': 510,
        'styles': ['hw-const-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-highway-weak': {
        'order': 511,
        'styles': ['hw-const-link-highway-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-service-weak': {
        'order': 512,
        'styles': ['hw-const-service-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-pedestrian-weak': {
        'order': 513,
        'styles': ['hw-const-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'pedestrian\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-residential-weak': {
        'order': 514,
        'styles': ['hw-const-residential-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-tertiary-weak': {
        'order': 515,
        'styles': ['hw-const-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-secondary-weak': {
        'order': 516,
        'styles': ['hw-const-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-primary-weak': {
        'order': 517,
        'styles': ['hw-const-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-trunk-weak': {
        'order': 518,
        'styles': ['hw-const-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'trunk\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-motorway-weak': {
        'order': 519,
        'styles': ['hw-const-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'motorway\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-tertiary-weak': {
        'order': 520,
        'styles': ['hw-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-secondary-weak': {
        'order': 521,
        'styles': ['hw-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-primary-weak': {
        'order': 522,
        'styles': ['hw-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-highway-weak': {
        'order': 523,
        'styles': ['hw-link-highway-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-service-weak': {
        'order': 524,
        'styles': ['hw-service-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-pedestrian-weak': {
        'order': 525,
        'styles': ['hw-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-residential-weak': {
        'order': 526,
        'styles': ['hw-residential-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-tertiary-weak': {
        'order': 527,
        'styles': ['hw-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-secondary-weak': {
        'order': 528,
        'styles': ['hw-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-primary-weak': {
        'order': 529,
        'styles': ['hw-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-trunk-weak': {
        'order': 530,
        'styles': ['hw-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-motorway-weak': {
        'order': 531,
        'styles': ['hw-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-pavement-bottom': {
        'order': 532,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'3\')'
    },
    'hw-bridge-3-path-bottom': {
        'order': 533,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-track-bottom': {
        'order': 534,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-tertiary-bottom': {
        'order': 535,
        'styles': ['hw-construction-tertiary-link-bridge', 'hw-construction-tertiary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-secondary-bottom': {
        'order': 536,
        'styles': ['hw-construction-secondary-link-bridge', 'hw-construction-secondary-link-bottom-basic',
                   'hw-construction-secondary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-primary-bottom': {
        'order': 537,
        'styles': ['hw-construction-primary-link-bridge', 'hw-construction-primary-link-bottom-basic',
                   'hw-construction-primary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-highway-bottom': {
        'order': 538,
        'styles': ['hw-construction-highway-link-bridge', 'hw-construction-highway-link-bottom-basic',
                   'hw-construction-highway-link-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-service-bottom': {
        'order': 539,
        'styles': ['hw-construction-service-bridge', 'hw-construction-service-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-residential-bottom': {
        'order': 540,
        'styles': ['hw-construction-residential-bridge', 'hw-construction-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-tertiary-bottom': {
        'order': 541,
        'styles': ['hw-construction-tertiary-bridge', 'hw-construction-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-secondary-bottom': {
        'order': 542,
        'styles': ['hw-construction-secondary-bridge', 'hw-construction-secondary-bottom-basic',
                   'hw-construction-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-primary-bottom': {
        'order': 543,
        'styles': ['hw-construction-primary-bridge', 'hw-construction-primary-bottom-basic',
                   'hw-construction-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-highway-bottom': {
        'order': 544,
        'styles': ['hw-construction-highway-bridge', 'hw-construction-highway-bottom-basic',
                   'hw-construction-highway-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-tertiary-bottom': {
        'order': 545,
        'styles': ['hw-link-tertiary-bridge', 'hw-link-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-secondary-bottom': {
        'order': 546,
        'styles': ['hw-link-secondary-bridge', 'hw-link-secondary-bottom-basic', 'hw-link-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-primary-bottom': {
        'order': 547,
        'styles': ['hw-link-primary-bridge', 'hw-link-primary-bottom-basic', 'hw-link-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-highway-bottom': {
        'order': 548,
        'styles': ['hw-link-highway-bridge', 'hw-link-highway-bottom-basic', 'hw-link-highway-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-service-bottom': {
        'order': 549,
        'styles': ['hw-service-bridge', 'hw-service-bottom'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-residential-bottom': {
        'order': 550,
        'styles': ['hw-residential-bridge', 'hw-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'pedestrian\', \'residential\', '
                 '\'living_street\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-tertiary-bottom': {
        'order': 551,
        'styles': ['hw-tertiary-bridge', 'hw-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-secondary-bottom': {
        'order': 552,
        'styles': ['hw-secondary-bridge', 'hw-secondary-bottom-basic', 'hw-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-primary-bottom': {
        'order': 553,
        'styles': ['hw-primary-bridge', 'hw-primary-bottom-basic', 'hw-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-trunk-bottom': {
        'order': 554,
        'styles': ['hw-trunk-bridge', 'hw-trunk-bottom-basic', 'hw-trunk-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-motorway-bottom': {
        'order': 555,
        'styles': ['hw-motorway-bridge', 'hw-motorway-bottom-basic', 'hw-motorway-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-pavement-middle': {
        'order': 556,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'3\')'
    },
    'hw-bridge-3-path-middle': {
        'order': 557,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-track-middle': {
        'order': 558,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-pavement': {
        'order': 559,
        'styles': ['hw-pavement-basic', 'hw-pavement-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'footway\', \'steps\') and '
                 '"bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-path': {
        'order': 560,
        'styles': ['hw-path-basic', 'hw-path-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'path\', \'bridleway\', '
                 '\'cycleway\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-track': {
        'order': 561,
        'styles': ['hw-track'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-tertiary-middle': {
        'order': 562,
        'styles': ['hw-construction-tertiary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-secondary-middle': {
        'order': 563,
        'styles': ['hw-construction-secondary-link-middle-basic', 'hw-construction-secondary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-primary-middle': {
        'order': 564,
        'styles': ['hw-construction-primary-link-middle-basic', 'hw-construction-primary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-highway-middle': {
        'order': 565,
        'styles': ['hw-construction-highway-link-middle-basic', 'hw-construction-highway-link-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-service-middle': {
        'order': 566,
        'styles': ['hw-construction-service-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-residential-middle': {
        'order': 567,
        'styles': ['hw-construction-residential-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-tertiary-middle': {
        'order': 568,
        'styles': ['hw-construction-tertiary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-secondary-middle': {
        'order': 569,
        'styles': ['hw-construction-secondary-middle-basic', 'hw-construction-secondary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-primary-middle': {
        'order': 570,
        'styles': ['hw-construction-primary-middle-basic', 'hw-construction-primary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-highway-middle': {
        'order': 571,
        'styles': ['hw-construction-highway-middle-basic', 'hw-construction-highway-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-tertiary-top': {
        'order': 572,
        'styles': ['hw-construction-tertiary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-secondary-top': {
        'order': 573,
        'styles': ['hw-construction-secondary-link-top-basic', 'hw-construction-secondary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-primary-top': {
        'order': 574,
        'styles': ['hw-construction-primary-link-top-basic', 'hw-construction-primary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-link-highway-top': {
        'order': 575,
        'styles': ['hw-construction-highway-link-top-basic', 'hw-construction-highway-link-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-service-top': {
        'order': 576,
        'styles': ['hw-construction-service-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-residential-top': {
        'order': 577,
        'styles': ['hw-construction-residential-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-tertiary-top': {
        'order': 578,
        'styles': ['hw-construction-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-secondary-top': {
        'order': 579,
        'styles': ['hw-construction-secondary-top-basic', 'hw-construction-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-primary-top': {
        'order': 580,
        'styles': ['hw-construction-primary-top-basic', 'hw-construction-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-const-highway-top': {
        'order': 581,
        'styles': ['hw-construction-highway-top-basic', 'hw-construction-highway-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-tertiary-top': {
        'order': 582,
        'styles': ['hw-link-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-secondary-top': {
        'order': 583,
        'styles': ['hw-link-secondary-top-basic', 'hw-link-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-primary-top': {
        'order': 584,
        'styles': ['hw-link-primary-top-basic', 'hw-link-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-link-highway-top': {
        'order': 585,
        'styles': ['hw-link-highway-top-basic', 'hw-link-highway-top'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-service-top': {
        'order': 586,
        'styles': ['hw-service-top'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-service-private': {
        'order': 587,
        'styles': ['hw-service-private'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'3\')'
    },
    'hw-bridge-3-pedestrian-top': {
        'order': 588,
        'styles': ['hw-pedestrian-top'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-residential-top': {
        'order': 589,
        'styles': ['hw-residential-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-residential-private': {
        'order': 590,
        'styles': ['hw-residential-private'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'3\')'
    },
    'hw-bridge-3-tertiary-top': {
        'order': 591,
        'styles': ['hw-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-secondary-top': {
        'order': 592,
        'styles': ['hw-secondary-top-basic', 'hw-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-primary-top': {
        'order': 593,
        'styles': ['hw-primary-top-basic', 'hw-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-trunk-top': {
        'order': 594,
        'styles': ['hw-trunk-top-basic', 'hw-trunk-top'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'3\')'
    },
    'hw-bridge-3-motorway-top': {
        'order': 595,
        'styles': ['hw-motorway-top-basic', 'hw-motorway-top'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-disused': {
        'order': 596,
        'styles': ['railway-disused-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'disused\', \'abandoned\') and "bridge" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-construction': {
        'order': 597,
        'styles': ['railway-construction-weak', 'railway-construction-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'construction\' and "bridge" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-subway-service': {
        'order': 598,
        'styles': ['railway-subway-service'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-tram-service': {
        'order': 599,
        'styles': ['railway-tram-service'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-special-service': {
        'order': 600,
        'styles': ['railway-special-service'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-rail-service': {
        'order': 601,
        'styles': ['railway-rail-service'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'3\')'
    },
    'rw-bridge-3-subway': {
        'order': 602,
        'styles': ['railway-subway-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-tram': {
        'order': 603,
        'styles': ['railway-tram-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-special': {
        'order': 604,
        'styles': ['railway-special-weak', 'railway-special-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is null and "layer"=\'3\')'
    },
    'rw-bridge-3-rail': {
        'order': 605,
        'styles': ['railway-rail-weak', 'railway-rail-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'3\')'
    },
    'rw-bridge-4-special-weak-bottom': {
        'order': 606,
        'styles': ['rw-bridge-special-weak'],
        'query': '(select way from planet_osm_line where "bridge" is not null and (("railway" in (\'funicular\', '
                 '\'light_rail\', \'narrow_gauge\', \'preserved\', \'construction\') and "service" is null) or '
                 '("railway"=\'rail\' and "service" is not null)) and "layer"=\'4\')'
    },
    'rw-bridge-4-rail-weak-bottom': {
        'order': 607,
        'styles': ['rw-bridge-rail-weak'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is null and "layer"=\'4\')'
    },
    'rw-bridge-4-disused-bottom': {
        'order': 608,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'4\')'
    },
    'rw-bridge-4-construction-bottom': {
        'order': 609,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'4\')'
    },
    'rw-bridge-4-subway-service-bottom': {
        'order': 610,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-tram-service-bottom': {
        'order': 611,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-special-service-bottom': {
        'order': 612,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-rail-service-bottom': {
        'order': 613,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-subway-bottom': {
        'order': 614,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-tram-bottom': {
        'order': 615,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-special-bottom': {
        'order': 616,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-rail-bottom': {
        'order': 617,
        'styles': ['rw-bridge-rail-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'4\')'
    },
    'rw-bridge-4-disused-top': {
        'order': 618,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'4\')'
    },
    'rw-bridge-4-construction-top': {
        'order': 619,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'4\')'
    },
    'rw-bridge-4-subway-service-top': {
        'order': 620,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-tram-service-top': {
        'order': 621,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-special-service-top': {
        'order': 622,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-rail-service-top': {
        'order': 623,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-subway-top': {
        'order': 624,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-tram-top': {
        'order': 625,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-special-top': {
        'order': 626,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-rail-top': {
        'order': 627,
        'styles': ['rw-bridge-rail-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-tertiary-weak-bottom': {
        'order': 628,
        'styles': ['hw-link-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-secondary-weak-bottom': {
        'order': 629,
        'styles': ['hw-link-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-primary-weak-bottom': {
        'order': 630,
        'styles': ['hw-link-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-highway-weak-bottom': {
        'order': 631,
        'styles': ['hw-link-highway-bridge-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-service-weak-bottom': {
        'order': 632,
        'styles': ['hw-service-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-pedestrian-weak-bottom': {
        'order': 633,
        'styles': ['hw-pedestrian-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-residential-weak-bottom': {
        'order': 634,
        'styles': ['hw-residential-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-tertiary-weak-bottom': {
        'order': 635,
        'styles': ['hw-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-secondary-weak-bottom': {
        'order': 636,
        'styles': ['hw-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-primary-weak-bottom': {
        'order': 637,
        'styles': ['hw-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-trunk-weak-bottom': {
        'order': 638,
        'styles': ['hw-trunk-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-motorway-weak-bottom': {
        'order': 639,
        'styles': ['hw-motorway-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-tertiary-weak': {
        'order': 640,
        'styles': ['hw-const-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-secondary-weak': {
        'order': 641,
        'styles': ['hw-const-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-primary-weak': {
        'order': 642,
        'styles': ['hw-const-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-highway-weak': {
        'order': 643,
        'styles': ['hw-const-link-highway-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-service-weak': {
        'order': 644,
        'styles': ['hw-const-service-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-pedestrian-weak': {
        'order': 645,
        'styles': ['hw-const-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'pedestrian\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-residential-weak': {
        'order': 646,
        'styles': ['hw-const-residential-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-tertiary-weak': {
        'order': 647,
        'styles': ['hw-const-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-secondary-weak': {
        'order': 648,
        'styles': ['hw-const-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-primary-weak': {
        'order': 649,
        'styles': ['hw-const-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-trunk-weak': {
        'order': 650,
        'styles': ['hw-const-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'trunk\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-motorway-weak': {
        'order': 651,
        'styles': ['hw-const-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'motorway\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-tertiary-weak': {
        'order': 652,
        'styles': ['hw-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-secondary-weak': {
        'order': 653,
        'styles': ['hw-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-primary-weak': {
        'order': 654,
        'styles': ['hw-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-highway-weak': {
        'order': 655,
        'styles': ['hw-link-highway-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-service-weak': {
        'order': 656,
        'styles': ['hw-service-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-pedestrian-weak': {
        'order': 657,
        'styles': ['hw-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-residential-weak': {
        'order': 658,
        'styles': ['hw-residential-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-tertiary-weak': {
        'order': 659,
        'styles': ['hw-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-secondary-weak': {
        'order': 660,
        'styles': ['hw-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-primary-weak': {
        'order': 661,
        'styles': ['hw-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-trunk-weak': {
        'order': 662,
        'styles': ['hw-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-motorway-weak': {
        'order': 663,
        'styles': ['hw-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-pavement-bottom': {
        'order': 664,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'4\')'
    },
    'hw-bridge-4-path-bottom': {
        'order': 665,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-track-bottom': {
        'order': 666,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-tertiary-bottom': {
        'order': 667,
        'styles': ['hw-construction-tertiary-link-bridge', 'hw-construction-tertiary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-secondary-bottom': {
        'order': 668,
        'styles': ['hw-construction-secondary-link-bridge', 'hw-construction-secondary-link-bottom-basic',
                   'hw-construction-secondary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-primary-bottom': {
        'order': 669,
        'styles': ['hw-construction-primary-link-bridge', 'hw-construction-primary-link-bottom-basic',
                   'hw-construction-primary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-highway-bottom': {
        'order': 670,
        'styles': ['hw-construction-highway-link-bridge', 'hw-construction-highway-link-bottom-basic',
                   'hw-construction-highway-link-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-service-bottom': {
        'order': 671,
        'styles': ['hw-construction-service-bridge', 'hw-construction-service-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-residential-bottom': {
        'order': 672,
        'styles': ['hw-construction-residential-bridge', 'hw-construction-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-tertiary-bottom': {
        'order': 673,
        'styles': ['hw-construction-tertiary-bridge', 'hw-construction-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-secondary-bottom': {
        'order': 674,
        'styles': ['hw-construction-secondary-bridge', 'hw-construction-secondary-bottom-basic',
                   'hw-construction-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-primary-bottom': {
        'order': 675,
        'styles': ['hw-construction-primary-bridge', 'hw-construction-primary-bottom-basic',
                   'hw-construction-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-highway-bottom': {
        'order': 676,
        'styles': ['hw-construction-highway-bridge', 'hw-construction-highway-bottom-basic',
                   'hw-construction-highway-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-tertiary-bottom': {
        'order': 677,
        'styles': ['hw-link-tertiary-bridge', 'hw-link-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-secondary-bottom': {
        'order': 678,
        'styles': ['hw-link-secondary-bridge', 'hw-link-secondary-bottom-basic', 'hw-link-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-primary-bottom': {
        'order': 679,
        'styles': ['hw-link-primary-bridge', 'hw-link-primary-bottom-basic', 'hw-link-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-highway-bottom': {
        'order': 680,
        'styles': ['hw-link-highway-bridge', 'hw-link-highway-bottom-basic', 'hw-link-highway-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-service-bottom': {
        'order': 681,
        'styles': ['hw-service-bridge', 'hw-service-bottom'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-residential-bottom': {
        'order': 682,
        'styles': ['hw-residential-bridge', 'hw-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'pedestrian\', \'residential\', '
                 '\'living_street\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-tertiary-bottom': {
        'order': 683,
        'styles': ['hw-tertiary-bridge', 'hw-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-secondary-bottom': {
        'order': 684,
        'styles': ['hw-secondary-bridge', 'hw-secondary-bottom-basic', 'hw-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-primary-bottom': {
        'order': 685,
        'styles': ['hw-primary-bridge', 'hw-primary-bottom-basic', 'hw-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-trunk-bottom': {
        'order': 686,
        'styles': ['hw-trunk-bridge', 'hw-trunk-bottom-basic', 'hw-trunk-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-motorway-bottom': {
        'order': 687,
        'styles': ['hw-motorway-bridge', 'hw-motorway-bottom-basic', 'hw-motorway-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-pavement-middle': {
        'order': 688,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'4\')'
    },
    'hw-bridge-4-path-middle': {
        'order': 689,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-track-middle': {
        'order': 690,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-pavement': {
        'order': 691,
        'styles': ['hw-pavement-basic', 'hw-pavement-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'footway\', \'steps\') and '
                 '"bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-path': {
        'order': 692,
        'styles': ['hw-path-basic', 'hw-path-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'path\', \'bridleway\', '
                 '\'cycleway\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-track': {
        'order': 693,
        'styles': ['hw-track'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-tertiary-middle': {
        'order': 694,
        'styles': ['hw-construction-tertiary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-secondary-middle': {
        'order': 695,
        'styles': ['hw-construction-secondary-link-middle-basic', 'hw-construction-secondary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-primary-middle': {
        'order': 696,
        'styles': ['hw-construction-primary-link-middle-basic', 'hw-construction-primary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-highway-middle': {
        'order': 697,
        'styles': ['hw-construction-highway-link-middle-basic', 'hw-construction-highway-link-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-service-middle': {
        'order': 698,
        'styles': ['hw-construction-service-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-residential-middle': {
        'order': 699,
        'styles': ['hw-construction-residential-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-tertiary-middle': {
        'order': 700,
        'styles': ['hw-construction-tertiary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-secondary-middle': {
        'order': 701,
        'styles': ['hw-construction-secondary-middle-basic', 'hw-construction-secondary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-primary-middle': {
        'order': 702,
        'styles': ['hw-construction-primary-middle-basic', 'hw-construction-primary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-highway-middle': {
        'order': 703,
        'styles': ['hw-construction-highway-middle-basic', 'hw-construction-highway-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-tertiary-top': {
        'order': 704,
        'styles': ['hw-construction-tertiary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-secondary-top': {
        'order': 705,
        'styles': ['hw-construction-secondary-link-top-basic', 'hw-construction-secondary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-primary-top': {
        'order': 706,
        'styles': ['hw-construction-primary-link-top-basic', 'hw-construction-primary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-link-highway-top': {
        'order': 707,
        'styles': ['hw-construction-highway-link-top-basic', 'hw-construction-highway-link-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-service-top': {
        'order': 708,
        'styles': ['hw-construction-service-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-residential-top': {
        'order': 709,
        'styles': ['hw-construction-residential-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-tertiary-top': {
        'order': 710,
        'styles': ['hw-construction-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-secondary-top': {
        'order': 711,
        'styles': ['hw-construction-secondary-top-basic', 'hw-construction-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-primary-top': {
        'order': 712,
        'styles': ['hw-construction-primary-top-basic', 'hw-construction-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-const-highway-top': {
        'order': 713,
        'styles': ['hw-construction-highway-top-basic', 'hw-construction-highway-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-tertiary-top': {
        'order': 714,
        'styles': ['hw-link-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-secondary-top': {
        'order': 715,
        'styles': ['hw-link-secondary-top-basic', 'hw-link-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-primary-top': {
        'order': 716,
        'styles': ['hw-link-primary-top-basic', 'hw-link-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-link-highway-top': {
        'order': 717,
        'styles': ['hw-link-highway-top-basic', 'hw-link-highway-top'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-service-top': {
        'order': 718,
        'styles': ['hw-service-top'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-service-private': {
        'order': 719,
        'styles': ['hw-service-private'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'4\')'
    },
    'hw-bridge-4-pedestrian-top': {
        'order': 720,
        'styles': ['hw-pedestrian-top'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-residential-top': {
        'order': 721,
        'styles': ['hw-residential-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-residential-private': {
        'order': 722,
        'styles': ['hw-residential-private'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'4\')'
    },
    'hw-bridge-4-tertiary-top': {
        'order': 723,
        'styles': ['hw-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-secondary-top': {
        'order': 724,
        'styles': ['hw-secondary-top-basic', 'hw-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-primary-top': {
        'order': 725,
        'styles': ['hw-primary-top-basic', 'hw-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-trunk-top': {
        'order': 726,
        'styles': ['hw-trunk-top-basic', 'hw-trunk-top'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'4\')'
    },
    'hw-bridge-4-motorway-top': {
        'order': 727,
        'styles': ['hw-motorway-top-basic', 'hw-motorway-top'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-disused': {
        'order': 728,
        'styles': ['railway-disused-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'disused\', \'abandoned\') and "bridge" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-construction': {
        'order': 729,
        'styles': ['railway-construction-weak', 'railway-construction-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'construction\' and "bridge" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-subway-service': {
        'order': 730,
        'styles': ['railway-subway-service'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-tram-service': {
        'order': 731,
        'styles': ['railway-tram-service'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-special-service': {
        'order': 732,
        'styles': ['railway-special-service'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-rail-service': {
        'order': 733,
        'styles': ['railway-rail-service'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'4\')'
    },
    'rw-bridge-4-subway': {
        'order': 734,
        'styles': ['railway-subway-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-tram': {
        'order': 735,
        'styles': ['railway-tram-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-special': {
        'order': 736,
        'styles': ['railway-special-weak', 'railway-special-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is null and "layer"=\'4\')'
    },
    'rw-bridge-4-rail': {
        'order': 737,
        'styles': ['railway-rail-weak', 'railway-rail-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'4\')'
    },
    'rw-bridge-5-special-weak-bottom': {
        'order': 738,
        'styles': ['rw-bridge-special-weak'],
        'query': '(select way from planet_osm_line where "bridge" is not null and (("railway" in (\'funicular\', '
                 '\'light_rail\', \'narrow_gauge\', \'preserved\', \'construction\') and "service" is null) or '
                 '("railway"=\'rail\' and "service" is not null)) and "layer"=\'5\')'
    },
    'rw-bridge-5-rail-weak-bottom': {
        'order': 739,
        'styles': ['rw-bridge-rail-weak'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is null and "layer"=\'5\')'
    },
    'rw-bridge-5-disused-bottom': {
        'order': 740,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'5\')'
    },
    'rw-bridge-5-construction-bottom': {
        'order': 741,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'5\')'
    },
    'rw-bridge-5-subway-service-bottom': {
        'order': 742,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-tram-service-bottom': {
        'order': 743,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-special-service-bottom': {
        'order': 744,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-rail-service-bottom': {
        'order': 745,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-subway-bottom': {
        'order': 746,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-tram-bottom': {
        'order': 747,
        'styles': ['rw-bridge-tram-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-special-bottom': {
        'order': 748,
        'styles': ['rw-bridge-special-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-rail-bottom': {
        'order': 749,
        'styles': ['rw-bridge-rail-bottom'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'5\')'
    },
    'rw-bridge-5-disused-top': {
        'order': 750,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'disused\', \'abandoned\') and "layer"=\'5\')'
    },
    'rw-bridge-5-construction-top': {
        'order': 751,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'construction\' and "layer"=\'5\')'
    },
    'rw-bridge-5-subway-service-top': {
        'order': 752,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-tram-service-top': {
        'order': 753,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-special-service-top': {
        'order': 754,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-rail-service-top': {
        'order': 755,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and '
                 '"service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-subway-top': {
        'order': 756,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'subway\' and '
                 '"service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-tram-top': {
        'order': 757,
        'styles': ['rw-bridge-tram-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'tram\' and '
                 '"service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-special-top': {
        'order': 758,
        'styles': ['rw-bridge-special-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway" in (\'funicular\', '
                 '\'light_rail\', \'monorail\', \'narrow_gauge\', \'preserved\') and "service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-rail-top': {
        'order': 759,
        'styles': ['rw-bridge-rail-top'],
        'query': '(select way from planet_osm_line where "bridge" is not null and "railway"=\'rail\' and "service" '
                 'is null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-tertiary-weak-bottom': {
        'order': 760,
        'styles': ['hw-link-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-secondary-weak-bottom': {
        'order': 761,
        'styles': ['hw-link-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-primary-weak-bottom': {
        'order': 762,
        'styles': ['hw-link-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-highway-weak-bottom': {
        'order': 763,
        'styles': ['hw-link-highway-bridge-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-service-weak-bottom': {
        'order': 764,
        'styles': ['hw-service-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-pedestrian-weak-bottom': {
        'order': 765,
        'styles': ['hw-pedestrian-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-residential-weak-bottom': {
        'order': 766,
        'styles': ['hw-residential-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-tertiary-weak-bottom': {
        'order': 767,
        'styles': ['hw-tertiary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-secondary-weak-bottom': {
        'order': 768,
        'styles': ['hw-secondary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-primary-weak-bottom': {
        'order': 769,
        'styles': ['hw-primary-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-trunk-weak-bottom': {
        'order': 770,
        'styles': ['hw-trunk-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-motorway-weak-bottom': {
        'order': 771,
        'styles': ['hw-motorway-bridge-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-tertiary-weak': {
        'order': 772,
        'styles': ['hw-const-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-secondary-weak': {
        'order': 773,
        'styles': ['hw-const-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-primary-weak': {
        'order': 774,
        'styles': ['hw-const-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-highway-weak': {
        'order': 775,
        'styles': ['hw-const-link-highway-weak'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-service-weak': {
        'order': 776,
        'styles': ['hw-const-service-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-pedestrian-weak': {
        'order': 777,
        'styles': ['hw-const-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'pedestrian\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-residential-weak': {
        'order': 778,
        'styles': ['hw-const-residential-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'residential\', \'living_street\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-tertiary-weak': {
        'order': 779,
        'styles': ['hw-const-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-secondary-weak': {
        'order': 780,
        'styles': ['hw-const-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-primary-weak': {
        'order': 781,
        'styles': ['hw-const-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-trunk-weak': {
        'order': 782,
        'styles': ['hw-const-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'trunk\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-motorway-weak': {
        'order': 783,
        'styles': ['hw-const-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'motorway\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-tertiary-weak': {
        'order': 784,
        'styles': ['hw-link-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-secondary-weak': {
        'order': 785,
        'styles': ['hw-link-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-primary-weak': {
        'order': 786,
        'styles': ['hw-link-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-highway-weak': {
        'order': 787,
        'styles': ['hw-link-highway-weak'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-service-weak': {
        'order': 788,
        'styles': ['hw-service-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-pedestrian-weak': {
        'order': 789,
        'styles': ['hw-pedestrian-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-residential-weak': {
        'order': 790,
        'styles': ['hw-residential-weak'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-tertiary-weak': {
        'order': 791,
        'styles': ['hw-tertiary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-secondary-weak': {
        'order': 792,
        'styles': ['hw-secondary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-primary-weak': {
        'order': 793,
        'styles': ['hw-primary-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-trunk-weak': {
        'order': 794,
        'styles': ['hw-trunk-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-motorway-weak': {
        'order': 795,
        'styles': ['hw-motorway-weak'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-pavement-bottom': {
        'order': 796,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'5\')'
    },
    'hw-bridge-5-path-bottom': {
        'order': 797,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-track-bottom': {
        'order': 798,
        'styles': ['hw-small-bridge-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-tertiary-bottom': {
        'order': 799,
        'styles': ['hw-construction-tertiary-link-bridge', 'hw-construction-tertiary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-secondary-bottom': {
        'order': 800,
        'styles': ['hw-construction-secondary-link-bridge', 'hw-construction-secondary-link-bottom-basic',
                   'hw-construction-secondary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-primary-bottom': {
        'order': 801,
        'styles': ['hw-construction-primary-link-bridge', 'hw-construction-primary-link-bottom-basic',
                   'hw-construction-primary-link-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-highway-bottom': {
        'order': 802,
        'styles': ['hw-construction-highway-link-bridge', 'hw-construction-highway-link-bottom-basic',
                   'hw-construction-highway-link-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-service-bottom': {
        'order': 803,
        'styles': ['hw-construction-service-bridge', 'hw-construction-service-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-residential-bottom': {
        'order': 804,
        'styles': ['hw-construction-residential-bridge', 'hw-construction-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-tertiary-bottom': {
        'order': 805,
        'styles': ['hw-construction-tertiary-bridge', 'hw-construction-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-secondary-bottom': {
        'order': 806,
        'styles': ['hw-construction-secondary-bridge', 'hw-construction-secondary-bottom-basic',
                   'hw-construction-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-primary-bottom': {
        'order': 807,
        'styles': ['hw-construction-primary-bridge', 'hw-construction-primary-bottom-basic',
                   'hw-construction-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-highway-bottom': {
        'order': 808,
        'styles': ['hw-construction-highway-bridge', 'hw-construction-highway-bottom-basic',
                   'hw-construction-highway-bottom'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-tertiary-bottom': {
        'order': 809,
        'styles': ['hw-link-tertiary-bridge', 'hw-link-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-secondary-bottom': {
        'order': 810,
        'styles': ['hw-link-secondary-bridge', 'hw-link-secondary-bottom-basic', 'hw-link-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-primary-bottom': {
        'order': 811,
        'styles': ['hw-link-primary-bridge', 'hw-link-primary-bottom-basic', 'hw-link-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-highway-bottom': {
        'order': 812,
        'styles': ['hw-link-highway-bridge', 'hw-link-highway-bottom-basic', 'hw-link-highway-bottom'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-service-bottom': {
        'order': 813,
        'styles': ['hw-service-bridge', 'hw-service-bottom'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-residential-bottom': {
        'order': 814,
        'styles': ['hw-residential-bridge', 'hw-residential-bottom'],
        'query': '(select way from planet_osm_line where "highway" in (\'pedestrian\', \'residential\', '
                 '\'living_street\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-tertiary-bottom': {
        'order': 815,
        'styles': ['hw-tertiary-bridge', 'hw-tertiary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-secondary-bottom': {
        'order': 816,
        'styles': ['hw-secondary-bridge', 'hw-secondary-bottom-basic', 'hw-secondary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-primary-bottom': {
        'order': 817,
        'styles': ['hw-primary-bridge', 'hw-primary-bottom-basic', 'hw-primary-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-trunk-bottom': {
        'order': 818,
        'styles': ['hw-trunk-bridge', 'hw-trunk-bottom-basic', 'hw-trunk-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-motorway-bottom': {
        'order': 819,
        'styles': ['hw-motorway-bridge', 'hw-motorway-bottom-basic', 'hw-motorway-bottom'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-pavement-middle': {
        'order': 820,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'footway\', \'steps\') and "bridge" is '
                 'not null and "layer"=\'5\')'
    },
    'hw-bridge-5-path-middle': {
        'order': 821,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'bridleway\', \'cycleway\') and '
                 '"bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-track-middle': {
        'order': 822,
        'styles': ['hw-small-bridge-top'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-pavement': {
        'order': 823,
        'styles': ['hw-pavement-basic', 'hw-pavement-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'footway\', \'steps\') and '
                 '"bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-path': {
        'order': 824,
        'styles': ['hw-path-basic', 'hw-path-detail'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'path\', \'bridleway\', '
                 '\'cycleway\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-track': {
        'order': 825,
        'styles': ['hw-track'],
        'query': '(select way from planet_osm_line where "highway"=\'track\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-tertiary-middle': {
        'order': 826,
        'styles': ['hw-construction-tertiary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-secondary-middle': {
        'order': 827,
        'styles': ['hw-construction-secondary-link-middle-basic', 'hw-construction-secondary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-primary-middle': {
        'order': 828,
        'styles': ['hw-construction-primary-link-middle-basic', 'hw-construction-primary-link-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-highway-middle': {
        'order': 829,
        'styles': ['hw-construction-highway-link-middle-basic', 'hw-construction-highway-link-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-service-middle': {
        'order': 830,
        'styles': ['hw-construction-service-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-residential-middle': {
        'order': 831,
        'styles': ['hw-construction-residential-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-tertiary-middle': {
        'order': 832,
        'styles': ['hw-construction-tertiary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-secondary-middle': {
        'order': 833,
        'styles': ['hw-construction-secondary-middle-basic', 'hw-construction-secondary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-primary-middle': {
        'order': 834,
        'styles': ['hw-construction-primary-middle-basic', 'hw-construction-primary-middle'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-highway-middle': {
        'order': 835,
        'styles': ['hw-construction-highway-middle-basic', 'hw-construction-highway-middle'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-tertiary-top': {
        'order': 836,
        'styles': ['hw-construction-tertiary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-secondary-top': {
        'order': 837,
        'styles': ['hw-construction-secondary-link-top-basic', 'hw-construction-secondary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-primary-top': {
        'order': 838,
        'styles': ['hw-construction-primary-link-top-basic', 'hw-construction-primary-link-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-link-highway-top': {
        'order': 839,
        'styles': ['hw-construction-highway-link-top-basic', 'hw-construction-highway-link-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk_link\', \'motorway_link\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-service-top': {
        'order': 840,
        'styles': ['hw-construction-service-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'unclassified\', \'service\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-residential-top': {
        'order': 841,
        'styles': ['hw-construction-residential-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'pedestrian\', \'residential\', \'living_street\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-tertiary-top': {
        'order': 842,
        'styles': ['hw-construction-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-secondary-top': {
        'order': 843,
        'styles': ['hw-construction-secondary-top-basic', 'hw-construction-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-primary-top': {
        'order': 844,
        'styles': ['hw-construction-primary-top-basic', 'hw-construction-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'construction\' and '
                 '"construction"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-const-highway-top': {
        'order': 845,
        'styles': ['hw-construction-highway-top-basic', 'hw-construction-highway-top'],
        'query': '(select way, "construction" from planet_osm_line where "highway"=\'construction\' and "construction" in '
                 '(\'trunk\', \'motorway\') and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-tertiary-top': {
        'order': 846,
        'styles': ['hw-link-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-secondary-top': {
        'order': 847,
        'styles': ['hw-link-secondary-top-basic', 'hw-link-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-primary-top': {
        'order': 848,
        'styles': ['hw-link-primary-top-basic', 'hw-link-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-link-highway-top': {
        'order': 849,
        'styles': ['hw-link-highway-top-basic', 'hw-link-highway-top'],
        'query': '(select way, "highway" from planet_osm_line where "highway" in (\'trunk_link\', \'motorway_link\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-service-top': {
        'order': 850,
        'styles': ['hw-service-top'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and "bridge" '
                 'is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-service-private': {
        'order': 851,
        'styles': ['hw-service-private'],
        'query': '(select way, "service" from planet_osm_line where "highway" in (\'unclassified\', \'service\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'5\')'
    },
    'hw-bridge-5-pedestrian-top': {
        'order': 852,
        'styles': ['hw-pedestrian-top'],
        'query': '(select way from planet_osm_line where "highway"=\'pedestrian\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-residential-top': {
        'order': 853,
        'styles': ['hw-residential-top'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-residential-private': {
        'order': 854,
        'styles': ['hw-residential-private'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'living_street\') and '
                 '"bridge" is not null and "access"=\'private\' and "layer"=\'5\')'
    },
    'hw-bridge-5-tertiary-top': {
        'order': 855,
        'styles': ['hw-tertiary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-secondary-top': {
        'order': 856,
        'styles': ['hw-secondary-top-basic', 'hw-secondary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-primary-top': {
        'order': 857,
        'styles': ['hw-primary-top-basic', 'hw-primary-top'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-trunk-top': {
        'order': 858,
        'styles': ['hw-trunk-top-basic', 'hw-trunk-top'],
        'query': '(select way from planet_osm_line where "highway"=\'trunk\' and "bridge" is not null and "layer"=\'5\')'
    },
    'hw-bridge-5-motorway-top': {
        'order': 859,
        'styles': ['hw-motorway-top-basic', 'hw-motorway-top'],
        'query': '(select way from planet_osm_line where "highway"=\'motorway\' and "bridge" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-disused': {
        'order': 860,
        'styles': ['railway-disused-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'disused\', \'abandoned\') and "bridge" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-construction': {
        'order': 861,
        'styles': ['railway-construction-weak', 'railway-construction-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'construction\' and "bridge" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-subway-service': {
        'order': 862,
        'styles': ['railway-subway-service'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-tram-service': {
        'order': 863,
        'styles': ['railway-tram-service'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-special-service': {
        'order': 864,
        'styles': ['railway-special-service'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-rail-service': {
        'order': 865,
        'styles': ['railway-rail-service'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and "service" '
                 'is not null and "layer"=\'5\')'
    },
    'rw-bridge-5-subway': {
        'order': 866,
        'styles': ['railway-subway-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'subway\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-tram': {
        'order': 867,
        'styles': ['railway-tram-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-special': {
        'order': 868,
        'styles': ['railway-special-weak', 'railway-special-basic'],
        'query': '(select way from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "service" is null and "layer"=\'5\')'
    },
    'rw-bridge-5-rail': {
        'order': 869,
        'styles': ['railway-rail-weak', 'railway-rail-basic'],
        'query': '(select way from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and '
                 '"service" is null and "layer"=\'5\')'
    },
    'route-cycling-generic': {
        'order': 870,
        'styles': ['route-cycling-basic', 'route-cycling-invert'],
        'query': '(select way from planet_osm_line where "route"=\'bicycle\')'
    },
    'route-cycling-other': {
        'order': 871,
        'styles': ['route-cycling-basic', 'route-cycling-invert'],
        'query': '(select way from planet_osm_line where "route"=\'bicycle\' and "colour" is null)'
    },
    'route-cycling-yellow': {
        'order': 872,
        'styles': ['route-cycling-yellow-basic', 'route-cycling-yellow-invert'],
        'query': '(select way from planet_osm_line where "route"=\'bicycle\' and "colour"=\'yellow\')'
    },
    'route-cycling-green': {
        'order': 873,
        'styles': ['route-cycling-green-basic', 'route-cycling-green-invert'],
        'query': '(select way from planet_osm_line where "route"=\'bicycle\' and "colour"=\'green\')'
    },
    'route-cycling-blue': {
        'order': 874,
        'styles': ['route-cycling-blue-basic', 'route-cycling-blue-invert'],
        'query': '(select way from planet_osm_line where "route"=\'bicycle\' and "colour"=\'blue\')'
    },
    'route-cycling-red': {
        'order': 875,
        'styles': ['route-cycling-red-basic', 'route-cycling-red-invert'],
        'query': '(select way from planet_osm_line where "route"=\'bicycle\' and "colour"=\'red\')'
    },
    'route-cycling-black': {
        'order': 876,
        'styles': ['route-cycling-black-basic', 'route-cycling-black-invert'],
        'query': '(select way from planet_osm_line where "route"=\'bicycle\' and "colour"=\'black\')'
    },
    'route-hiking-other': {
        'order': 877,
        'styles': ['route-hiking-other-basic', 'route-hiking-other-invert'],
        'query': '(select way from planet_osm_line where "route" in (\'hiking\', \'foot\') and (("colour" is null or '
                 '"colour" not in (\'yellow\', \'red\', \'green\', \'blue\')) and ("osmc:symbol" is null or '
                 '((position(\'yellow\' in "osmc:symbol") <= 0) and (position(\'green\' in "osmc:symbol") <= 0) and'
                 '(position(\'red\' in "osmc:symbol") <= 0) and (position(\'blue\' in "osmc:symbol") <= 0)))))'
    },
    'route-hiking-yellow': {
        'order': 878,
        'styles': ['route-hiking-yellow-basic', 'route-hiking-yellow-invert'],
        'query': '(select way from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'yellow\' or '
                 ' position(\'yellow\' in "osmc:symbol") > 0))'
    },
    'route-hiking-green': {
        'order': 879,
        'styles': ['route-hiking-green-basic', 'route-hiking-green-invert'],
        'query': '(select way from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'green\' or '
                 ' position(\'green\' in "osmc:symbol") > 0))'
    },
    'route-hiking-blue': {
        'order': 880,
        'styles': ['route-hiking-blue-basic', 'route-hiking-blue-invert'],
        'query': '(select way from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'blue\' or '
                 ' position(\'blue\' in "osmc:symbol") > 0))'
    },
    'route-hiking-red': {
        'order': 881,
        'styles': ['route-hiking-red-basic', 'route-hiking-red-invert'],
        'query': '(select way from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'red\' or '
                 ' position(\'red\' in "osmc:symbol") > 0))'
    },
    'route-ski_alp': {
        'order': 882,
        'styles': ['route-ski_alp-basic'],
        'query': '(select way from planet_osm_line where "piste:type" in (\'skitour\', \'nordic\'))'
    },
    'route-xcountry': {
        'order': 883,
        'styles': ['route-xcountry-basic'],
        'query': '(select way from planet_osm_line where "route"=\'ski\')'
    },
    'route-piste-novice': {
        'order': 884,
        'styles': ['route-piste-novice-basic'],
        'query': '(select way from planet_osm_line where "piste:type"=\'downhill\' and "piste:difficulty"=\'novice\')'
    },
    'route-piste-easy': {
        'order': 885,
        'styles': ['route-piste-easy-basic'],
        'query': '(select way from planet_osm_line where "piste:type"=\'downhill\' and "piste:difficulty"=\'easy\')'
    },
    'route-piste-intermediate': {
        'order': 886,
        'styles': ['route-piste-intermediate-basic'],
        'query': '(select way from planet_osm_line where "piste:type"=\'downhill\' and '
                 '"piste:difficulty"=\'intermediate\')'
    },
    'route-piste-advanced': {
        'order': 887,
        'styles': ['route-piste-advanced-basic'],
        'query': '(select way from planet_osm_line where "piste:type"=\'downhill\' and "piste:difficulty"=\'advanced\')'
    },
    'ski-snow_park': {
        'order': 1888,
        'styles': ['ski-snow_park-basic'],
        'query': '(select way from planet_osm_polygon where "piste:type"=\'snow_park\')'
    },
    'man_made-way-conveyor': {
        'order': 1889,
        'styles': ['man_made_way-conveyor'],
        'query': '(select way from planet_osm_line where "man_made"=\'goods_conveyor\')'
    },
    'aerial-way': {
        'order': 1890,
        'styles': ['aerial_way-basic'],
        'query': '(select way, "aerialway" from planet_osm_line where "aerialway" is not null)'
    },
    'tourism-area-theme': {
        'order': 1891,
        'styles': ['tourism-area-item-theme-bottom'],
        'query': '(select way from planet_osm_polygon where "tourism" in (\'theme_park\', \'zoo\') and ST_Area(way, true) > {})',
        'min_area': 0
    },
    'boundary-admin-district': {
        'order': 1892,
        'styles': ['boundary-admin-district-basic'],
        'query': '(select way from planet_osm_polygon where "boundary"=\'administrative\' and (("admin_level"=\'8\''
                 'and "ref" like \'SK%\') or ("admin_level"=\'7\' and "ref" like \'CZ%\')))'
    },
    'boundary-admin-region': {
        'order': 1893,
        'styles': ['boundary-admin-region-basic'],
        'query': '(select way from planet_osm_polygon where "boundary"=\'administrative\' and (("admin_level"=\'4\''
                 'and "ref" like \'SK%\') or ("admin_level"=\'6\' and "ref" not like \'SK%\')))'
    },
    'boundary-admin-country': {
        'order': 1894,
        'styles': ['boundary-admin-country-basic'],
        'query': '(select way from planet_osm_polygon where "boundary"=\'administrative\' and "admin_level"=\'2\')'
    },
    'boundary-protected': {
        'order': 1895,
        'styles': ['boundary-protected-basic'],
        'query': '(select way, "boundary" from planet_osm_polygon where "boundary" in (\'national_park\', '
                 '\'protected_area\') and ST_Area(way, true) > {})',
        'min_area': 1
    },
    'military-area': {
        'order': 1896,
        'styles': ['military_area-basic'],
        'query': '(select way from planet_osm_polygon where "landuse"=\'military\')'
    },
    'boundary-admin-district-name': {
        'order': 2897,
        'styles': ['boundary-admin-district-auto-name', 'boundary-admin-district-big-name',
                   'boundary-admin-district-small-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where '
                 '"boundary"=\'administrative\' and (("admin_level"=\'8\'and "ref" like \'SK%\') or '
                 '("admin_level"=\'7\' and "ref" like \'CZ%\')) and "name" is not null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'boundary-admin-region-name': {
        'order': 2898,
        'styles': ['boundary-admin-region-auto-name', 'boundary-admin-region-big-name',
                   'boundary-admin-region-small-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where '
                 '"boundary"=\'administrative\' and (("admin_level"=\'4\'and "ref" like \'SK%\') or '
                 '("admin_level"=\'6\' and "ref" not like \'SK%\')) and "name" is not null and '
                 'ST_Area(way, true) > {})',
        'min_area': 2
    },
    'boundary-admin-country-name': {
        'order': 2899,
        'styles': ['boundary-admin-country-auto-name', 'boundary-admin-country-small-name',
                   'boundary-admin-country-big-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where '
                 '"boundary"=\'administrative\' and "admin_level"=\'2\' and "name" is not null and '
                 'ST_Area(way, true) > {})',
        'min_area': 2
    },
    'place-admin-capital': {
        'order': 2900,
        'styles': ['place-admin-capital-icon', 'place-admin-capital-name'],
        'query': '(select way, "name" from planet_osm_point where "place"=\'city\' and "capital"=\'yes\' and "name" is '
                 'not null)'
    },
    'place-admin-city': {
        'order': 2901,
        'styles': ['place-admin-city-icon', 'place-admin-city-name'],
        'query': '(select way, "name" from planet_osm_point where "place"=\'city\' and ("capital"!=\'yes\' or '
                 '"capital" is null) and "name" is not null order by population::int desc)'
    },
    'place-admin-town': {
        'order': 2902,
        'styles': ['place-admin-town-icon', 'place-admin-town-name'],
        'query': '(select way, "name" from planet_osm_point where "place"=\'town\' and ("capital"!=\'yes\' or '
                 '"capital" is null) and "name" is not null order by population::int desc)'
    },
    'place-admin-village': {
        'order': 2903,
        'styles': ['place-admin-village-icon', 'place-admin-village-name'],
        'query': '(select way, "name" from planet_osm_point where "place"=\'village\' and "name" is not null)'
    },
    'place-admin-dwelling': {
        'order': 2904,
        'styles': ['place-admin-dwelling-name'],
        'query': '(select way, "name" from planet_osm_point where "place" in  (\'isolated_dwelling\', \'farm\', '
                 '\'allotments\', \'hamlet\') and "name" is not null)'
    },
    'place-admin-suburb': {
        'order': 2905,
        'styles': ['place-admin-suburb-name'],
        'query': '(select way, "name" from planet_osm_point where "place" in  (\'borough\', \'suburb\', '
                 '\'quarter\') and "name" is not null)'
    },
    'place-admin-neighborhood': {
        'order': 2906,
        'styles': ['place-admin-neighborhood-name'],
        'query': '(select way, "name" from planet_osm_point where "place" in  (\'neighbourhood\', \'city_block\', '
                 '\'plot\') and "name" is not null)'
    },
    'aero-area-a': {
        'order': 2907,
        'styles': ['aero_item-a-basic', 'aero_item-a-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "aeroway"=\'aerodrome\')'
    },
    'land_use-ski-detail': {
        'order': 2908,
        'styles': ['land_use-ski-icon', 'land_use-ski-name'],
        'query': '(select way, "name" from planet_osm_polygon where "landuse"=\'winter_sports\')'
    },
    'rw-item-station': {
        'order': 2909,
        'styles': ['railway-station-basic', 'railway-station-detail'],
        'query': '(select way, "name" from planet_osm_point where "railway" in (\'station\', \'halt\'))'
    },
    'leisure-area-marina-detail': {
        'order': 2910,
        'styles': ['leisure-area-marina-name'],
        'query': '(select way, "name" from planet_osm_polygon where "leisure"=\'marina\' and ST_Area(way, true) > {})',
        'min_area': 1
    },
    'amenity-item-ferry': {
        'order': 2911,
        'styles': ['amenity-item-ferry-icon', 'amenity-item-ferry-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'ferry_terminal\')'
    },
    'boundary-protected-name': {
        'order': 2912,
        'styles': ['boundary-protected-auto-name', 'boundary-protected-big-name', 'boundary-protected-small-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where "boundary" in '
                 '(\'national_park\', \'protected_area\') and "name" is not null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'water-area-lake-name': {
        'order': 2913,
        'styles': ['water_area-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where "water" in (\'lake\', '
                 '\'oxbow\', \'lagoon\') and "name" is not null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'water-area-reservoir-name': {
        'order': 2914,
        'styles': ['water_area-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where "water" in '
                 '(\'reservoir\', \'pond\', \'basin\', \'reflecting_pool\', \'moat\') and "name" is not null and '
                 'ST_Area(way, true) > {})',
        'min_area': 2
    },
    'water-area-river-name': {
        'order': 2915,
        'styles': ['water_area-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where "water"=\'river\' '
                 'and "name" is not null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'waterway-river-name': {
        'order': 2916,
        'styles': ['waterway-river-name'],
        'query': '(select way, "name" from planet_osm_line where "waterway"=\'river\' and "name" is not null)'
    },
    'waterway-canal-name': {
        'order': 2917,
        'styles': ['waterway-canal-name'],
        'query': '(select way, "waterway", "name" from planet_osm_line where "waterway" in (\'canal\', \'ditch\', '
                 '\'drain\') and "name" is not null)'
    },
    'waterway-stream-name': {
        'order': 2918,
        'styles': ['waterway-stream-name'],
        'query': '(select way, "name" from planet_osm_line where "waterway"=\'stream\' and "name" is not null)'
    },
    'hw-junction-name': {
        'order': 2919,
        'styles': ['highway-junction-name'],
        'query': '(select way, "name", "ref" from planet_osm_point where "highway"=\'motorway_junction\' and "name" '
                 'is not null)'
    },
    'rw-bridge-rail-detail': {
        'order': 2920,
        'styles': ['rw-bridge-icon', 'rw-bridge-name'],
        'query': '(select way, "name" from planet_osm_line where "railway"=\'rail\' and "bridge" is not null and '
                 '"name" is not null and "service" is null)'
    },
    'rw-bridge-special-detail': {
        'order': 2921,
        'styles': ['rw-bridge-icon', 'rw-bridge-name'],
        'query': '(select way, "name" from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "bridge" is not null and "name" is not null and '
                 '"service" is null)'
    },
    'rw-bridge-tram-detail': {
        'order': 2922,
        'styles': ['rw-bridge-icon', 'rw-bridge-name'],
        'query': '(select way, "name" from planet_osm_line where "railway"=\'tram\' and "bridge" is not null and '
                 '"name" is not null and "service" is null)'
    },
    'rw-tunnel-rail-detail': {
        'order': 2923,
        'styles': ['rw-tunnel-icon', 'rw-tunnel-name'],
        'query': '(select way, "name" from planet_osm_line where "railway"=\'rail\' and "tunnel" is not null and '
                 '"name" is not null and "service" is null)'
    },
    'rw-tunnel-special-detail': {
        'order': 2924,
        'styles': ['rw-tunnel-icon', 'rw-tunnel-name'],
        'query': '(select way, "name" from planet_osm_line where "railway" in (\'funicular\', \'light_rail\', '
                 '\'narrow_gauge\', \'preserved\') and "tunnel" is not null and "name" is not null and "service" '
                 'is null)'
    },
    'rw-tunnel-tram-detail': {
        'order': 2925,
        'styles': ['rw-tunnel-icon', 'rw-tunnel-name'],
        'query': '(select way, "name" from planet_osm_line where "railway"=\'tram\' and "tunnel" is not null and '
                 '"name" is not null and "service" is null)'
    },
    'hw-bridge-highway-detail': {
        'order': 2926,
        'styles': ['hw-bridge-icon', 'hw-bridge-name'],
        'query': '(select way, "name" from planet_osm_line where "highway" in (\'motorway\', \'trunk\') and "bridge" is '
                 'not null and "name" is not null)'
    },
    'hw-bridge-primary-detail': {
        'order': 2927,
        'styles': ['hw-bridge-icon', 'hw-bridge-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'primary\' and "bridge" is '
                 'not null and "name" is not null)'
    },
    'hw-bridge-secondary-detail': {
        'order': 2928,
        'styles': ['hw-bridge-icon', 'hw-bridge-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'secondary\' and "bridge" is '
                 'not null and "name" is not null)'
    },
    'hw-bridge-tertiary-detail': {
        'order': 2929,
        'styles': ['hw-bridge-icon', 'hw-bridge-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'tertiary\' and "bridge" is '
                 'not null and "name" is not null)'
    },
    'hw-tunnel-highway-detail': {
        'order': 2930,
        'styles': ['hw-tunnel-icon', 'hw-tunnel-name'],
        'query': '(select way, "name" from planet_osm_line where "highway" in (\'motorway\', \'trunk\') and "tunnel" '
                 'is not null and "name" is not null)'
    },
    'hw-tunnel-primary-detail': {
        'order': 2931,
        'styles': ['hw-tunnel-icon', 'hw-tunnel-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'primary\' and "tunnel" is not null and '
                 '"name" is not null)'
    },
    'hw-tunnel-secondary-detail': {
        'order': 2932,
        'styles': ['hw-tunnel-icon', 'hw-tunnel-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'secondary\' and "tunnel" is not null and '
                 '"name" is not null)'
    },
    'hw-tunnel-tertiary-detail': {
        'order': 2933,
        'styles': ['hw-tunnel-icon', 'hw-tunnel-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'tertiary\' and "tunnel" is not null and '
                 '"name" is not null)'
    },
    'hw-highway-name': {
        'order': 2934,
        'styles': ['hw-name'],
        'query': '(select way, "name" from planet_osm_line where "highway" in (\'motorway\', \'trunk\') and "name" '
                 'is not null)'
    },
    'hw-primary-name': {
        'order': 2935,
        'styles': ['hw-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'primary\' and "name" '
                 'is not null)'
    },
    'hw-secondary-name': {
        'order': 2936,
        'styles': ['hw-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'secondary\' and "name" '
                 'is not null)'
    },
    'hw-tertiary-name': {
        'order': 2937,
        'styles': ['hw-name'],
        'query': '(select way, "name" from planet_osm_line where "highway"=\'secondary\' and "name" '
                 'is not null)'
    },
    'hw-residential-name': {
        'order': 2938,
        'styles': ['hw-name'],
        'query': '(select way, "name" from planet_osm_line where "highway" in (\'residential\', \'living_street\', '
                 '\'pedestrian\') and "name" is not null)'
    },
    'hw-service-name': {
        'order': 2939,
        'styles': ['hw-name'],
        'query': '(select way, "name" from planet_osm_line where "highway" in (\'service\', \'unclassified\') and "name" '
                 'is not null)'
    },
    'tourism-area-theme-name': {
        'order': 2940,
        'styles': ['tourism-area-item-theme-top'],
        'query': '(select way, "name" from planet_osm_polygon where "tourism" in (\'theme_park\', \'attraction\', \'zoo\') and '
                 '"name" is not null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'land_use-built-name': {
        'order': 2941,
        'styles': ['land_use-built-name'],
        'query': '(select way, "landuse", "name", ST_Area(way, true) as size from planet_osm_polygon where "landuse" '
                 'in (\'commercial\', \'industrial\', \'retail\') and "name" is not null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'land_use-farm-name': {
        'order': 2942,
        'styles': ['land_use-farm-name'],
        'query': '(select way, "name", ST_Area(way, true) as size from planet_osm_polygon where "landuse"=\'farmyard\' '
                 'and "name" is not null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'land_use-quarry-name': {
        'order': 2943,
        'styles': ['land_use-quarry-name'],
        'query': '(select way, "name" from planet_osm_polygon where "landuse"=\'quarry\' and "name" is not '
                 'null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'land_use-cemetery-name': {
        'order': 2944,
        'styles': ['land_use-cemetery-name'],
        'query': '(select way, "name" from planet_osm_polygon where "landuse"=\'cemetery\' and "name" is not '
                 'null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'amenity-area-name': {
        'order': 2945,
        'styles': ['amenity-area-name-education'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'university\' and "name" is not '
                 'null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'military-area-name': {
        'order': 2946,
        'styles': ['military_area-name'],
        'query': '(select way, "name" from planet_osm_polygon where "landuse"=\'military\' and "name" is not '
                 'null and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'route-cycling-name': {
        'order': 2947,
        'styles': ['route-cycling-name'],
        'query': '(select way, "name" from planet_osm_line where "route"=\'bicycle\' and "name" is not null)'
    },
    'route-hiking-other-name': {
        'order': 2948,
        'styles': ['route-hiking-other-name'],
        'query': '(select way, "name" from planet_osm_line where "route" in (\'hiking\', \'foot\') and (("colour" is '
                 'null or "colour" not in (\'yellow\', \'red\', \'green\', \'blue\')) and ("osmc:symbol" is null or '
                 '((position(\'yellow\' in "osmc:symbol") <= 0) and (position(\'green\' in "osmc:symbol") <= 0) and'
                 '(position(\'red\' in "osmc:symbol") <= 0) and (position(\'blue\' in "osmc:symbol") <= 0)))) and '
                 '"name" is not null)'
    },
    'route-hiking-red-name': {
        'order': 2949,
        'styles': ['route-hiking-red-name'],
        'query': '(select way, "name" from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'red\' or '
                 ' position(\'red\' in "osmc:symbol") > 0) and "name" is not null)'
    },
    'route-hiking-blue-name': {
        'order': 2950,
        'styles': ['route-hiking-blue-name'],
        'query': '(select way, "name" from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'blue\' or '
                 ' position(\'blue\' in "osmc:symbol") > 0) and "name" is not null)'
    },
    'route-hiking-green-name': {
        'order': 2951,
        'styles': ['route-hiking-green-name'],
        'query': '(select way, "name" from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'green\' or '
                 ' position(\'green\' in "osmc:symbol") > 0) and "name" is not null)'
    },
    'route-hiking-yellow-name': {
        'order': 2952,
        'styles': ['route-hiking-yellow-name'],
        'query': '(select way, "name" from planet_osm_line where "route" in (\'hiking\', \'foot\') and ("colour"=\'yellow\' or '
                 ' position(\'yellow\' in "osmc:symbol") > 0) and "name" is not null)'
    },
    'route-piste-advanced-name': {
        'order': 2953,
        'styles': ['route-piste-advanced-name'],
        'query': '(select way, "name" from planet_osm_line where "piste:type"=\'downhill\' and '
                 '"piste:difficulty"=\'advanced\' and "name" is not null)'
    },
    'route-piste-intermediate-name': {
        'order': 2954,
        'styles': ['route-piste-intermediate-name'],
        'query': '(select way, "name" from planet_osm_line where "piste:type"=\'downhill\' and '
                 '"piste:difficulty"=\'intermediate\' and "name" is not null)'
    },
    'route-piste-easy-name': {
        'order': 2955,
        'styles': ['route-piste-easy-name'],
        'query': '(select way, "name" from planet_osm_line where "piste:type"=\'downhill\' and '
                 '"piste:difficulty"=\'easy\' and "name" is not null)'
    },
    'route-piste-novice-name': {
        'order': 2956,
        'styles': ['route-piste-novice-name'],
        'query': '(select way, "name" from planet_osm_line where "piste:type"=\'downhill\' and '
                 '"piste:difficulty"=\'novice\' and "name" is not null)'
    },
    'route-xcountry-name': {
        'order': 2957,
        'styles': ['route-xcountry-name'],
        'query': '(select way, "name" from planet_osm_line where "route"=\'ski\' and "name" is not null)'
    },
    'route-ski_alp-name': {
        'order': 2958,
        'styles': ['route-ski_alp-name'],
        'query': '(select way, "name" from planet_osm_line where "piste:type" in (\'skitour\', \'nordic\') and "name" is not null)'
    },
    'ski-snow_park-name': {
        'order': 2959,
        'styles': ['ski-snow_park-name'],
        'query': '(select way, "name" from planet_osm_polygon where "piste:type"=\'snow_park\' and "name" is not null '
                 'and ST_Area(way, true) > {})',
        'min_area': 1
    },
    'aerial-way-name': {
        'order': 2960,
        'styles': ['aerial_way-name'],
        'query': '(select way, "name" from planet_osm_line where "aerialway" is not null and "name" is not null)'
    },
    'natural-item-peak': {
        'order': 2961,
        'styles': ['natural_item-peak-basic', 'natural_item-peak-medium', 'natural_item-peak-detail'],
        'query': '(select way, "name", round(ele::numeric) as ele from planet_osm_point where "natural"=\'peak\' and '
                 '"name" is not null and "ele" is not null order by "ele"::real desc)'
    },
    'natural-item-volcano': {
        'order': 2962,
        'styles': ['natural_item-volcano-basic', 'natural_item-volcano-medium', 'natural_item-volcano-detail'],
        'query': '(select way, "name", round(ele::numeric) as ele from planet_osm_point where "natural"=\'volcano\' '
                 'and "name" is not null and "ele" is not null order by "ele"::real desc)'
    },
    'natural-item-saddle': {
        'order': 2963,
        'styles': ['natural_item-saddle-basic', 'natural_item-saddle-medium', 'natural_item-saddle-detail'],
        'query': '(select way, "name", round(ele::numeric) as ele from planet_osm_point where "natural"=\'saddle\' '
                 'and "name" is not null and "ele" is not null order by "ele"::real desc)'
    },
    'natural-item-cave': {
        'order': 2964,
        'styles': ['natural_item-cave-basic', 'natural_item-cave-medium', 'natural_item-cave-detail'],
        'query': '(select way, "name", round(ele::numeric) as ele  from planet_osm_point where '
                 '"natural"=\'cave_entrance\' and "name" is not null)'
    },
    'hydro-item-waterfall': {
        'order': 2965,
        'styles': ['waterway-item-waterfall-basic', 'waterway-item-waterfall-detail'],
        'query': '(select way, "name" from planet_osm_point where "waterway"=\'waterfall\' and "name" is not null)'
    },
    'hydro-item-spring': {
        'order': 2966,
        'styles': ['natural_item-hydro-spring'],
        'query': '(select way from planet_osm_point where "natural" in (\'spring\', \'geyser\'))'
    },
    'amenity-area-health-a': {
        'order': 2967,
        'styles': ['amenity-area-item-health-a-basic', 'amenity-area-item-health-a-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'hospital\')'
    },
    'amenity-item-health-a': {
        'order': 2968,
        'styles': ['amenity-item-health-a-basic', 'amenity-item-health-a-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'hospital\')'
    },
    'amenity-area-school-a': {
        'order': 2969,
        'styles': ['amenity-area-item-school-a-basic', 'amenity-area-item-school-a-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity" in (\'university\', \'college\'))'
    },
    'amenity-item-school-a': {
        'order': 2970,
        'styles': ['amenity-item-school-a-basic', 'amenity-item-school-a-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity" in (\'university\', \'college\'))'
    },
    'leisure-area-golf-detail': {
        'order': 2971,
        'styles': ['leisure-area-golf-icon', 'leisure-area-golf-name'],
        'query': '(select way, "name" from planet_osm_polygon where "leisure"=\'golf_course\')'
    },
    'leisure-item-golf': {
        'order': 2972,
        'styles': ['leisure-item-golf-icon', 'leisure-item-golf-name'],
        'query': '(select way, "name" from planet_osm_point where "leisure"=\'golf_course\')'
    },
    'shop-area-a': {
        'order': 2973,
        'styles': ['shop-area-item-a-basic', 'shop-area-item-a-name'],
        'query': '(select way, "name" from planet_osm_polygon where "shop" in (\'supermarket\', \'mall\', '
                 '\'department_store\'))'
    },
    'shop-item-a': {
        'order': 2974,
        'styles': ['shop-item-a-basic', 'shop-item-a-name'],
        'query': '(select way, "name" from planet_osm_point where "shop" in (\'supermarket\', \'mall\', '
                 '\'department_store\'))'
    },
    'amenity-area-forces': {
        'order': 2975,
        'styles': ['amenity-area-item-forces-basic', 'amenity-area-item-forces-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'police\', \'fire_station\'))'
    },
    'amenity-item-forces': {
        'order': 2976,
        'styles': ['amenity-item-forces-basic', 'amenity-item-forces-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'police\', \'fire_station\'))'
    },
    'amenity-area-office': {
        'order': 2977,
        'styles': ['amenity-area-item-office-basic', 'amenity-area-item-office-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'townhall\', \'post_office\'))'
    },
    'amenity-item-office': {
        'order': 2978,
        'styles': ['amenity-item-office-basic', 'amenity-item-office-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'townhall\', \'post_office\'))'
    },
    'amenity-area-law': {
        'order': 2979,
        'styles': ['amenity-area-item-law-basic', 'amenity-area-item-law-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'courthouse\', \'prison\'))'
    },
    'amenity-item-law': {
        'order': 2980,
        'styles': ['amenity-item-law-basic', 'amenity-item-law-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'courthouse\', \'prison\'))'
    },
    'leisure-area-stadium-detail': {
        'order': 2981,
        'styles': ['leisure-area-stadium-icon', 'leisure-area-stadium-name'],
        'query': '(select way, "name", "sport" from planet_osm_polygon where "leisure"=\'stadium\')'
    },
    'leisure-item-stadium': {
        'order': 2982,
        'styles': ['leisure-item-stadium-icon', 'leisure-item-stadium-name'],
        'query': '(select way, "name", "sport" from planet_osm_point where "leisure"=\'stadium\')'
    },
    'historic-area': {
        'order': 2983,
        'styles': ['historic-area-item-basic', 'historic-area-item-name'],
        'query': '(select way, "name", "historic", "memorial", "castle_type" from planet_osm_polygon where "historic" is '
                 'not null)'
    },
    'historic-item': {
        'order': 2984,
        'styles': ['historic-item-basic', 'historic-item-name'],
        'query': '(select way, "name", "historic", "memorial", "castle_type" from planet_osm_point where "historic" is '
                 'not null)'
    },
    'tourism-area-hotel': {
        'order': 2985,
        'styles': ['tourism-area-item-hotel-basic', 'tourism-area-item-hotel-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "tourism"=\'hotel\')'
    },
    'tourism-item-hotel': {
        'order': 2986,
        'styles': ['tourism-item-hotel-basic', 'tourism-item-hotel-detail'],
        'query': '(select way, "name" from planet_osm_point where "tourism"=\'hotel\')'
    },
    'amenity-area-religion': {
        'order': 2987,
        'styles': ['amenity-area-item-religion-basic', 'amenity-area-item-religion-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'place_of_worship\')'
    },
    'amenity-item-religion': {
        'order': 2988,
        'styles': ['amenity-item-religion-basic', 'amenity-item-religion-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'place_of_worship\')'
    },
    'tourism-area-museum': {
        'order': 2989,
        'styles': ['tourism-area-item-museum-basic', 'tourism-area-item-museum-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "tourism" in (\'museum\', \'gallery\'))'
    },
    'tourism-item-museum': {
        'order': 2990,
        'styles': ['tourism-item-museum-basic', 'tourism-item-museum-detail'],
        'query': '(select way, "name" from planet_osm_point where "tourism" in (\'museum\', \'gallery\'))'
    },
    'amenity-area-bus': {
        'order': 2991,
        'styles': ['amenity-area-item-bus-basic', 'amenity-area-item-bus-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'bus_station\')'
    },
    'amenity-item-bus': {
        'order': 2992,
        'styles': ['amenity-item-bus-basic', 'amenity-item-bus-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'bus_station\')'
    },
    'aero-area-b': {
        'order': 2993,
        'styles': ['aero_item-b-basic', 'aero_item-b-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "aeroway"=\'helipad\')'
    },
    'aero-item-b': {
        'order': 2994,
        'styles': ['aero_item-b-basic', 'aero_item-b-detail'],
        'query': '(select way, "name" from planet_osm_point where "aeroway"=\'helipad\')'
    },
    'amenity-area-health-b': {
        'order': 2995,
        'styles': ['amenity-area-item-health-b-basic', 'amenity-area-item-health-b-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'clinic\', \'doctors\', '
                 '\'dentist\', \'pharmacy\'))'
    },
    'amenity-item-health-b': {
        'order': 2996,
        'styles': ['amenity-item-health-b-basic', 'amenity-item-health-b-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'clinic\', \'doctors\', '
                 '\'dentist\', \'pharmacy\'))'
    },
    'amenity-area-school-b': {
        'order': 2997,
        'styles': ['amenity-area-item-school-b-basic', 'amenity-area-item-school-b-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'school\')'
    },
    'amenity-item-school-b': {
        'order': 2998,
        'styles': ['amenity-item-school-b-basic', 'amenity-item-school-b-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'school\')'
    },
    'tourism-area-hostel': {
        'order': 2999,
        'styles': ['tourism-area-item-hostel-basic', 'tourism-area-item-hostel-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "tourism" in (\'hostel\', \'motel\', '
                 '\'apartment\', \'guest_house\'))'
    },
    'tourism-item-hostel': {
        'order': 3000,
        'styles': ['tourism-item-hostel-basic', 'tourism-item-hostel-detail'],
        'query': '(select way, "name" from planet_osm_point where "tourism" in (\'hostel\', \'motel\', '
                 '\'apartment\', \'guest_house\'))'
    },
    'leisure-area-pool-detail': {
        'order': 3001,
        'styles': ['leisure-area-pool-icon', 'leisure-area-pool-name'],
        'query': '(select way, "name", "leisure" from planet_osm_polygon where "leisure" in (\'water_park\', '
                 '\'beach_resort\', \'swimming_area\', \'swimming_pool\') and ("access" is null or "access"!=\'private\'))'
    },
    'leisure-item-pool': {
        'order': 3002,
        'styles': ['leisure-item-pool-icon', 'leisure-item-pool-name'],
        'query': '(select way, "name", "leisure" from planet_osm_point where "leisure" in (\'water_park\', '
                 '\'beach_resort\', \'swimming_area\', \'swimming_pool\') and ("access" is null or "access"!=\'private\'))'
    },
    'man_made-area-tower-historic': {
        'order': 3003,
        'styles': ['man_made-area-item-tower-historic-basic', 'man_made-area-item-tower-historic-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "man_made"=\'tower\' and "historic" is not null)'
    },
    'man_made-item-tower-historic': {
        'order': 3004,
        'styles': ['man_made-item-tower-historic-basic', 'man_made-item-tower-historic-detail'],
        'query': '(select way, "name" from planet_osm_point where "man_made"=\'tower\' and "historic" is not null)'
    },
    'man_made-area-obelisk': {
        'order': 3005,
        'styles': ['man_made-area-item-obelisk-basic', 'man_made-area-item-obelisk-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "man_made"=\'obelisk\')'
    },
    'man_made-item-obelisk': {
        'order': 3006,
        'styles': ['man_made-item-obelisk-basic', 'man_made-item-obelisk-detail'],
        'query': '(select way, "name" from planet_osm_point where "man_made"=\'obelisk\')'
    },
    'man_made-area-tower': {
        'order': 3007,
        'styles': ['man_made-area-item-tower-basic', 'man_made-area-item-tower-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "man_made"=\'tower\' and historic is null)'
    },
    'man_made-item-tower': {
        'order': 3008,
        'styles': ['man_made-item-tower-basic', 'man_made-item-tower-detail'],
        'query': '(select way, "name" from planet_osm_point where "man_made"=\'tower\' and historic is null)'
    },
    'amenity-area-art': {
        'order': 3009,
        'styles': ['amenity-area-item-art-basic', 'amenity-area-item-art-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'theatre\', '
                 '\'cinema\', \'arts_centre\', \'nightclub\', \'casino\'))'
    },
    'amenity-item-art': {
        'order': 3010,
        'styles': ['amenity-item-art-basic', 'amenity-item-art-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'theatre\', '
                 '\'cinema\', \'arts_centre\', \'nightclub\', \'casino\'))'
    },
    'tourism-item-art': {
        'order': 3011,
        'styles': ['tourism-item-artwork-basic', 'tourism-item-artwork-detail'],
        'query': '(select way, "name" from planet_osm_point where "tourism"=\'artwork\')'
    },
    'tourism-area-hut': {
        'order': 3012,
        'styles': ['tourism-area-item-hut-basic', 'tourism-area-item-hut-detail'],
        'query': '(select way, "name" from planet_osm_polygon where "tourism"=\'alpine_hut\')'
    },
    'tourism-item-hut': {
        'order': 3013,
        'styles': ['tourism-item-hut-basic', 'tourism-item-hut-detail'],
        'query': '(select way, "name" from planet_osm_point where "tourism"=\'alpine_hut\')'
    },
    'tourism-area-chalet': {
        'order': 3014,
        'styles': ['tourism-area-item-chalet'],
        'query': '(select way, "name", "tourism" from planet_osm_polygon where "tourism" in (\'chalet\', '
                 '\'wilderness_hut\', \'camp_site\', \'caravan_site\'))'
    },
    'tourism-item-chalet': {
        'order': 3015,
        'styles': ['tourism-item-chalet'],
        'query': '(select way, "name", "tourism" from planet_osm_point where "tourism" in (\'chalet\', '
                 '\'wilderness_hut\', \'camp_site\', \'caravan_site\'))'
    },
    'amenity-area-fountain': {
        'order': 3016,
        'styles': ['amenity-area-item-fountain-basic', 'amenity-area-item-fountain-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'fountain\')'
    },
    'amenity-item-fountain': {
        'order': 3017,
        'styles': ['amenity-item-fountain-basic', 'amenity-item-fountain-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'fountain\')'
    },
    'amenity-area-food-a': {
        'order': 3018,
        'styles': ['amenity-area-item-food-a-basic', 'amenity-area-item-food-a-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity" in (\'restaurant\', \'food_court\'))'
    },
    'amenity-item-food-a': {
        'order': 3019,
        'styles': ['amenity-item-food-a-basic', 'amenity-item-food-a-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity" in (\'restaurant\', \'food_court\'))'
    },
    'amenity-area-library': {
        'order': 3020,
        'styles': ['amenity-area-item-library-basic', 'amenity-area-item-library-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'library\')'
    },
    'amenity-item-library': {
        'order': 3021,
        'styles': ['amenity-item-library-basic', 'amenity-item-library-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'library\')'
    },
    'amenity-area-fuel-a': {
        'order': 3022,
        'styles': ['amenity-area-item-fuel-a-basic', 'amenity-area-item-fuel-a-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'fuel\')'
    },
    'amenity-item-fuel-a': {
        'order': 3023,
        'styles': ['amenity-item-fuel-a-basic', 'amenity-item-fuel-a-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'fuel\')'
    },
    'amenity-area-bank': {
        'order': 3024,
        'styles': ['amenity-area-item-bank-basic', 'amenity-area-item-bank-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'bank\')'
    },
    'amenity-item-bank': {
        'order': 3025,
        'styles': ['amenity-item-bank-basic', 'amenity-item-bank-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'bank\')'
    },
    'amenity-area-food-b': {
        'order': 3026,
        'styles': ['amenity-area-item-food-b-basic', 'amenity-area-item-food-b-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'fast_food\', \'bar\', '
                 '\'pub\', \'biergarten\', \'cafe\'))'
    },
    'amenity-item-food-b': {
        'order': 3027,
        'styles': ['amenity-item-food-b-basic', 'amenity-item-food-b-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'fast_food\', \'bar\', '
                 '\'pub\', \'biergarten\', \'cafe\'))'
    },
    'amenity-area-market': {
        'order': 3028,
        'styles': ['amenity-area-item-market-basic', 'amenity-area-item-market-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'marketplace\')'
    },
    'amenity-item-market': {
        'order': 3029,
        'styles': ['amenity-item-market-basic', 'amenity-item-market-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'marketplace\')'
    },
    'shop-area-b': {
        'order': 3030,
        'styles': ['shop-area-item-b-basic', 'shop-area-item-b-name'],
        'query': '(select way, "name" from planet_osm_polygon where "shop" in (\'pet\', \'toys\', \'books\', '
                 '\'stationery\', \'gift\', \'video_games\', \'video\', \'photo\', \'musical_instrument\', '
                 '\'music\', \'craft\', \'games\', \'art\', \'sports\', \'outdoor\', \'electronics\', \'furniture\', '
                 '\'hardware\', \'houseware\', \'garden_centre\', \'florist\', \'appliance\', \'perfumery\', '
                 '\'optician\', \'medical_supply\', \'cosmetics\', \'beauty\', \'chemist\', \'second_hand\', '
                 '\'shoes\', \'watches\', \'clothes\', \'bag\', \'general\', \'wine\', \'pastry\', \'bakery\', '
                 '\'greengrocer\', \'farm\', \'dairy\', \'convenience\', \'butcher\', \'alcohol\'))'
    },
    'shop-item-b': {
        'order': 3031,
        'styles': ['shop-item-a-basic', 'shop-item-b-name'],
        'query': '(select way, "name" from planet_osm_point where "shop" in (\'pet\', \'toys\', \'books\', '
                 '\'stationery\', \'gift\', \'video_games\', \'video\', \'photo\', \'musical_instrument\', '
                 '\'music\', \'craft\', \'games\', \'art\', \'sports\', \'outdoor\', \'electronics\', \'furniture\', '
                 '\'hardware\', \'houseware\', \'garden_centre\', \'florist\', \'appliance\', \'perfumery\', '
                 '\'optician\', \'medical_supply\', \'cosmetics\', \'beauty\', \'chemist\', \'second_hand\', '
                 '\'shoes\', \'watches\', \'clothes\', \'bag\', \'general\', \'wine\', \'pastry\', \'bakery\', '
                 '\'greengrocer\', \'farm\', \'dairy\', \'convenience\', \'butcher\', \'alcohol\'))'
    },
    'leisure-area-park-detail': {
        'order': 3032,
        'styles': ['leisure-area-park-name'],
        'query': '(select way, "name" from planet_osm_polygon where "leisure"=\'park\' and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'leisure-item-park': {
        'order': 3033,
        'styles': ['leisure-item-park-name'],
        'query': '(select way, "name" from planet_osm_point where "leisure"=\'park\')'
    },
    'leisure-area-garden-detail': {
        'order': 3034,
        'styles': ['leisure-area-garden-name'],
        'query': '(select way, "name" from planet_osm_polygon where "leisure"=\'garden\' and ST_Area(way, true) > {})',
        'min_area': 2
    },
    'leisure-area-pitch-detail': {
        'order': 3035,
        'styles': ['leisure-area-pitch-icon', 'leisure-area-pitch-name'],
        'query': '(select way, "name", "sport" from planet_osm_polygon where (("leisure" in (\'pitch\', \'track\')) or '
                 '("leisure"=\'sports_centre\' and "sport" is not null)) order by ST_Area(way, true) desc)'
    },
    'leisure-item-pitch': {
        'order': 3036,
        'styles': ['leisure-item-pitch-icon', 'leisure-item-pitch-name'],
        'query': '(select way, "name", "sport" from planet_osm_point where (("leisure" in (\'pitch\', \'track\')) or '
                 '("leisure"=\'sports_centre\' and "sport" is not null)) order by ST_Area(way, true) desc)'
    },
    'leisure-area-horse-detail': {
        'order': 3037,
        'styles': ['leisure-area-horse-icon', 'leisure-area-horse-name'],
        'query': '(select way, "name" from planet_osm_polygon where "leisure"=\'horse_riding\')'
    },
    'leisure-item-horse': {
        'order': 3038,
        'styles': ['leisure-item-horse-icon', 'leisure-item-horse-name'],
        'query': '(select way, "name" from planet_osm_point where "leisure"=\'horse_riding\')'
    },
    'leisure-area-fitness': {
        'order': 3039,
        'styles': ['leisure-area-fitness-icon'],
        'query': '(select way from planet_osm_polygon where "leisure" in (\'fitness_centre\', \'fitness_station\'))'
    },
    'leisure-item-fitness': {
        'order': 3040,
        'styles': ['leisure-item-fitness-icon'],
        'query': '(select way from planet_osm_point where "leisure" in (\'fitness_centre\', \'fitness_station\'))'
    },
    'amenity-area-fuel-b': {
        'order': 3041,
        'styles': ['amenity-area-item-fuel-b-basic', 'amenity-area-item-fuel-b-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'car_wash\', \'charging_station\'))'
    },
    'amenity-item-fuel-b': {
        'order': 3042,
        'styles': ['amenity-item-fuel-b-basic', 'amenity-item-fuel-b-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'car_wash\', \'charging_station\'))'
    },
    'amenity-area-social': {
        'order': 3043,
        'styles': ['amenity-area-item-social-basic', 'amenity-area-item-social-name'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'social_facility\', '
                 '\'nursing_home\', \'community_centre\'))'
    },
    'amenity-item-social': {
        'order': 3044,
        'styles': ['amenity-item-social-basic', 'amenity-item-social-name'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'social_facility\', '
                 '\'nursing_home\', \'community_centre\'))'
    },
    'amenity-area-school-c': {
        'order': 3045,
        'styles': ['amenity-area-item-school-c-basic', 'amenity-area-item-school-c-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity" in (\'kindergarten\', \'childcare\'))'
    },
    'amenity-item-school-c': {
        'order': 3046,
        'styles': ['amenity-item-school-c-basic', 'amenity-item-school-c-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity" in (\'kindergarten\', \'childcare\'))'
    },
    'man_made-area-tall_building': {
        'order': 3047,
        'styles': ['man_made-area-item-tall_building-basic'],
        'query': '(select way, "name", "man_made" from planet_osm_polygon where "man_made" in (\'cross\', \'chimney\', '
                 '\'windmill\', \'communications_tower\', \'mast\', \'crane\', \'silo\', \'storage_tank\', '
                 '\'water_tower\'))'
    },
    'man_made-item-tall_building': {
        'order': 3048,
        'styles': ['man_made-item-tall_building-basic'],
        'query': '(select way, "name", "man_made" from planet_osm_point where "man_made" in (\'cross\', \'chimney\', '
                 '\'windmill\', \'communications_tower\', \'mast\', \'crane\', \'silo\', \'storage_tank\', '
                 '\'water_tower\'))'
    },
    'amenity-area-waste': {
        'order': 3049,
        'styles': ['amenity-area-item-waste-basic', 'amenity-area-item-waste-name'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'recycling\' and '
                 '"recycling_type"=\'centre\')'
    },
    'amenity-item-waste': {
        'order': 3050,
        'styles': ['amenity-item-waste-basic', 'amenity-item-waste-name'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'recycling\' and '
                 '"recycling_type"=\'centre\')'
    },
    'leisure-area-dance': {
        'order': 3051,
        'styles': ['leisure-area-dance-icon', 'leisure-area-dance-name'],
        'query': '(select way, "name" from planet_osm_polygon where "leisure"=\'dance\')'
    },
    'leisure-item-dance': {
        'order': 3052,
        'styles': ['leisure-item-dance-icon', 'leisure-item-dance-name'],
        'query': '(select way, "name" from planet_osm_point where "leisure"=\'dance\')'
    },
    'rw-item-tram_stop': {
        'order': 3053,
        'styles': ['railway-tram_stop-basic', 'railway-tram_stop-detail'],
        'query': '(select way, "name" from planet_osm_point where "railway"=\'tram_stop\')'
    },
    'hw-item-bus_stop': {
        'order': 3054,
        'styles': ['highway-bus_stop-basic', 'highway-bus_stop-detail'],
        'query': '(select way, "name" from planet_osm_point where "highway"=\'bus_stop\')'
    },
    'aerial-item-station': {
        'order': 3055,
        'styles': ['aerial_way-item-basic', 'aerial_way-item-name'],
        'query': '(select way, "name" from planet_osm_point where "aerialway"=\'station\')'
    },
    'amenity-item-parking': {
        'order': 3056,
        'styles': ['amenity-area-item-parking'],
        'query': '(select way, "name", "access" from planet_osm_polygon where "amenity"=\'parking\')'
    },
    'tourism-item-picnic': {
        'order': 3057,
        'styles': ['tourism_item-picnic'],
        'query': '(select way, "name" from planet_osm_point where "tourism"=\'picnic_site\')'
    },
    'leisure-area-playground-detail': {
        'order': 3058,
        'styles': ['leisure-area-playground-icon'],
        'query': '(select way from planet_osm_polygon where "leisure"=\'playground\')'
    },
    'leisure-item-playground': {
        'order': 3059,
        'styles': ['leisure-item-playground-icon'],
        'query': '(select way from planet_osm_point where "leisure"=\'playground\')'
    },
    'emergency-area': {
        'order': 3060,
        'styles': ['emergency-area-item'],
        'query': '(select way, "name" from planet_osm_polygon where "emergency"=\'phone\')'
    },
    'emergency-item': {
        'order': 3061,
        'styles': ['emergency-item'],
        'query': '(select way, "name" from planet_osm_point where "emergency"=\'phone\')'
    },
    'shop-area-c': {
        'order': 3062,
        'styles': ['shop-area-item-c-basic'],
        'query': '(select way, "name" from planet_osm_polygon where "shop" in (\'newsagent\', \'kiosk\'))'
    },
    'shop-item-c': {
        'order': 3063,
        'styles': ['shop-item-c-basic'],
        'query': '(select way, "name" from planet_osm_point where "shop" in (\'newsagent\', \'kiosk\'))'
    },
    'amenity-area-food-c': {
        'order': 3064,
        'styles': ['amenity-area-item-food-c-basic'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity"=\'ice_cream\')'
    },
    'amenity-item-food-c': {
        'order': 3065,
        'styles': ['amenity-item-food-c-basic'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'ice_cream\')'
    },
    'tourism-item-guidepost': {
        'order': 3066,
        'styles': ['tourism_item-guidepost'],
        'query': '(select way, "name", "information" from planet_osm_point where "tourism"=\'information\')'
    },
    'tourism-item-viewpoint': {
        'order': 3067,
        'styles': ['tourism_item-viewpoint'],
        'query': '(select way, "name" from planet_osm_point where "tourism"=\'viewpoint\')'
    },
    'amenity-item-parking_tickets': {
        'order': 3068,
        'styles': ['amenity-item-parking_tickets-basic'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'vending_machine\' and '
                 '"vending"=\'parking_tickets\')'
    },
    'amenity-item-bus_tickets': {
        'order': 3069,
        'styles': ['amenity-item-bus_tickets-basic'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'vending_machine\' and '
                 '"vending"=\'public_transport_tickets\')'
    },
    'amenity-item-atm': {
        'order': 3070,
        'styles': ['amenity-item-atm-basic'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'atm\')'
    },
    'amenity-item-post_box': {
        'order': 3071,
        'styles': ['amenity-item-post_box-basic'],
        'query': '(select way, "name" from planet_osm_point where "amenity"=\'post_box\')'
    },
    'barrier-item': {
        'order': 3072,
        'styles': ['barrier-item-basic'],
        'query': '(select way, "name", "barrier" from planet_osm_point where "barrier" in (\'toll_booth\', '
                 '\'swing_gate\', \'lift_gate\', \'gate\'))'
    },
    'rw-item-crossing': {
        'order': 3073,
        'styles': ['railway-crossing-basic'],
        'query': '(select way, "name" from planet_osm_point where "railway" in (\'crossing\', \'level_crossing\'))'
    },
    'hw-item-lights': {
        'order': 3074,
        'styles': ['highway-lights-basic'],
        'query': '(select way, "name" from planet_osm_point where "highway"=\'traffic_signals\')'
    },
    'amenity-area-nature': {
        'order': 3075,
        'styles': ['amenity-area-item-nature'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'hunting_stand\'))'
    },
    'amenity-item-nature': {
        'order': 3076,
        'styles': ['amenity-item-nature'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'hunting_stand\'))'
    },
    'leisure-area-nature': {
        'order': 3077,
        'styles': ['leisure-area-item-nature'],
        'query': '(select way, "name", "leisure" from planet_osm_polygon where "leisure" in (\'fishing\', \'firepit\'))'
    },
    'leisure-item-nature': {
        'order': 3078,
        'styles': ['leisure-item-nature'],
        'query': '(select way, "name", "leisure" from planet_osm_point where "leisure" in (\'fishing\', \'firepit\'))'
    },
    'amenity-area-city': {
        'order': 3079,
        'styles': ['amenity-area-item-city'],
        'query': '(select way, "name", "amenity" from planet_osm_polygon where "amenity" in (\'shelter\', \'toilets\', '
                 '\'telephone\', \'bench\', \'drinking_water\'))'
    },
    'amenity-item-city': {
        'order': 3080,
        'styles': ['amenity-item-city'],
        'query': '(select way, "name", "amenity" from planet_osm_point where "amenity" in (\'shelter\', \'toilets\', '
                 '\'telephone\', \'bench\', \'drinking_water\'))'
    },
    'amenity-area-bin': {
        'order': 3081,
        'styles': ['amenity-area-item-bin'],
        'query': '(select way, "name" from planet_osm_polygon where "amenity" in (\'waste_basket\', \'waste_disposal\') '
                 'or ("amenity"=\'recycling\' and "recycling_type"=\'container\'))'
    },
    'amenity-item-bin': {
        'order': 3082,
        'styles': ['amenity-item-bin'],
        'query': '(select way, "name" from planet_osm_point where "amenity" in (\'waste_basket\', \'waste_disposal\') '
                 'or ("amenity"=\'recycling\' and "recycling_type"=\'container\'))'
    },
    'building-area-name': {
        'order': 3083,
        'styles': ['building-area-name'],
        'query': '(select way, "name" from planet_osm_polygon where "building" is not null and "name" is not null '
                 'and ST_Area(way, true) > {})',
        'min_area': 0
    },
    'building-area-number': {
        'order': 3084,
        'styles': ['building-area-number'],
        'query': '(select way, "addr:streetnumber" from planet_osm_polygon where "building" is not null and '
                 '"name" is null and "addr:streetnumber" is not null and ST_Area(way, true) > {})',
        'min_area': 0
    },
    'building-item-number': {
        'order': 3085,
        'styles': ['building-item-number'],
        'query': '(select way, "addr:streetnumber" from planet_osm_point where "addr:streetnumber" is not null)'
    },
    'hw-path-oneway': {
        'order': 3086,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway" in (\'path\', \'cycleway\', \'bridleway\') and '
                 ' "oneway" is not null)'
    },
    'hw-tertiary-link-oneway': {
        'order': 3087,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary_link\' and "oneway" is not null)'
    },
    'hw-secondary-link-oneway': {
        'order': 3088,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary_link\' and "oneway" is not null)'
    },
    'hw-primary-link-oneway': {
        'order': 3089,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway"=\'primary_link\' and "oneway" is not null)'
    },
    'hw-highway-link-oneway': {
        'order': 3090,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway" in (\'motorway_link\', \'trunk_link\') and "oneway" is not null)'
    },
    'hw-service-oneway': {
        'order': 3091,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway" in (\'service\', \'unclassified\') and "oneway" is not null)'
    },
    'hw-residential-oneway': {
        'order': 3092,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway" in (\'residential\', \'pedestrian\') and "oneway" is not null)'
    },
    'hw-tertiary-oneway': {
        'order': 3093,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway"=\'tertiary\' and "oneway" is not null)'
    },
    'hw-secondary-oneway': {
        'order': 3094,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway"=\'secondary\' and "oneway" is not null)'
    },
    'hw-primary-oneway': {
        'order': 3095,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway"=\'primary\' and "oneway" is not null)'
    },
    'hw-highway-oneway': {
        'order': 3096,
        'styles': ['hw-oneway'],
        'query': '(select way from planet_osm_line where "highway" in (\'motorway\', \'trunk\') and "oneway" is not null)'
    }
}

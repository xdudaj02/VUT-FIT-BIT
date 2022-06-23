"""
This file acts as controller in MVC - servers views for different endpoints.

file:   app.py
author: Jakub Duda, xdudaj02
date:   8. 5. 2022
"""

import os
import json
import base64
from flask import Flask
from flask import jsonify, make_response, render_template, request

import map_util
import map
import blind_map

app = Flask(__name__)


@app.route('/')
@app.route("/home/", methods=['GET'])
def home():
    """Returns view for home page.

    :return: View for home page.
    """
    return render_template('index.html')


@app.route("/new-classic/", methods=['GET'])
def new_classic():
    """Returns view for more or less blind map generation page.

    :return: View for more or less blind map generation page.
    """
    return render_template('new_classic.html')


@app.route("/new-blind/", methods=['GET'])
def new_blind():
    """Returns view for completely blind map generation page.

    :return: View for completely blind map generation page.
    """
    return render_template('new_blind.html')


@app.route("/new-style/", methods=['GET'])
def new_style():
    """Returns view for style set definition page.

    :return: View for style set definition page. Includes dictionary containing all options and data for preview image.
    """
    # load style set options
    with open('data/style_options.json', 'r') as file:
        data = file.read()
        options = json.loads(data)

    # create preview
    filename = map.make_map([16.5863, 49.2173, 16.6061, 49.2345], [300, 400], 'custom', 'png',
                            custom_style_data={}, path='user_files/preview')
    with open(filename, 'rb') as file_raw:
        base64_data = base64.b64encode(file_raw.read()).decode('utf8')
    try:
        os.remove(filename)
    except OSError:
        pass
    return render_template('new_style.html', data=base64_data, options=options)


@app.route("/create-blind/", methods=['POST'])
def create_blind():
    """Generates and returns a completely blind map.

    :return: Data of generated completely blind map.
    """
    if request.data:
        data = json.loads(request.data)

        # get parameters
        map_area = data['area'] if type(data['area']) is list else [data['area']]
        map_size = data['size']
        map_config_on = (data['type'] if type(data['type']) is list else [data['type']]) if 'type' in data else []
        map_config_name = (data['names'] if type(data['names']) is list else [data['names']]) if 'names' in data else []
        map_use = data['use']

        # generate map
        file = blind_map.make_map(map_area, map_size, map_config_on, map_config_name, map_use,
                                  path='user_files/generated')
        with open(file, 'rb') as file_raw:
            base64_data = base64.b64encode(file_raw.read()).decode('utf8')
        try:
            os.remove(file)
        except OSError:
            pass
        if file:
            return make_response(jsonify({'success': True, 'extension': file.split('.')[-1], 'data': base64_data}), 200)
        else:
            return make_response(jsonify({'success': False}), 200)


@app.route("/create-classic/", methods=['POST'])
def create_classic():
    """Generates and returns a more or less blind map.

    :return: Data of more or less completely blind map.
    """
    if request.form:
        data = request.form.to_dict()

        # get parameters
        try:
            gpx_count = int(data['gpx_count'])
            custom_ppi = data['ppi_custom'] if 'ppi_custom' in data else None
            map_ppi = map.get_ppi(data['ppi'], custom_ppi)
            map_extent = map.get_extent(data['area_left'], data['area_bottom'], data['area_right'], data['area_top'])
            map_size = [map.get_pixel(data['size_x'], data['size_unit'], map_ppi),
                        map.get_pixel(data['size_y'], data['size_unit'], map_ppi)]
            map_type = data['type']
            map_format = data['format']
            map_proj = data['projection']
            custom_type = data['custom_style_type']
            custom_saved_data = data['custom_saved'] if data['custom_style_type'] == 'saved' else None
        except KeyError:
            return make_response(jsonify({'success': False}), 200)

        file_data = request.files
        # get gpx files
        gpx_data = []
        all_gpx_filenames = []
        if gpx_count:
            for i in range(1, gpx_count + 1):
                gpx_files = file_data.getlist("file_" + str(i))
                gpx_filenames = []
                for file in gpx_files:
                    filename = map_util.save_file('user_files/loaded_gpx', file, 'gpx')
                    gpx_filenames.append(filename)
                gpx_color = data['file_' + str(i) + '_color']
                gpx_data.append([gpx_color, gpx_filenames])
                all_gpx_filenames += gpx_filenames

        # get custom style set definition
        custom_style_data = None
        if map_type == 'custom':
            if custom_type == 'file':
                custom_style_file = file_data['custom_file']
                if custom_style_file:
                    custom_style_data = json.loads(custom_style_file.read())
            elif custom_type == 'saved':
                custom_style_data = json.loads(custom_saved_data)

        # generate map
        file = map.make_map(map_extent, map_size, map_type, map_format, gpx_data, custom_style_data, map_ppi=map_ppi,
                            map_proj=map_proj, path='user_files/generated')

        # remove gpx files
        for x in all_gpx_filenames:
            try:
                os.remove(x)
            except OSError:
                pass

        if file:
            with open(file, 'rb') as file_raw:
                base64_data = base64.b64encode(file_raw.read()).decode('utf8')
            try:
                os.remove(file)
            except OSError:
                pass
            return make_response(jsonify({'success': True, 'data': base64_data, 'extension': file.split('.')[-1]}), 200)
        else:
            return make_response(jsonify({'success': False}), 200)


@app.route("/check-json/", methods=['POST'])
def check_json():
    """Checks validity of given style set defintion JSON file.

    :return: Response indicating validity of given file.
    """
    file = request.files['file']
    if file:
        style_data = json.loads(file.read())
        if map.check_style_file(style_data):
            return make_response(jsonify({'success': True}), 200)
    return make_response(jsonify({'success': False}), 200)


@app.route("/get-style/", methods=['POST'])
def get_style():
    """Handles importing of style set definition in style set definition tool. Gets style set definition for template
    or checks validity of imported file and returns its content. In case of invalid style set definition returns
    indication of error.

    :return: Parsed style set definition in serialized JSON format.
    """
    if request.form:
        data = request.form.to_dict()
        if data['import_type'] == 'user':
            if request.files:
                file = request.files['user_style_input']
                if file:
                    style_data = json.loads(file.read())
                    if map.check_style_file(style_data):
                        return make_response(jsonify({'success': True, 'data': style_data}), 200)
        if data['import_type'] == 'template':
            style_data = map.get_template_config(data['template_style_input'])
            if style_data:
                return make_response(jsonify({'success': True, 'data': style_data}), 200)
    return make_response(jsonify({'success': False}), 200)


@app.route("/get-preview/", methods=['POST'])
def get_preview():
    """Creates a preview map for given parameters.

    :return: Data of generated preview map.
    """
    if request.data:
        data = json.loads(request.data)
        config = json.loads(data['json'])
        filename = map.make_map([float(data['left']), float(data['bottom']), float(data['right']), float(data['top'])],
                                [300, 400], 'custom', 'png', custom_style_data=config, path='user_files/preview')
        if filename:
            with open(filename, 'rb') as file_raw:
                base64_data = base64.b64encode(file_raw.read()).decode('utf8')
            try:
                os.remove(filename)
            except OSError:
                pass
            return make_response(jsonify({'success': True, 'data': base64_data}), 200)
    return make_response(jsonify({'success': False}), 200)


@app.route("/get-zoom/", methods=['POST'])
def get_zoom():
    """Adjusts style set definition to given zoom level.

    :return: Adjusted style set definition.
    """
    if request.data:
        data = json.loads(request.data)
        config = json.loads(data['json'])
        zoom = int(data['zoom']) - 1

        if map.check_style_file(config):
            config = map.adjust_to_zoom(config, zoom)
            return make_response(jsonify({'success': True, 'data': config}), 200)
    return make_response(jsonify({'success': False}), 200)


@app.errorhandler(404)
def not_found(e):
    """Handles occurrence of error type 404.

    :return: View for 404 error.
    """
    return render_template("404.html")


if __name__ == '__main__':
    app.run()

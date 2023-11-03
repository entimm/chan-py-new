from flask import Blueprint, render_template

import config
from data_process.chan import Chan

data_blueprint = Blueprint('data', __name__)


@data_blueprint.route('/')
def get_index():
    return render_template('index.html')


@data_blueprint.route('/data')
def get_data():
    chan = Chan('sh.000001')
    chan.load('2020-01-01', '2023-09-30')
    bar_list = [{
        'timestamp': item.time,
        'open': item.open,
        'high': item.high,
        'low': item.low,
        'close': item.close,
        'volume': item.volume
    } for item in chan.bar_union_manager.bar_iter()]

    bar_union_list = [{
        'begin': {'timestamp': item.time_begin, 'value': item.low},
        'end': {'timestamp': item.time_end, 'value': item.high}
    } for item in chan.bar_union_manager.list]

    fractal_list = [{
        'direction': item.fractal_type.name,
        'timestamp': item.fractal_time,
        'value': item.fractal_value,
    } for item in chan.bar_union_manager.fractal_iter()]

    stroke_list = [{
        'name': f'笔{item.index}',
        'is_sure': item.is_ok,
        'direction': item.direction.name,
        'begin': {'timestamp': item.fractal_start.fractal_time, 'value': item.fractal_start.fractal_value},
        'end': {'timestamp': item.fractal_end.fractal_time, 'value': item.fractal_end.fractal_value},
    } for item in chan.stroke_manager.list]

    segment_list = [{
        'name': f'段{item.index}',
        'is_sure': item.is_ok,
        'direction': item.direction.name,
        'begin': {'timestamp': item.stroke_list[0].fractal_start.fractal_time, 'value': item.stroke_list[0].fractal_start.fractal_value},
        'end': {'timestamp': item.stroke_list[-1].fractal_end.fractal_time, 'value': item.stroke_list[-1].fractal_end.fractal_value},
    } for item in chan.segment_manager.list]

    data = {'bar_list': bar_list}
    if config.output_union: data['bar_union_list'] = bar_union_list
    if config.output_fractal: data['fractal_list'] = fractal_list
    if config.output_stroke: data['stroke_list'] = stroke_list
    if config.output_segment: data['segment_list'] = segment_list

    return data

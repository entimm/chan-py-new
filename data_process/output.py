import config
from data_process.chan import Chan


def data(chan: Chan):
    bar_list = [{
        'timestamp': item.time,
        'open': item.open,
        'high': item.high,
        'low': item.low,
        'close': item.close,
        'volume': item.volume
    } for item in chan.bar_union_manager.bar_iter()]

    bar_union_list = [{
        'index': item.index,
        'begin': {'timestamp': item.time_start, 'value': item.low},
        'end': {'timestamp': item.time_end, 'value': item.high}
    } for item in chan.bar_union_manager.list]

    fractal_list = [{
        'index': item.index,
        'direction': item.fractal_type.name,
        'timestamp': item.fractal_time,
        'value': item.fractal_value,
    } for item in chan.bar_union_manager.fractal_iter()]

    stroke_list = [{
        'index': item.index,
        'is_sure': item.is_ok,
        'direction': item.direction.name,
        'begin': {'timestamp': item.fractal_start.fractal_time, 'value': item.fractal_start.fractal_value},
        'end': {'timestamp': item.fractal_end.fractal_time, 'value': item.fractal_end.fractal_value},
    } for item in chan.stroke_manager.list if item.len > 0]

    segment_list = [{
        'index': item.index,
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

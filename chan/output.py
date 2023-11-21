from chan import chan_config
from chan.chan import Chan


def data(chan: Chan):
    bar_list = [{
        'timestamp': item.time,
        'open': item.open,
        'high': item.high,
        'low': item.low,
        'close': item.close,
        'volume': item.volume
    } for item in chan.data_list]

    def get_time(index):
        return bar_list[index]['timestamp']

    bar_union_list = [{
        'index': item.index,
        'begin': {'timestamp': get_time(item.start), 'value': item.low},
        'end': {'timestamp': get_time(item.end), 'value': item.high}
    } for item in chan.bar_union_manager.list]

    fractal_list = [{
        'index': item.index,
        'direction': item.fractal_type.name,
        'timestamp': get_time(item.fractal_index),
        'value': item.fractal_value,
    } for item in chan.bar_union_manager.fractal_iter()]

    stroke_list = [{
        'index': item.index,
        'is_sure': item.is_ok,
        'direction': item.direction.name,
        'begin': {'timestamp': get_time(item.fractal_start.fractal_index), 'value': item.fractal_start.fractal_value},
        'end': {'timestamp': get_time(item.fractal_end.fractal_index), 'value': item.fractal_end.fractal_value},
    } for item in chan.stroke_manager.list if item.len > 0]

    segment_list = [{
        'index': item.index,
        'is_sure': item.is_ok,
        'status': item.status.name,
        'is_trend_1f': item.is_trend_1f,
        'direction': item.direction.name,
        'begin': {'timestamp': get_time(item.stroke_list[0].fractal_start.fractal_index), 'value': item.stroke_list[0].fractal_start.fractal_value},
        'end': {'timestamp': get_time(item.stroke_list[-1].fractal_end.fractal_index), 'value': item.stroke_list[-1].fractal_end.fractal_value},
    } for item in chan.segment_manager.list if item.len >= 3]

    data = {'bar_list': bar_list}
    if chan_config.output_union: data['bar_union_list'] = bar_union_list
    if chan_config.output_fractal: data['fractal_list'] = fractal_list
    if chan_config.output_stroke: data['stroke_list'] = stroke_list
    if chan_config.output_segment: data['segment_list'] = segment_list

    data['output_text'] = chan_config.output_text

    return data

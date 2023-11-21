from flask import Blueprint, render_template, request

import config
from data_fetch import manager as fetch_manager
from data_fetch.fetcher import Fetcher
from data_process.chan_manager import ChanManager
from common.const import PeriodEnum
from data_process import output
from data_process.chan import Chan

data_blueprint = Blueprint('resources', __name__)

chan_manager = ChanManager()


@data_blueprint.route('/')
def get_index():
    return render_template('index.html')


@data_blueprint.route('/data')
def get_data():
    ticker = request.args.get('ticker', 'sh.000001')
    start = request.args.get('start', '2020-01-01')
    end = request.args.get('end', '2023-09-30')
    period_name = request.args.get('period', 'D')

    try:
        period = PeriodEnum.__members__[period_name]
    except KeyError:
        period = PeriodEnum.D

    fetcher_cls = fetch_manager.get_fetcher(config.data_src)
    fetcher: Fetcher = fetcher_cls(ticker=ticker, start=start, end=end, period=period)

    chan = Chan()
    chan.load(fetcher.get_kl_data())
    chan_id = chan_manager.register(chan)

    data = output.data(chan)
    data['chan_id'] = chan_id

    return data


@data_blueprint.route('/update/<chan_id>')
def update(chan_id):
    chan = chan_manager.get(chan_id)
    if chan is None:
        return []

    # chan.append([])

    data = output.data(chan)
    data['chan_id'] = chan_id

    return data

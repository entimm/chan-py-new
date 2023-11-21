from flask import Blueprint, render_template, request

import config
from data_fetch import manager as fetch_manager
from data_fetch.fetcher import Fetcher
from chan.chan_manager import ChanManager
from common.const import PeriodEnum
from chan import output
from chan.chan import Chan

blueprint = Blueprint('chart', __name__)

chan_manager = ChanManager()


@blueprint.route('/chart')
def view():
    return render_template('chart.html')


@blueprint.route('/chart/data')
def data():
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


@blueprint.route('/chart/update/<chan_id>')
def update(chan_id):
    chan = chan_manager.get(chan_id)
    if chan is None:
        return []

    # chan.append([])

    data = output.data(chan)
    data['chan_id'] = chan_id

    return data

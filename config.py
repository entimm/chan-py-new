from common.const import AdjType
from data_fetch.manager import DataSrc

# 数据源
adj_type = AdjType.QFQ
data_src = DataSrc.LOCAL
local_data_file_name = "sh.000001"
kline_len = 5000
step_skip = kline_len

# 输出
output_text = False
output_fractal = True
output_union = False
output_stroke = True
output_segment = True

from data_process.element.stroke import Stroke


class Segment:
    def __init__(self, stroke_start, stroke_end):
        # 开始笔
        self.stroke_start: Stroke = stroke_start
        # 结束笔
        self.stroke_end: Stroke = stroke_end
        # 长度
        self.len = 0
        if stroke_end is not None:
            self.len = stroke_end.index - stroke_start.index
        # 是否确认
        self.is_ok = False

        self.index = 0

        self.direction = stroke_start.direction

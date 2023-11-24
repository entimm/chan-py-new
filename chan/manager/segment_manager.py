from typing import List

from chan.chan_const import SegmentStatus, Direction
from chan.element.abs_stroke import AbsStroke
from chan.element.segment import Segment
from logger import logger


class SegmentManager:
    def __init__(self):
        self.list: List[Segment] = []

    def add_stroke(self, stroke: AbsStroke):
        logger.info(f'投喂笔给线段 {stroke}')
        if stroke.len == 0:
            return
        if len(self.list) == 0:
            self.append_with_stroke(stroke)
            return

        last_segment = self.list[-1]

        # 处理丢弃笔
        last_stroke = last_segment.stroke_list[-1]
        if stroke.index < last_stroke.index:
            # self.process_dropped(stroke)
            self.process_multi_dropped(stroke, last_segment)
            return

        self.handle(last_segment, stroke)

    def handle(self, last_segment: Segment, stroke: AbsStroke):
        """
        投喂笔形成线段
        由于笔会生长，所以相同的笔会返回进来
        """
        if last_segment.stroke_list[-1].index == stroke.index:
            logger.info(f'线段同笔更新{last_segment}')

            if len(self.list) >= 2 and last_segment.len == 1:
                pre_segment = self.list[-2]
                if pre_segment.check_if_add(stroke):
                    self.cancel_last_segment()
                    self.add_stroke_in_segment(pre_segment, stroke)

            # 笔生长时更新极点,并可能触发笔破坏
            last_segment.update_vertex(stroke)
            self.handle_break(last_segment)

            return

        if last_segment.check_if_add(stroke):
            self.add_stroke_in_segment(last_segment, stroke)
            return

        self.append_with_stroke(stroke)

    def add_stroke_in_segment(self, last_segment: Segment, stroke: AbsStroke):
        """
        往当天的线段中投喂笔
        """
        last_segment.add_stroke(stroke)
        # 实笔诞生
        if len(self.list) >= 2 and last_segment.len >= 3:
            self.list[-2].is_ok = True
        # 线段长度变更后可能触发笔破坏
        self.handle_break(last_segment)

    def append_with_stroke(self, stroke: AbsStroke):
        segment = Segment(len(self.list), stroke)

        logger.info(f'新增线段: {segment}')

        self.list.append(segment)

    def handle_break(self, last_segment):
        """
        处理线段破坏
        """
        if last_segment.status == SegmentStatus.BREAK:
            if len(self.list) == 1:
                # 第一根线段看多几根笔,这个if条件也可不需要
                if self.list[-1].len >= 4:
                    last_segment.rebase()
            if len(self.list) >= 2:
                self.list[-2].merge(last_segment)
                self.cancel_last_segment()
                # 合并过完如果存在反向突破，则拆分并继续与前一线段进行部分合并
                if len(self.list) >= 2:
                    self.try_split()

    def try_split(self):
        """
        与前一线段的正向极点进行比对后合并
        """
        pre_segment = self.list[-2]
        last_segment = self.list[-1]
        if pre_segment.direction == Direction.UP:
            if Segment.top_vertex_higher(pre_segment, last_segment):
                self.split_then_merge(pre_segment, last_segment, last_segment.top_stroke)
        if pre_segment.direction == Direction.DOWN:
            if Segment.bottom_vertex_lower(pre_segment, last_segment):
                self.split_then_merge(pre_segment, last_segment, last_segment.bottom_stroke)

    def split_then_merge(self, pre_segment: Segment, last_segment: Segment, stroke: AbsStroke):
        """
        拆分后进行合并
        """
        logger.info(f'{pre_segment} split_then_merge {last_segment} 用 {stroke}')
        out_stroke_list: list[AbsStroke] = []
        in_stroke_list: list[AbsStroke] = []
        for item in last_segment.stroke_list:
            if item.index <= stroke.index:
                out_stroke_list.append(item)
            else:
                in_stroke_list.append(item)

        # 笔移除合并到前一根线段中
        if len(out_stroke_list) > 0:
            pre_segment.set_stroke_list(pre_segment.stroke_list + out_stroke_list)
            Segment.merge_vertex(pre_segment, last_segment)
            last_segment.status = SegmentStatus.MERGE
            last_segment.is_ok = False

        self.cancel_last_segment()
        # 剩余的笔重新添加
        if len(in_stroke_list) > 0:
            for item in in_stroke_list:
                self.add_stroke(item)

    def process_one_dropped(self, stroke: AbsStroke):
        """
        处理单笔丢弃的情况
        更加高效巧妙，不需要重新处理之前不变的笔
        该方法暂时废弃，因为他不具备通用性
        """
        logger.info(f'线段处理丢弃 {stroke}')
        # 把最近的那个线段中的笔暂存以便重新处理，然后丢弃
        reprocess_stroke_list = self.list[-1].stroke_list
        self.cancel_last_segment()
        # 暂存笔里面移除被丢弃的笔
        dropped_stroke = reprocess_stroke_list.pop()

        append_reprocess_stroke_list = []
        # 如果暂存笔现在空了，从当前的上个线段取出最后一根笔存进去
        if len(reprocess_stroke_list) == 0:
            append_reprocess_stroke_list.append(self.list[-1].stroke_list[-1])
        # 因为丢弃的笔也从暂存笔中也被丢弃了，所以如果当前的笔和丢弃笔位置相同，则加进去
        # 如果有，他也一定是最新的笔
        if stroke.index == dropped_stroke.index:
            append_reprocess_stroke_list.append(stroke)

        reprocess_stroke_list = reprocess_stroke_list + append_reprocess_stroke_list

        logger.info(f'重新处理笔列表大小 {len(reprocess_stroke_list)}, 关键的笔:{len(append_reprocess_stroke_list)}笔 {[str(item) for item in append_reprocess_stroke_list]}')

        # 逐跟处理所有暂存笔
        for item in reprocess_stroke_list:
            self.add_stroke(item)

    def process_multi_dropped(self, stroke: AbsStroke, last_segment):
        """
        处理多笔丢弃的情况
        可能会重新处理之前不变的笔
        """
        logger.info(f'线段处理多个丢弃 {stroke}')
        # 把最近的那个线段中的笔暂存以便重新处理
        reprocess_stroke_list = []
        # 把涉及到的线段都丢掉
        while stroke.index < last_segment.stroke_list[-1].index:
            reprocess_stroke_list = last_segment.stroke_list + reprocess_stroke_list
            self.cancel_last_segment()
            if len(self.list) >= 1:
                last_segment = self.list[-1]
            else:
                break

        reprocess_stroke_list = [item for item in reprocess_stroke_list if item.index < stroke.index]
        reprocess_stroke_list.append(stroke)

        # 逐跟处理所有暂存笔
        for item in reprocess_stroke_list:
            self.add_stroke(item)

    def cancel_last_segment(self):
        segment = self.list.pop()
        logger.info(f'线段被丢弃 {segment}')


import re
from datetime import datetime

from .nayose import convert_ascii


def calc_publish_plug(raw_sentence: str | float) -> int:
    if type(raw_sentence) is float:
        return 4
    han_mode = convert_ascii(raw_sentence)
    return int(han_mode[0])


def build_publish_conditions(publish_flag: int, raw_sentence: str | float) -> list[int]:
    if publish_flag == 1:
        return []
    if publish_flag == 4:
        return [4]
    reason_indexes = re.findall(r"\d+", convert_ascii(raw_sentence))
    return [int(reason_index) for reason_index in reason_indexes]


def build_miniature(raw_sentence: str | float) -> int:
    print(raw_sentence, type(raw_sentence))
    if type(raw_sentence) is float:
        return -1
    base_target = raw_sentence.split("-")[-1]
    base_target = base_target.split("・")[-1]
    target = int(base_target.replace(",", ""))
    return target


def build_published_at(raw_sentence: str | float) -> datetime | None:
    if type(raw_sentence) is float:
        return None
    if raw_sentence == "不明":
        return None
    base_target = raw_sentence.split("-")[-1]
    base_target = base_target.split("・")[-1]

    return datetime(int(base_target), 1, 1)

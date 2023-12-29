from mojimoji import zen_to_han  # pylint: disable=E0611


def convert_ascii(target: str | float):
    if type(target) is float:
        # データが存在しない場合のnanがfloat型扱いだったのでその場合の処理
        target = "nan"
    return zen_to_han(target, kana=False, digit=True, ascii=True)

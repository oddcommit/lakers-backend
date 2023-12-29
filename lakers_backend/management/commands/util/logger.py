import os
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LogFileWriter:
    log_dir: str
    file_name: str

    @property
    def log_path(self):
        return os.path.join(self.log_dir, self.file_name)

    def write_log(self, sentence: str):
        os.makedirs(self.log_dir, exist_ok=True)
        now_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        write_sentence = f"{now_str}: {sentence}"
        print(write_sentence)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.writelines(write_sentence)

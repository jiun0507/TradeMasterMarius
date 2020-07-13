import enum

class reply(enum.Enum):
    sleep = "동동이가 잠 들었습니다.\n"
    no_work = "동동이가 할 일이 없어서 잠들었습니다..\n"
class button_text(enum.Enum):
    wake_up = "동동이를 꺠워주세요."
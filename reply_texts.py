import enum

class reply(enum.Enum):
    sleep = "마리우스가 잠 들었습니다.\n"
    no_work = "마리우스가 할 일이 없어서 잠들었습니다..\n"
class button_text(enum.Enum):
    wake_up = "마리우스를 꺠워주세요."
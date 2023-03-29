class ActionType:
    click = "click"


class NotificationType:
    paused = "PAUSED"
    stopped = "STOPPED"
    completed = "COMPLETED"


class DetectType:
    color = "color"
    noverify = "noverify"
    image = "image"


class Action:
    def __init__(
        self,
        action_type,
        x,
        y,
        r,
        g,
        b,
        repeat,
        notification,
            detect):
        self.action_type = action_type
        self.x = int(x)
        self.y = int(y)
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.repeat = int(repeat)
        self.notification = eval(notification)
        self.detect = detect

    def getActionString(self):
        return f'{self.action_type} {self.x} {self.y} {self.r} {self.g} {self.b} {self.repeat} {self.notification} {self.detect}'


class Settings:
    loops_done = 0

    def __init__(
            self,
            replay_loops,
            click_delay_min,
            click_delay_max,
            notification_delay,
            notification_loops):
        self.replay_loops = int(replay_loops)
        self.click_delay_min = float(click_delay_min)
        self.click_delay_max = float(click_delay_max)
        self.notification_delay = float(notification_delay)
        self.notification_loops = int(notification_loops)

    def getSettingsColumns(self):
        return f'#settings loops minDelay maxDelay notifDelay notifLoops'

    def getSettingsString(self):
        return f'settings {self.replay_loops} {self.click_delay_min} {self.click_delay_max} {self.notification_delay} {self.notification_loops}'


class ScriptLogInfo:
    def __init__(self, time_ran, loops_ran, retries):
        self.time_ran = time_ran
        self.loops_ran = loops_ran
        self.retries = retries

    def getScriptLogInfoString(self):
        return f'= time ran: {self.time_ran}\n= average time: {float(self.time_ran)/float(self.loops_ran)}\n= loops ran: {self.loops_ran}\n= retries: {self.retries}'

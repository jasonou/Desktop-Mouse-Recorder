class ActionType:
    click = "click"


class NotificationType:
    paused = "paused"
    stopped = "stopped"

class DetectType:
    color = "color"
    noverify = "noverify"
    image = "image"


class Action:
    def __init__(self, action_type, x, y, r, g, b, notification, detect):
        self.action_type = action_type
        self.x = int(x)
        self.y = int(y)
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.notification = eval(notification)
        self.detect = detect

    def getActionString(self):
        return f'{self.action_type} {self.x} {self.y} {self.r} {self.g} {self.b} {self.notification} {self.detect}'


class Settings:
    loops_done = 0

    def __init__(
            self,
            replay_loops,
            log_comments,
            log_actions,
            log_debug,
            click_delay_min,
            click_delay_max,
            notification_delay,
            notification_loops):
        self.replay_loops = float(replay_loops)
        self.log_comments = eval(log_comments)
        self.log_actions = eval(log_actions)
        self.log_debug = eval(log_debug)
        self.click_delay_min = float(click_delay_min)
        self.click_delay_max = float(click_delay_max)
        self.notification_delay = float(notification_delay)
        self.notification_loops = float(notification_loops)

    def getSettingsString(self):
        return f'settings {self.replay_loops} {self.log_comments} {self.log_actions} {self.log_debug} {self.click_delay_min} {self.click_delay_max} {self.notification_delay} {self.notification_loops}'

import os
import random
import winsound

ALERTS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'alerts'
)

ALERTS = list(
    os.path.join(ALERTS_PATH, alert)
    for alert in os.listdir(ALERTS_PATH)
    if os.path.isfile(os.path.join(ALERTS_PATH, alert))
    and alert.split('.')[-1].lower() == 'wav'
)


class SoundOperation:

    @staticmethod
    def choice_random_alert() -> os.PathLike | None:
        return random.choice(ALERTS)

    @staticmethod
    def execute_audio(path: os.PathLike) -> None:
        winsound.PlaySound(path, winsound.SND_ASYNC)

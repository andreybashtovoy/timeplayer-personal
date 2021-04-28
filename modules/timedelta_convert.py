import datetime


def td_to_dict(td: datetime.timedelta) -> dict:
    def __t(t, n):
        if t < n:
            return t, 0
        v = t // n

        return t - (v * n), v

    (s, h) = __t(td.seconds, 3600)
    (s, m) = __t(s, 60)
    (micS, milS) = __t(td.microseconds, 1000)

    return {
        'days': td.days,
        'hours': h,
        'minutes': m,
        'seconds': s,
        'milliseconds': milS,
        'microseconds': micS
    }

import arrow


def get_time_diff(arrow_time_obj: arrow.arrow.Arrow, granularity=['day', 'hour', 'minute']):
    return arrow_time_obj.humanize(
        only_distance=True,
        locale='zh',
        granularity=granularity
    )

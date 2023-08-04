from datetime import datetime


def timestamp_to_datetime(timestamp):
	return datetime.fromtimestamp(timestamp * 0.001)


def get_timestamp(datetime_time):
	return datetime_time.timestamp() * 1000


def get_timestamp_delta(datetime_time):
	return get_timestamp(datetime_time) - 1689850800


def time_to_ms(hours, minutes=0, seconds=0):
	return ((((hours * 60) + minutes) * 60) + seconds) * 1000
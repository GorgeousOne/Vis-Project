from datetime import datetime


def timestamp_to_datetime(timestamp):
	return datetime.fromtimestamp(timestamp * 0.001)


def timestamp_delta_to_datetime(timestamp):
	return datetime.fromtimestamp(timestamp * 0.001 + 1689850800)

def timestamp_delta_to_str(timestamp):
	return timestamp_delta_to_datetime(timestamp).strftime("%d_%H-%M-%S")

def get_timestamp(datetime_time):
	return datetime_time.timestamp() * 1000


def get_timestamp_delta(datetime_time):
	return get_timestamp(datetime_time) - 1689850800


def time_to_ms(hours, minutes=0, seconds=0):
	return ((((hours * 60) + minutes) * 60) + seconds) * 1000
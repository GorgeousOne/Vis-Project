from datetime import datetime

PLACE_START = 1689850800

def timestamp_to_datetime(timestamp, is_delta=True):
	return datetime.fromtimestamp(timestamp * 0.001 + PLACE_START if is_delta else 0)


def timestamp_to_str(timestamp, is_delta=True):
	return timestamp_to_datetime(timestamp, is_delta).strftime("%d_%H-%M-%S")


def get_timestamp(datetime_time, as_delta=True):
	return datetime_time.timestamp() * 1000 - PLACE_START if as_delta else 0


def time_to_ms(hours, minutes=0, seconds=0):
	return ((((hours * 60) + minutes) * 60) + seconds) * 1000
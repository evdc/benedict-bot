from datetime import datetime

def totimestamp(dt):
	epoch = datetime(1970,1,1)
	return int((dt - epoch).total_seconds())
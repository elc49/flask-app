class Config(object):
	"""Common configurations
	"""
	 
class Development(Config):
	"""Development configurations
	"""
	DEBUG = True
	SQLALCHEMY_ECHO = True # for sqlalchemy logging
	SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(Config):
	"""Production configurations
	"""
	DEBUG = False

app_config = {
	"development": Development,
	"production": Production
}

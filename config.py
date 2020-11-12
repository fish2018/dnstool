from loguru import logger
import time

# loguru
logger.add('logs/{time}.log', encoding='utf-8', level="INFO", rotation='00:00', retention='10 days',
           compression='zip', colorize=True,
           format="<green>{time}</green> <level>{message}</level>")

class AliDnsConf:
    AccessKeyID=''
    AccessKeySecret=''
    ZoneId=""

class WinDnsConf:
    wmrTarget = 'http://xxx:5985/wsman'
    userName = ''
    passWord = ''
    Zone = ''


class DevelopmentConfig(AliDnsConf, WinDnsConf):
    Records = [] # Ingress Controller hosts
    Domains = [] # ingress domains


APP_ENV = DevelopmentConfig

from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from img_pro import monitoring_thread
class UserConfig(AppConfig):
    name = 'User'

    # def ready(self):
    #         autodiscover_modules('monitoring_thread.py')
    #         moni_thread=monitoring_thread.MonitoringThread("foolish")
    #         moni_thread.start()
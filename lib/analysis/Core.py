from lib.adb import Device
from lib.model import Application
from lib.receiver.Frida import Frida
from lib.receiver.Proxy import Proxy

import logging
import time


class Core:

    def __init__(self, configuration, device: Device, module, path: str):
        self.configuration = configuration
        self.device = device
        self.path = path
        self.module = module
        self.timeout = configuration['ANALYSIS'].getint('analysis_timeout')

        self.current_application = None
        self.receivers = []

    def select_applications(self):
        logging.debug("Core:select_applications()")
        return self.module.select(self.path)

    def start_analysis(self):
        logging.debug("Core:start_analysis()")

        apk_paths = self.select_applications()

        if self.configuration['ANALYSIS'].getboolean('use_proxy'):
            self.device.install_certificate(self.configuration['PROXY'].get('proxy_certificate'))

        if self.configuration['ANALYSIS'].getboolean('use_frida'):
            Frida.compile(configuration=self.configuration)
            self.device.install_frida()

        for apk in apk_paths:
            self.analyse_sample(apk)

    def analyse_sample(self, apk_path):
        logging.debug("Core:analyse_sample()")

        self.current_application = Application.Application(apk_path)

        logging.info(f"Package name: {self.current_application.package}")
        logging.info(f"Main activity: {self.current_application.get_main_activity()}")
        logging.info(f"Path : {self.current_application.path}")
        logging.info(f"SHA256 : {self.current_application.get_sha256_hash()}")

        time_init = time.time()

        module = self.module(self.current_application)

        self.device.install_application(self.current_application.path)
        self.start_receivers(module)

        current_time = 0
        while current_time < self.timeout :
            current_time = time.time() - time_init
            logging.debug(current_time)
            time.sleep(1)

        self.stop_receivers()
        self.device.uninstall_application(self.current_application.package)

    def start_receivers(self, module):

        logging.debug("Core:start_receivers()")

        use_frida = self.configuration['ANALYSIS'].getboolean('use_frida')
        use_proxy = self.configuration['ANALYSIS'].getboolean('use_proxy')

        if use_proxy:
            proxy = Proxy(self.configuration['PROXY'], module)
            proxy.start()
            self.receivers.append(proxy)

        if use_frida:
            frida = Frida(self.configuration['FRIDA'], module, self.device)
            frida.start()
            self.receivers.append(frida)
        else:
            self.device.launch_application(self.current_application.package)

        logging.debug("Core:start_receivers() -> Started")

    def stop_receivers(self):

        logging.debug("Core:stop_receivers()")

        for i in range(len(self.receivers)):
            self.receivers[i].stop()

        self.receivers = []

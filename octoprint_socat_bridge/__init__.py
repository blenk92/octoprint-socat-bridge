# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os
import subprocess

class SocatBridgePlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin):
    def on_after_startup(self):
        socat_bin = os.path.join(os.path.dirname(__file__), "tools", "socat")
        while True:
            device_path = self._settings.get(["device_path"])
            host = self._settings.get(["host"])
            port = self._settings.get(["port"])
            args = [socat_bin, "pty,link={},raw".format(device_path), "tcp:{}:{}".format(host, port)]
            self._logger.info("running %s" % " ".join(args))
            subprocess.run(args)


    def get_settings_defaults(self):
        return dict(
            device_path="/dev/virtualcom0",
            host="esp3d.local",
            port="8888"
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_assets(self):
        return dict(
            js=["js/socat_bridge.js"],
            css=["css/socat_bridge.css"],
            less=["less/socat_bridge.less"]
        )

__plugin_name__ = "Socat Bridge"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = SocatBridgePlugin()

# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import re


class Pause_managementPlugin(octoprint.plugin.SettingsPlugin,
                             octoprint.plugin.AssetPlugin,
                             octoprint.plugin.TemplatePlugin
                             ):

    # ~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "pause_positions": [],
            "pause_command": "M600",
            "pause_command_ignored": "M600",
            "layer_indicator": "@PAUSE_POSITION",
            "ignore_enabled": False
        }

    # ~~ AssetPlugin mixin

    def get_assets(self):
        return {
            "css": ["css/pause_management.css"],
            "js": ["js/pause_management.js"]
        }

    # ~~ gcode queueing hook
    def process_gcode(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        # check to see if we need to inject a pause
        if cmd and cmd.startswith(self._settings.get(["layer_indicator"])):
            injection_check = cmd.replace(self._settings.get(["layer_indicator"]), "").strip()
            if injection_check in self._settings.get(["pause_positions"]):
                self._logger.debug(f"Injecting pause command at position: {injection_check}")
                return [cmd, self._settings.get(["pause_command"])]

        # exit early otherwise and return original line
        if gcode != self._settings.get(["pause_command_ignored"]):
            return

        # remove the command from the queue for sending to printer
        if self._settings.get_boolean(["ignore_enabled"]):
            self._logger.debug(f"Ignoring pause command: {cmd}")
            return None,

    # ~~ TemplatePlugin mixin
    def get_template_configs(self):
        return [{"type": "settings", "template": "pause_management_settings.jinja2", "custom_bindings": True},
                {"type": "sidebar", "icon": "pause", "custom_bindings": True,
                 "template": "pause_management_sidebar.jinja2",
                 "template_header": "pause_management_sidebar_header.jinja2"}]

    # ~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "pause_management": {
                "displayName": "Pause Management",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "jneilliii",
                "repo": "OctoPrint-PauseManagement",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/jneilliii/OctoPrint-PauseManagement/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Pause Management"
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Pause_managementPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.process_gcode,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

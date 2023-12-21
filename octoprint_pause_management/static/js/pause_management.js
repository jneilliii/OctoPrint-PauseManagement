/*
 * View model for Pause Management
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function Pause_managementViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];
        self.new_pause_position = ko.observable();

        self.onBeforeBinding = function() {
            self.pause_positions_sorted = ko.pureComputed(function() {
                return self.settingsViewModel.settings.plugins.pause_management.pause_positions.sorted().reverse();
            });
        };

        self.onToggleIgnoreEnabled = function(data) {
            if(self.settingsViewModel.settings.plugins.pause_management.ignore_enabled()) {
                self.settingsViewModel.settings.plugins.pause_management.ignore_enabled(false);
            } else {
                self.settingsViewModel.settings.plugins.pause_management.ignore_enabled(true);
            }
            self.settingsViewModel.saveData();
        };

        self.addPausePosition = function(data) {
            if(self.settingsViewModel.settings.plugins.pause_management.ignore_enabled()) {
                self.new_pause_position("");
                $("#new_position_modal").modal("show");
            }
        };

        self.removeAllPausePositions = function (data) {
            if(self.settingsViewModel.settings.plugins.pause_management.ignore_enabled()) {
                self.settingsViewModel.settings.plugins.pause_management.pause_positions.removeAll();
                self.settingsViewModel.saveData();
            }
        };

        self.insertPosition = function() {
            if(self.new_pause_position() !== "" && !self.settingsViewModel.settings.plugins.pause_management.pause_positions().includes(self.new_pause_position())) {
                self.settingsViewModel.settings.plugins.pause_management.pause_positions.push(self.new_pause_position());
                self.settingsViewModel.saveData();
            }
            $("#new_position_modal").modal("hide");
        };

        self.removePausePosition = function(data) {
            self.settingsViewModel.settings.plugins.pause_management.pause_positions.remove(data);
            self.settingsViewModel.saveData();
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: Pause_managementViewModel,
        dependencies: [ "settingsViewModel" ],
        elements: [ "#settings_plugin_pause_management", "#sidebar_plugin_pause_management_wrapper" ]
    });
});

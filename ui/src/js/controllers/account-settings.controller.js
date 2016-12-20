(function() {
    'use strict';

    angular.module('wau')
            .controller('AccountSettingsController', accountSettingsController);

    accountSettingsController.$inject = ['$rootScope', '$location', 'Notification', 'User'];

    function accountSettingsController($rootScope, $location, Notification, User) {
        $rootScope.goBack = true;

        var vm = this;
        vm.user = angular.copy($rootScope.user);
        vm.save = saveUser;
        vm.reset = resetUser;

        ////////////////////////////

        function saveUser() {
            vm.user.$save(function (user, headers) {
                Notification.success("User settings saved successfully!");
                $location.path('/');
            });
        }

        function resetUser() {
            vm.user = angular.copy($rootScope.user);
        }
    }
}) ();
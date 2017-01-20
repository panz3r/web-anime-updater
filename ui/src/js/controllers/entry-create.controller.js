(function() {
    'use strict';

    angular.module('wau')
            .controller('EntryCreateController', entryCreateController);

    entryCreateController.$inject = ['$rootScope', '$routeParams', '$location', 'Notification', 'Anime'];

    function entryCreateController($rootScope, $routeParams, $location, Notification, Anime) {
        $rootScope.goBack = true;

        var vm = this;
        vm.series = new Anime();
        vm.save = saveAnime;

        ////////////////////////////

        function saveAnime() {
            vm.series.$save(function (entry, headers) {
                Notification.success("New entry added successfully!");
                $location.path('/');
            });
        }
    }
}) ();
(function() {
    'use strict';

    angular.module('wau')
            .controller('EntryListController', entryListController);

    entryListController.$inject = ['$rootScope', 'Anime'];

    function entryListController($rootScope, Anime) {
        $rootScope.goBack = false;

        var vm = this;
        vm.series = getSeries();

        //////////////////////////

        function getSeries() {
            return Anime.query();
        }
    }
}) ();
(function() {
    'use strict';

    angular.module('wau')
            .controller('EntryDetailsController', entryDetailsController);

    entryDetailsController.$inject = ['$rootScope', '$routeParams', '$location', 'Anime', 'Episode'];

    function entryDetailsController($rootScope, $routeParams, $location, Anime, Episode) {
        $rootScope.goBack = true;

        var vm = this;

        var entryId = $routeParams.entryId;
        vm.anime = Anime.get({entryId: entryId});
        vm.episodes = Episode.query({entryId: entryId});
    }
}) ();
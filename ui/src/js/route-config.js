(function() {
    'use strict';

    angular.module('wau')
            .config(config)
            .run(init);

    config.$inject = ['$routeProvider', '$locationProvider', '$qProvider'];

    function config($routeProvider, $locationProvider, $qProvider) {
        $routeProvider
            .when('/', {
                templateUrl:  '/static/views/entries/list.html',
                controller:   'EntryListController',
                controllerAs: 'vm'
            })
            .when('/anime/new', {
                templateUrl:  '/static/views/entries/create.html',
                controller:   'EntryCreateController',
                controllerAs: 'vm'
            })
            .when('/anime/:entryId', {
                templateUrl:  '/static/views/entries/detail.html',
                controller:   'EntryDetailsController',
                controllerAs: 'vm'
            })
            .when('/settings', {
                templateUrl:  '/static/views/entries/settings.html',
                controller:   'AccountSettingsController',
                controllerAs: 'vm'
            })
            .otherwise({redirectTo: '/'});

        // use the HTML5 History API
        $locationProvider.html5Mode(true);

        // Try to fix not working notifications
        $qProvider.errorOnUnhandledRejections(false);
    }

    init.$inject = ['$rootScope', 'User'];

    function init($rootScope, User) {
        $rootScope.user = new User.get();
    }
}) ();
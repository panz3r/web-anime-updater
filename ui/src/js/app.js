angular.module("webanimeupdater.services", ['ngResource', 'ngRoute']).
    factory('Entry', function ($resource) {
        var Entry = $resource('/api/v1/entries/:entryId', {entryId: '@id'});
        Entry.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return Entry;
    })
    .factory('SubEntry', function ($resource) {
        var SubEntry = $resource('/api/v1/subentries/:entryId', {entryId: '@id'});
        SubEntry.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return SubEntry;
    })
    .factory('User', function ($resource) {
        var User = $resource('/api/v1/user');
        User.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return User;
    });

angular.module("getanime", ["webanimeupdater.services"]).
    config(function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {templateUrl: '/static/views/entries/list.html', controller: EntryListController})
            .when('/anime/new', {templateUrl: '/static/views/entries/create.html', controller: EntryCreateController})
            .when('/anime/:entryId', {templateUrl: '/static/views/entries/detail.html', controller: EntryDetailController})
            .when('/settings', {templateUrl: '/static/views/entries/settings.html', controller: AccountSettingsController});

        // use the HTML5 History API
        $locationProvider.html5Mode(true);
    });

function EntryListController($scope, $rootScope, Entry) {
    $rootScope.goBack = false;
    $scope.entries = Entry.query();
}

function EntryCreateController($scope, $rootScope, $routeParams, $location, Entry) {
    $rootScope.goBack = true;

    $scope.entry = new Entry();

    $scope.save = function () {
    	$scope.entry.$save(function (entry, headers) {
    		toastr.success("New entry added successfully!");
            $location.path('/');
        });
    };
}

function EntryDetailController($scope, $rootScope, $routeParams, $location, Entry, SubEntry) {
    $rootScope.goBack = true;

    var entryId = $routeParams.entryId;
    $scope.entry = Entry.get({entryId: entryId});
    $scope.subentries = SubEntry.query({entryId: entryId});
}

function AccountSettingsController($scope, $rootScope, $location, User) {
    $rootScope.goBack = true;

    $scope.user = User.get();
}

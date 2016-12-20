(function() {
    'use strict';

    angular.module('wau')
           .factory('Episode', episode);

    episode.$inject = ['$resource'];

    function episode($resource) {
        var SubEntry = $resource('/api/v1/subentries/:entryId', {entryId: '@id'});
        SubEntry.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return SubEntry;
    }
}) ();
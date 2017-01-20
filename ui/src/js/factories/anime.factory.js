(function() {
    'use strict';

    angular.module('wau')
           .factory('Anime', anime);

    anime.$inject = ['$resource'];

    function anime($resource) {
        var Entry = $resource('/api/v1/entries/:entryId', {entryId: '@id'});
        Entry.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        };
        return Entry;
    }
}) ();
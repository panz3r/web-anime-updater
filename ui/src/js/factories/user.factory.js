(function() {
    'use strict';

    angular.module('wau')
           .factory('User', user);

    user.$inject = ['$resource'];

    function user($resource) {
        var User = $resource('/api/v1/user');
        User.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return User;
    }
}) ();
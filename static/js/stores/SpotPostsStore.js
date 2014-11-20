var EventEmitter = require('events').EventEmitter;
var merge = require('react/lib/merge');

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var Actions = require('../actions/Actions');
var xhr = require('../utils/xhr');

// local fields HERE

var SpotPostsStore = merge(EventEmitter.prototype, {

  getState: function() {
    return {
    };
  },

  emitChange: function() {
    this.emit(Constants.CHANGE_EVENT);
  },

  addChangeListener: function(callback) {
    this.on(Constants.CHANGE_EVENT, callback);
  },

  removeChangeListener: function(callback) {
    this.removeListener(Constants.CHANGE_EVENT, callback);
  }
});

SpotPostsStore.dispatchToken = AppDispatcher.register(function(payload) {
  var action = payload.action;

  switch(action.actionType) {
    default:
      return true;
  }

  SpotPostsStore.emitChange();

  return true;
});

module.exports = SpotPostsStore;

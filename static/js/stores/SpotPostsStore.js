var EventEmitter = require('events').EventEmitter;
var merge = require('react/lib/merge');

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var Actions = require('../actions/Actions');
var xhr = require('../utils/xhr');
var SPOTPOST = require('../utils/SPOTPOST');

// local fields HERE
var _spotPosts = [];
var _opState = {
  isLoading: true,
  edit: {
    isEditing: false,
    isSpotPost: false,
    isComment: false,
    id: -1
  },
  user: {}
}

var _getSpotPostsState = function() {
  Actions.refreshUserStatus();
  Actions.updateSpotPosts();
  return {
    spotPosts: _spotPosts,
    opState: _opState
  };
};

var SpotPostsStore = merge(EventEmitter.prototype, {

  getState: function() {
    return _getSpotPostsState();
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
    case Constants.UPVOTE_SPOTPOST:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getSpotPostUpvoteUrl(action.spotPostId))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
      
    case Constants.UPVOTE_SPOTPOST:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getSpotPostDownvoteUrl(action.spotPostId))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
      
    case Constants.GET_SPOTPOSTS:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getGetUrl())
        .success(function(data) {
          _opState.isLoading = false;
          _spotPosts = data;
          console.log('SPOTPOSTS');
          console.log(_spotPosts);
        });
      break;
      
    case Constants.REFRESH_USER_STATUS:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getUserStatusUrl())
        .success(function(data) {
          _opState.isLoading = false;
          _opState.user = data;
          console.log('USER');
          console.log(_opState.user);
        });
      break;
      
    case Constants.EDIT_SPOTPOST:
      _opState.edit = {
        isSpotPost: true,
        isComment: false,
        isEditing: true,
        id: action.spotPostId
      };
      break;
    
    case Constants.SUBMIT_EDIT_SPOTPOST:
      _opState.isLoading = true;
      xhr('POST', getSpotPostUpdateUrl(), action.spotPost)
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
    
    case Constants.CANCEL_EDIT_SPOTPOST:
      _opState.edit = {
        isSpotPost: false,
        isComment: false,
        isEditing: false,
        id: -1
      };
      break;
    
    case Constants.DELETE_SPOTPOST:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getSpotPostDeleteUrl(action.spotPostId))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
      
    default:
      return true;
  }

  SpotPostsStore.emitChange();

  return true;
});

module.exports = SpotPostsStore;

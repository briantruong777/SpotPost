var EventEmitter = require('events').EventEmitter;
var merge = require('react/lib/merge');

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var Actions = require('../actions/Actions');
var xhr = require('../utils/xhr');
var SPOTPOST = require('../utils/SPOTPOST');

// local fields HERE
var _onPageLoad = true;
var _spotPosts = [];
var _opState = {
  isLoading: true,
  edit: {},
  user: {}
}

var _getSpotPostsState = function() {
  if (_onPageLoad) {
    _clearEdit();
    Actions.refreshUserStatus();
    Actions.updateSpotPosts();
    _onPageLoad = false;
  }
  return {
    spotPosts: _spotPosts,
    opState: _opState
  };
};

var _clearEdit = function() {
  _opState.edit = {
    isEditing: false,
    editSpotPost: false,
    spotPostId: -1,
    editComment: false,
    newComment: false,
    commentId: -1,
    errorMessage: undefined
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
      
    case Constants.DOWNVOTE_SPOTPOST:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getSpotPostDownvoteUrl(action.spotPostId))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
      
    case Constants.GET_SPOTPOSTS:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getSpotPostGetUrl())
        .success(function(data) {
          _opState.isLoading = false;
          _spotPosts = data;
          SpotPostsStore.emitChange();
        });
      break;
      
    case Constants.REFRESH_USER_STATUS:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getUserStatusUrl())
        .success(function(data) {
          _opState.isLoading = false;
          _opState.user = data;
          SpotPostsStore.emitChange();
        });
      break;
      
    case Constants.EDIT_SPOTPOST:
      _opState.edit.isEditing = true;
      _opState.edit.editSpotPost = true;
      _opState.edit.spotPostId = action.spotPostId;
      break;
    
    case Constants.SUBMIT_EDIT_SPOTPOST:
      var spotPostUpdate = action.spotPostUpdate;
      _clearEdit();
      _opState.isLoading = true;
      console.log(JSON.stringify(spotPostUpdate));
      xhr('POST', SPOTPOST.getSpotPostUpdateUrl(), JSON.stringify(spotPostUpdate))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
    
    case Constants.CANCEL_EDIT:
      _clearEdit();
      break;
    
    case Constants.DELETE_SPOTPOST:
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getSpotPostDeleteUrl(action.spotPostId))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
      
    case Constants.COMMENT:
      _opState.edit.isEditing = true;
      _opState.edit.newComment = true;
      _opState.edit.spotPostId = action.spotPostId;
      break;
      
    case Constants.SUBMIT_COMMENT:
      var spotPostId = action.spotPostId;
      var content = action.content;
      if (content === undefined || content === null || content.length === 0) {
        _opState.edit.errorMessage = "No content";
        break;
      }
      
      _clearEdit();
      _opState.isLoading = true;
      var commentObject = {
        message_id: spotPostId,
        content: content
      };
      xhr('POST', SPOTPOST.getCommentPostUrl(), JSON.stringify(commentObject))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
    
    case Constants.EDIT_COMMENT:
      // no support for editing comments
      break;
      
    case Constants.SUBMIT_EDIT_COMMENT:
      // no support for editing comments
      break;
      
    case Constants.CLEAR_EDIT_ERROR:
      _opState.edit.errorMessage = undefined;
      break;
      
    case Constants.UPVOTE_COMMENT:
      var commentId = action.commentId;
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getCommentUpvoteUrl(commentId))
        .success(function(data) {
          Actions.updateSpotPosts();
        });
      break;
      
    case Constants.DOWNVOTE_COMMENT:
      var commentId = action.commentId;
      _opState.isLoading = true;
      xhr('GET', SPOTPOST.getCommentDownvoteUrl(commentId))
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

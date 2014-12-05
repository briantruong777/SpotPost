var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

var Actions = {

  // LOGIN actions
  submitSignIn: function(username, password) {
    AppDispatcher.handleViewAction({
      actionType: Constants.SUBMIT_SIGN_IN,
      username: username,
      password: password
    });
  },
  
  submitRegister: function(username, password, password2, email) {
    AppDispatcher.handleViewAction({
      actionType: Constants.SUBMIT_REGISTER,
      username: username,
      password: password,
      password2: password2,
      email: email
    });
  },
  
  clearSignInError: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.CLEAR_SIGN_IN_ERROR
    });
  },
  
  clearRegisterError: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.CLEAR_REGISTER_ERROR
    });
  },
  
  // SPOTPOST actions
  updateSpotPosts: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.GET_SPOTPOSTS
    });
  },
  
  upvoteSpotPost: function(spotPostId) {
    AppDispatcher.handleViewAction({
      actionType: Constants.UPVOTE_SPOTPOST,
      spotPostId: spotPostId
    });
  },
  
  downvoteSpotPost: function(spotPostId) {
    AppDispatcher.handleViewAction({
      actionType: Constants.DOWNVOTE_SPOTPOST,
      spotPostId: spotPostId
    });
  },
  
  refreshUserStatus: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.REFRESH_USER_STATUS
    });
  },
  
  editSpotPost: function(spotPostId) {
    AppDispatcher.handleViewAction({
      actionType: Constants.EDIT_SPOTPOST,
      spotPostId: spotPostId
    });
  },
  
  submitEditSpotPost: function(spotPost) {
    AppDispatcher.handleViewAction({
      actionType: Constants.SUBMIT_EDIT_SPOTPOST,
      spotPost: spotPost
    });
  },
  
  cancelEdit: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.CANCEL_EDIT
    });
  },
  
  deleteSpotPost: function(spotPostId) {
    AppDispatcher.handleViewAction({
      actionType: Constants.DELETE_SPOTPOST,
      spotPostId: spotPostId
    });
  },
  
  comment: function(spotPostId) {
    AppDispatcher.handleViewAction({
      actionType: Constants.COMMENT,
      spotPostId: spotPostId
    });
  },
  
  submitComment: function(spotPostId, content) {
    AppDispatcher.handleViewAction({
      actionType: Constants.SUBMIT_COMMENT,
      spotPostId: spotPostId,
      content: content
    });
  },
  
  editComment: function(spotPostId, commentId) {
    AppDispatcher.handleViewAction({
      actionType: Constants.EDIT_COMMENT,
      spotPostId: spotPostId,
      commentId: commentId
    });
  },
  
  submitEditComment: function(comment) {
    AppDispatcher.handleViewAction({
      actionType: Constants.SUBMIT_EDIT_COMMENT,
      comment: comment
    });
  },
  
  clearEditError: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.CLEAR_EDIT_ERROR
    });
  }

};

module.exports = Actions;

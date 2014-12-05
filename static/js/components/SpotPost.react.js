/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPostUserControls = require('./SpotPostUserControls.react.js');
var SpotPostOwnerControls = require('./SpotPostOwnerControls.react.js');
var Comments = require('./Comments.react.js');
var Actions = require('../actions/Actions');
var ErrorMessage = require('./ErrorMessage.react');

var ENTER_KEY = 13;

var SpotPost = React.createClass({

  _spotPost: undefined,
  _opState: undefined,

  _onClickSubmitEdit: function(event) {
    event.preventDefault();
    var spotPostUpdate = {
      id: this._spotPost.id,
      title: this.refs.newTitle.state.value,
      content: this.refs.newContent.state.value
    };
    Actions.submitEditSpotPost(spotPostUpdate);
  },
  
  _clearError: function() {
    var error = this._opState.edit.errorMessage;
    if (error !== undefined && error !== null) {
      Actions.clearEditError();
    }
  },
  
  _onClickCancel: function(event) {
    event.preventDefault();
    Actions.cancelEdit();
  },
  
  _onKeyDown: function(event) {
    this._clearError();
    if (event.keyCode === ENTER_KEY) {
      this._submit();
    }
  },

  render: function() {
    var spotPost = this.props.spotPost;
    var opState = this.props.opState;
    
    this._spotPost = spotPost;
    this._opState = opState;
    
    var edit = opState.edit;
    var isLoading = opState.isLoading;
    var user = opState.user;
    
    var comments = spotPost.comments;
    
    // if own post, display similar spotPost but with edit/delete controls
    // controls variable, two different kinds of controls:
    // - ownerControls
    // - userControls
    
    if (user.username === spotPost.user.username && edit.spotPostId === spotPost.id && edit.commentId < 0) {
      var title = spotPost.title;
      var content = spotPost.content;
      var error = opState.edit.errorMessage;
      return (
        <div>
          <input ref="newTitle" type="text" onKeyDown={this._onKeyDown} defaultValue={title} onChange={this._handleTitleChange} placeholder="SpotPost Title" disabled={isLoading} />
          <input ref="newContent" type="text" onKeyDown={this._onKeyDown} defaultValue={content} placeholder="SpotPost Content" disabled={isLoading} />
          <button onClick={this._onClickSubmitEdit} >Submit</button>
          <button onClick={this._onClickCancel} >Cancel</button>
          <ErrorMessage error={error} />
        </div>
      )
    }
    
    var Controls = undefined;
    if (user.username === spotPost.user.username) {
      Controls = SpotPostOwnerControls;
    }
    else {
      Controls = SpotPostUserControls;
    }
    
    return (
      <div>
        <p><b>{spotPost.title}</b></p>
        <p>{spotPost.user.username} at {spotPost.time}</p>
        <p>{spotPost.content}</p>
        <p>Reputation: {spotPost.reputation}</p>
        <Controls spotPost={spotPost} opState={opState} />
        <Comments spotPost={spotPost} opState={opState} />
      </div>
    );
  }

});

module.exports = SpotPost;

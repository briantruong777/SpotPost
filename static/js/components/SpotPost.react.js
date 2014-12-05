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
    
    if (user.username === spotPost.user.username && edit.spotPostId === spotPost.id && edit.commentId < 0 && !edit.newComment) {
      var title = spotPost.title;
      var content = spotPost.content;
      var error = opState.edit.errorMessage;
      return (
        <div className="col-md-4 col-md-offset-4">
          <div className="panel panel-success">
            <div className="panel-heading">
              <input className="form-control" ref="newTitle" type="text" onKeyDown={this._onKeyDown} defaultValue={title} onChange={this._handleTitleChange} placeholder="SpotPost Title" disabled={isLoading} />
              <p><small>{spotPost.user.username} at {spotPost.time}</small></p>
            </div>
            <div className="row">
            <div className="col-md-10 col-md-offset-1">
              <div className="row">
                <input className="form-control" ref="newContent" type="text" onKeyDown={this._onKeyDown} defaultValue={content} placeholder="SpotPost Content" disabled={isLoading} />
              </div>
              <p>Reputation: {spotPost.reputation}</p>
              <button type="button" className="btn btn-primary" onClick={this._onClickSubmitEdit} >Submit</button>
              <button type="button" className="btn btn-default" onClick={this._onClickCancel} >Cancel</button>
              <ErrorMessage error={error} />
            </div>
            </div>
          </div>
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
      <div className="col-md-4 col-md-offset-4">
        <div className="panel panel-primary">
          <div className="panel-heading">
            <h3>{spotPost.title}</h3>
            <p><small>{spotPost.user.username} at {spotPost.time}</small></p>
          </div>
          <div className="col-md-10 col-md-offset-1">
            <h3>{spotPost.content}</h3>
            <p>Reputation: {spotPost.reputation}</p>
            <Controls spotPost={spotPost} opState={opState} />
          </div>
          <Comments spotPost={spotPost} opState={opState} />
        </div>
      </div>
    );
  }

});

module.exports = SpotPost;

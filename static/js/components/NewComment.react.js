/**
 * @jsx React.DOM
 */

var React = require('react');
var Actions = require('../actions/Actions');
var ErrorMessage = require('./ErrorMessage.react');

var ENTER_KEY = 13;

var NewComment = React.createClass({

  _spotPost: undefined,
  _opState: undefined,
  
  _onClickComment: function(event) {
    event.preventDefault();
    Actions.comment(this._spotPost.id);
  },
  
  _onClickCancel: function(event) {
    event.preventDefault();
    Actions.cancelEdit();
  },
  
  _onClickSubmit: function(event) {
    event.preventDefault();
    this._submit();
  },
  
  _submit: function() {
    Actions.submitComment(this._spotPost.id, this.refs.content.state.value);
  },
  
  _clearError: function() {
    var error = this._opState.edit.errorMessage;
    if (error !== undefined && error !== null) {
      Actions.clearEditError();
    }
  },

  _onKeyDown: function(event) {
    this._clearError();
    if (event.keyCode === ENTER_KEY) {
      this._submit();
    }
  },
  
  _clear: function() {
    this._clearError();
    this.refs.content.setState({
      value: null
    });
  },

  render: function() {
    var spotPost = this.props.spotPost;
    var opState = this.props.opState;
  
    this._spotPost = spotPost;
    this._opState = opState;
    
    var isLoading = opState.isLoading;
    var edit = opState.edit;
    if (edit.isEditing && edit.newComment && edit.spotPostId === spotPost.id) {
      var error = opState.edit.errorMessage;
      return (
        <div>
          <input ref="content" type="text" onKeyDown={this._onKeyDown} placeholder="Comment" />
          <button onClick={this._onClickSubmit} disable={isLoading}>Post</button>
          <button onClick={this._onClickCancel} disable={isLoading}>Cancel</button>
          <ErrorMessage error={error} />
        </div>
      );
    }
    
    var disable = edit.isEditing || isLoading;
    
    return (
      <div>
        <button onClick={this._onClickComment} disable={disable}>Comment</button>
      </div>
    );
  }

});

module.exports = NewComment;

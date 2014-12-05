/**
 * @jsx React.DOM
 */

var React = require('react');
var Actions = require('../actions/Actions');

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
    this._spotPost = this.props.spotPost;
    this._opState = this.props.opState;
    
    var isLoading = this._opState.isLoading;
    var edit = this._opState.edit;
    if (edit.isEditing && edit.newComment && edit.spotPostId === this._spotPost.id) {
      return (
        <div>
          <input ref="content" type="text" onKeyDown={this._onKeyDown} placeholder="Comment" />
          <button onClick={this._onClickSubmit} disable={isLoading}>Post</button>
          <button onClick={this._onClickCancel} disable={isLoading}>Cancel</button>
        </div>
      );
    }
    
    var disable = edit.isEditing || isLoading;
    
    return (
      <button onClick={this._onClickComment} disable={disable}>Comment</button>
    );
  }

});

module.exports = NewComment;

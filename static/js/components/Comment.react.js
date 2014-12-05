/**
 * @jsx React.DOM
 */

var React = require('react');
var Actions = require('../actions/Actions');

var Comment = React.createClass({

  _comment: undefined,

  _onClickPlus1: function(event) {
    event.preventDefault();
    Actions.upvoteComment(this._comment.id);
  },
  
  _onClickMinus1: function(event) {
    event.preventDefault();
    Actions.downvoteComment(this._comment.id);
  },

  render: function() {
    var comment = this.props.comment;
    var opState = this.props.opState;
    var isLoading = opState.isLoading;
    var isEditing = opState.edit.isEditing;
    
    var disable = isLoading || isEditing;
    
    this._comment = comment;
    
    return (
      <div>
        <p>{comment.username} at {comment.time}</p>
        <p>{comment.content}</p>
        <p>Reputation: {comment.reputation}</p>
        <button onClick={this._onClickPlus1} disable={disable} >+1</button>
        <button onClick={this._onClickMinus1} disable={disable} >-1</button>
      </div>
    );
  }

});

module.exports = Comment;

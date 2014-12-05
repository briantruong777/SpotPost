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
      <div className="row">
        <div className="panel panel-default">
          <div className="panel-heading">
            <h6>{comment.username} at {comment.time}</h6>
          </div>
          <div className="row">
            <div className="col-md-10 col-md-offset-1">
              <h5>{comment.content}</h5>
              <p>Reputation: {comment.reputation}</p>
              <button type="button" className="btn btn-success" onClick={this._onClickPlus1} disable={disable} >
                <span className="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span>
              </button>
              <button type="button" className="btn btn-danger" onClick={this._onClickMinus1} disable={disable} >
                <span className="glyphicon glyphicon-thumbs-down" aria-hidden="true"></span>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

});

module.exports = Comment;

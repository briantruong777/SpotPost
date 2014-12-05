/**
 * @jsx React.DOM
 */

var React = require('react');

var Comment = React.createClass({

  render: function() {
    var comment = this.props.comment;
    var opState = this.props.opState;
    console.log(comment);
    
    return (
      <div>
        <p>{comment.username} at {comment.time}</p>
        <p>{comment.content}</p>
      </div>
    );
  }

});

module.exports = Comment;

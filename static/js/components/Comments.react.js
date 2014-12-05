/**
 * @jsx React.DOM
 */

var React = require('react');
var Comment = require('./Comment.react');
var NewComment = require('./NewComment.react');

var Comments = React.createClass({

  _spotPost: undefined,
  _opState: undefined,

  _renderComment: function(comment) {
    return (<li><Comment comment={comment} opState={this._opState} /></li>);
  },
  
  _onClickComment: function(event) {
    event.preventDefault();
    Actions.comment(this._spotPost.id);
  },

  render: function() {
    this._spotPost = this.props.spotPost;
    this._opState = this.props.opState;
    
    var comments = this._spotPost.comments;
    
    return (
      <div>
        <ul>
          {comments.map(this._renderComment)}
        </ul>
        <NewComment spotPost={this._spotPost} opState={this._opState} />
      </div>
    );
  }

});

module.exports = Comments;

/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPostUserControls = require('./SpotPostUserControls.react.js');
var SpotPostOwnerControls = require('./SpotPostOwnerControls.react.js');
var Comments = require('./Comments.react.js');
var Actions = require('../actions/Actions');

var SpotPost = React.createClass({

  _spotPost: undefined,

  _onClickSubmitEdit: function(event) {
    event.preventDefault();
    //Actions.submitSpotPostEdit(this._spotPost);
    console.log('submit edit not implemented');
  },
  
  _onClickCancel: function(event) {
    event.preventDefault();
    Actions.cancelEdit();
  },

  render: function() {
    var spotPost = this.props.spotPost;
    var opState = this.props.opState;
    
    this._spotPost = spotPost;
    
    var edit = opState.edit;
    var isLoading = opState.isLoading;
    var user = opState.user;
    
    var comments = spotPost.comments;
    
    // if own post, display similar spotPost but with edit/delete controls
    // controls variable, two different kinds of controls:
    // - ownerControls
    // - userControls
    
    if (user.username === spotPost.user.username && edit.spotPostId === spotPost.id && edit.commentId < 0) {
      return (
        <div>
          <button onClick={this._onClickSubmitEdit} >Submit</button>
          <button onClick={this._onClickCancel} >Cancel</button>
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
        <p>Points: {spotPost.reputation}</p>
        <Controls spotPost={spotPost} opState={opState} />
        <Comments spotPost={spotPost} opState={opState} />
      </div>
    );
  }

});

module.exports = SpotPost;

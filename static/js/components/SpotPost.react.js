/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPostUserControls = require('./SpotPostUserControls.react.js');
var SpotPostOwnerControls = require('./SpotPostOwnerControls.react.js');
var Comments = require('./Comments.react.js');

var SpotPost = React.createClass({

  render: function() {
    var spotPost = this.props.spotPost;
    var opState = this.props.opState;
    
    var edit = opState.edit;
    var isLoading = opState.isLoading;
    var user = opState.user;
    
    var comments = spotPost.comments;
    
    // if own post, display similar spotPost but with edit/delete controls
    // controls variable, two different kinds of controls:
    // - ownerControls
    // - userControls
    
    if (user.username === spotPost.user.username && edit.isSpotPost && edit.id === spotPost.id) {
      return (
        <div>EDIT
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

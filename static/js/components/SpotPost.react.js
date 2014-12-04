/**
 * @jsx React.DOM
 */

var React = require('react');

var SpotPost = React.createClass({

  render: function() {
    var spotPost = this.props.spotPost;
    
    return (
      <div>
        <p><b>{spotPost.title}</b></p>
        <p>{spotPost.user.username} at {spotPost.time}</p>
        <p>{spotPost.content}</p>
        <p>Points: {spotPost.reputation}</p>
      </div>
    );
  }

});

module.exports = SpotPost;

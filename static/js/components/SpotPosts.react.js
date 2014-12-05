/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPost = require('./SpotPost.react');

var SpotPosts = React.createClass({

  _opState: undefined,

  _renderSpotPost: function(spotPost) {
    return (<li><SpotPost spotPost={spotPost} opState={this._opState} /></li>);
  },

  render: function() {
    var spotPosts = this.props.spotPosts;
    this._opState = this.props.opState;
    
    if (spotPosts === undefined) {
      return (<ul><li>No SpotPosts to display.</li></ul>);
    }
  
    return (
      <ul className="list-unstyled">
        {spotPosts.map(this._renderSpotPost)}
      </ul>
    );
  }

});

module.exports = SpotPosts;
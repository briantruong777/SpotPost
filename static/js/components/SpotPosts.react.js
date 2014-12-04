/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPost = require('./SpotPost.react');

var SpotPosts = React.createClass({

  _renderSpotPost: function(spotPost) {
    var edit = false;
    if (spotPost.id === editId) {
      edit = true;
    }
    return (<li><UserSpotPost spotPost={spotPost} edit={edit} isLoading={isLoading} /></li>);
  },

  render: function() {
    var spotPosts = this.props.spotPosts;
    var isLoading = this.props.isLoading;
    var editId = this.props.editId;
    
    if (spotPosts === undefined) {
      return (<ul><li>No SpotPosts to display.</li></ul>);
    }
  
    return (
      <ul>
        {spotPosts.map(this._renderSpotPost)}
      </ul>
    );
  }

});

module.exports = SpotPosts;
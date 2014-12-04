/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPost = require('./SpotPost.react');

var SpotPosts = React.createClass({

  passInfo: {
    editId: -1,
    isLoading: false
  },

  _renderSpotPost: function(spotPost) {
    var edit = false;
    if (spotPost.id === passInfo.editId) {
      edit = true;
    }
    return (<li><UserSpotPost spotPost={spotPost} edit={edit} isLoading={passInfo.isLoading} /></li>);
  },

  render: function() {
    var spotPosts = this.props.spotPosts;
    passInfo.isLoading = this.props.isLoading;
    passInfo.editId = this.props.editId;
    
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
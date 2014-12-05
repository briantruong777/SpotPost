/**
 * @jsx React.DOM
 */

var React = require('react');
var Actions = require('../actions/Actions');

var SpotPostUserControls = React.createClass({

  _spotPost: undefined,

  _onClickPlus1: function(event) {
    event.preventDefault();
    Actions.upvoteSpotPost(this._spotPost.id);
  },
  
  _onClickMinus1: function(event) {
    event.preventDefault();
    Actions.downvoteSpotPost(this._spotPost.id);
  },

  render: function() {
    var opState = this.props.opState;
    var spotPost = this.props.spotPost;
    var isEditing = opState.edit.isEditing;
    var isLoading = opState.isLoading;
    var disable = isEditing || isLoading;
    
    this._spotPost = spotPost;
    
    return (
      <div>
        <button onClick={this._onClickPlus1} disable={disable} >+1</button>
        <button onClick={this._onClickMinus1} disable={disable} >-1</button>
      </div>
    );
  }

});

module.exports = SpotPostUserControls;

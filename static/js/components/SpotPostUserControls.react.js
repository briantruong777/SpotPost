/**
 * @jsx React.DOM
 */

var React = require('react');

var SpotPostUserControls = React.createClass({

  _onClickPlus1: function(event) {
    event.preventDefault();
    Actions.upvoteSpotPost(this.state.spotPost.id);
  },
  
  _onClickMinus1: function(event) {
    event.preventDefault();
    Actions.downvoteSpotPost(this.state.spotPost.id);
  },

  render: function() {
    var opState = this.props.opState;
    var spotPost = this.props.spotPost
    var isEditing = opState.edit.isEditing;
    var isLoading = opState.isLoading;
    var disablePlus1 = isEditing || isloading;
    var disableMinus1 = isEditing || isloading;
    
    this.setState({
      spotPost: spotPost
    });
    
    return (
      <div>
        <button onClick={this._onClickPlus1} disable={disablePlus1} >+1</button>
        <button onClick={this._onClickMinus1} disable={disableMinus1} >-1</button>
      </div>
    );
  }

});

module.exports = SpotPostUserControls;

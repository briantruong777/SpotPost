/**
 * @jsx React.DOM
 */

var React = require('react');

var SpotPostOwnerControls = React.createClass({

  _onClickEdit: function(event) {
    event.preventDefault();
    Actions.editSpotPost(this.state.spotPost.id);
  },
  
  _onClickMinus1: function(event) {
    event.preventDefault();
    Actions.deleteSpotPost(this.state.spotPost.id);
  },

  render: function() {
    var opState = this.props.opState;
    var spotPost = this.props.spotPost;
    var isEditing = opState.edit.isEditing;
    var isLoading = opState.isLoading;
    var disable = isEditing || isLoading;
    
    this.setState({
      spotPost: spotPost
    });
    
    return (
      <div>
        <button onClick={this._onClickEdit} disable={disable} >Edit</button>
        <button onClick={this._onClickDelete} disable={disable} >Delete</button>
      </div>
    );
  }

});

module.exports = SpotPostOwnerControls;

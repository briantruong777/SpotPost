/**
 * @jsx React.DOM
 */

var React = require('react');
var Actions = require('../actions/Actions');

var SpotPostOwnerControls = React.createClass({

  _spotPost: undefined,

  _onClickEdit: function(event) {
    event.preventDefault();
    Actions.editSpotPost(this._spotPost.id);
  },
  
  _onClickDelete: function(event) {
    event.preventDefault();
    Actions.deleteSpotPost(this._spotPost.id);
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
        <button onClick={this._onClickEdit} disable={disable} >Edit</button>
        <button onClick={this._onClickDelete} disable={disable} >Delete</button>
      </div>
    );
  }

});

module.exports = SpotPostOwnerControls;

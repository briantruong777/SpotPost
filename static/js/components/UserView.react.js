/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPostsStore = require('../stores/SpotPostsStore');
var SpotPosts = require('./SpotPosts.react.js');
var SPOTPOST = require('../utils/SPOTPOST');

var _getUserViewState = function() {
  return SpotPostsStore.getState();
};

var UserView = React.createClass({

  getInitialState: function() {
    return _getUserViewState();
  },
  
  componentDidMount: function() {
    SpotPostsStore.addChangeListener(this._onChange);
  },

  componentWillUnmount: function() {
    SpotPostsStore.removeChangeListener(this._onChange);
  },

  _onChange: function() {
    this.setState(_getUserViewState());
  },
  
  _onClickLogout: function(event) {
    event.preventDefault();
    window.location.assign(SPOTPOST.getLogoutUrl());
  },

  render: function() {
    return (
      <div>
        <div className="jumbotron">
          <h1 className="text-center">Welcome to SpotPost</h1>
        </div>
        <button onClick={this._onClickLogout} >Logout</button>
        <SpotPosts spotPosts={this.state.spotPosts} opState={this.state.opState} />
      </div>
    );
  }

});

module.exports = UserView;

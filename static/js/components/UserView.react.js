/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPostsStore = require('../stores/SpotPostsStore');

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

  render: function() {
    
    return (
      <div>
        <h1 className="col-sm-offset-1 col-md-4">Welcome to SpotPost!</h1>
      </div>
    );
  }

});

module.exports = UserView;

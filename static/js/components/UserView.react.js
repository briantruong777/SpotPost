/**
 * @jsx React.DOM
 */

var React = require('react');
var SpotPostsStore = require('../stores/SpotPostsStore');
var SpotPosts = require('./SpotPosts.react.js');

var _spotPosts = [
  {
    id: 1,
    user: {
      username: 'usernameA',
      reputation: 123,
    },
    title: "titleA",
    content: "contentA",
    time: "1:23 PM 01/02/03",
    reputation: 1234
  },
  {
    id: 2,
    user: {
      username: 'usernameB',
      reputation: 234,
    },
    title: "titleB",
    content: "contentB",
    time: "2:34 PM 02/03/04",
    reputation: 2345
  },
  {
    id: 3,
    user: {
      username: 'usernameC',
      reputation: 345,
    },
    title: "titleC",
    content: "contentC",
    time: "3:45 PM 03/04/05",
    reputation: 3456
  },
  {
    id: 4,
    user: {
      username: 'usernameD',
      reputation: 567,
    },
    title: "titleD",
    content: "contentD",
    time: "4:56 PM 04/05/06",
    reputation: 4567
  }
];

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
        <a href="http://spotpost.me/_logout">Log out</a>
        <SpotPosts spotPosts={_spotPosts} />
      </div>
    );
  }

});

module.exports = UserView;

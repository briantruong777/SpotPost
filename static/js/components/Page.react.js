/**
 * @jsx React.DOM
 */

var React = require('react');
var LoginView = require('./LoginView.react');

var Page = React.createClass({

  render: function() {
    
    return (
      <div>
        <LoginView />
      </div>
    );
  }

});

module.exports = Page;

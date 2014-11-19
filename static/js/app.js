/**
 * @jsx React.DOM
 */

var React = require('react');

var LoginView = require('./components/LoginView.react');

var renderLoginPage = function() {
  React.renderComponent(
    <LoginView />,
    document.getElementById('loginApp')
  );
};

var renderUserPage = function() {
  React.renderComponent(
    <LoginView />,
    document.getElementById('app')
  );
};

if (document.getElementById('app')) {
  renderUserPage();
}

if (document.getElementById('loginApp')) {
  renderLoginPage();
}



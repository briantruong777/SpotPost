/**
 * @jsx React.DOM
 */

var React = require('react');

var LoginView = require('./components/LoginView.react');
var UserView = require('./components/UserView.react');

var renderLoginPage = function() {
  React.renderComponent(
    <LoginView />,
    document.getElementById('loginApp')
  );
};

var renderUserPage = function() {
  React.renderComponent(
    <UserView />,
    document.getElementById('app')
  );
};

if (document.getElementById('app')) {
  renderUserPage();
}
else if (document.getElementById('loginApp')) {
  renderLoginPage();
}



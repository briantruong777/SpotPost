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

console.log(document.getElementById('app'));
console.log(document.getElementById('loginApp'));
if (document.getElementById('app')) {
  console.log('USER PAGE');
  renderUserPage();
}
else if (document.getElementById('loginApp')) {
  console.log('LOGIN PAGE');
  renderLoginPage();
}



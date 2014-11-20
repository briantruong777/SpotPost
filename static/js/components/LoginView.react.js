/**
 * @jsx React.DOM
 */

var React = require('react');
var SignIn = require('./SignIn.react');
var Register = require('./Register.react');
var LoginStore = require('../stores/LoginStore');

var _getLoginState = function() {
  return LoginStore.getState();
};

var LoginView = React.createClass({

  getInitialState: function() {
    return _getLoginState();
  },
  
  componentDidMount: function() {
    LoginStore.addChangeListener(this._onChange);
  },

  componentWillUnmount: function() {
    LoginStore.removeChangeListener(this._onChange);
  },

  _onChange: function() {
    this.setState(_getLoginState());
  },

  render: function() {
    var isBusy = this.state.isBusy;
    var signInError = this.state.signInError;
    var registerError = this.state.registerError;
    
    return (
      <div>
        <h1 className="col-sm-offset-1 col-md-4">Welcome to SpotPost!</h1>
        <SignIn isBusy={isBusy} error={signInError} />
        <Register isBusy={isBusy} error={registerError} />
      </div>
    );
  }

});

module.exports = LoginView;

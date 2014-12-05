var EventEmitter = require('events').EventEmitter;
var merge = require('react/lib/merge');

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var Actions = require('../actions/Actions');
var SPOTPOST = require('../utils/SPOTPOST');
var xhr = require('../utils/xhr');

// local fields HERE
var _isBusy = false;
var _signInError = undefined;
var _registerError = undefined;

var LoginStore = merge(EventEmitter.prototype, {

  getState: function() {
    return {
      isBusy: _isBusy,
      signInError: _signInError,
      registerError: _registerError
    };
  },

  emitChange: function() {
    this.emit(Constants.CHANGE_EVENT);
  },

  addChangeListener: function(callback) {
    this.on(Constants.CHANGE_EVENT, callback);
  },

  removeChangeListener: function(callback) {
    this.removeListener(Constants.CHANGE_EVENT, callback);
  }
});

LoginStore.dispatchToken = AppDispatcher.register(function(payload) {
  var action = payload.action;

  switch(action.actionType) {
    case Constants.SUBMIT_SIGN_IN:
      var username = action.username;
      var password = action.password;
      
      // client side validity check
      var errorMessage = null;
      if (username === null || username.length < 1) {
        errorMessage = "No username entered";
      }
      else if (password === null || password.length < 1) {
        errorMessage = "No password entered";
      }
      
      if (errorMessage !== null) {
        _signInError = errorMessage;
      }
      else {
        _isBusy = true;
        var loginObject = {
          username: action.username,
          password: action.password
        };
        var request = xhr('POST', SPOTPOST.getLoginUrl(), JSON.stringify(loginObject));
        request.success(function(data) {
          if (data.code === "1000") {
            window.location.assign(SPOTPOST.getBase());
          }
          else {
            _signInError = data.message;
          }
          _isBusy = false;
          LoginStore.emitChange();
        });
        request.error(function(data) {
          _isBusy = false;
          LoginStore.emitChange();
        });
      }
      break;
      
    case Constants.SUBMIT_REGISTER:
      var username = action.username;
      var password = action.password;
      var password2 = action.password2;
      var email = action.email;
      
      // client side validity check
      var errorMessage = null;
      if (username === null || username.length < 1) {
        errorMessage = "No username entered";
      }
      else if (password !== password2) {
        errorMessage = "Passwords don't match";
      }
      else if (password === null || password.length < 1) {
        errorMessage = "No password entered";
      }
      else if (email === null || email.length < 1) {
        errorMessage = "No email entered";
      }
    
      if (errorMessage !== null) {
        _registerError = errorMessage;
      }
      else {
        _isBusy = true;
        var regObject = {
          username: username,
          password: password,
          email: email
        };
        var request = xhr('POST', SPOTPOST.getRegisterUrl(), JSON.stringify(regObject));
        request.success(function(data) {
          if (data.code === "1000") {
            window.location.assign(SPOTPOST.getBase());
          }
          else {
            _registerError = data.message;
          }
          _isBusy = false;
          LoginStore.emitChange();
        });
        request.error(function(data) {
          _isBusy = false;
          LoginStore.emitChange();
        });
      }
      break;
      
    case Constants.CLEAR_SIGN_IN_ERROR:
      _signInError = undefined;
      break;
      
    case Constants.CLEAR_REGISTER_ERROR:
      _registerError = undefined;
      break;
      
    default:
      return true;
  }

  LoginStore.emitChange();

  return true;
});

module.exports = LoginStore;

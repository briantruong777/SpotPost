var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

var Actions = {

  submitSignIn: function(username, password) {
    AppDispatcher.handleViewAction({
      actionType: Constants.SUBMIT_SIGN_IN,
      username: username,
      password: password
    });
  },
  
  submitRegister: function(username, password, password2, email) {
    AppDispatcher.handleViewAction({
      actionType: Constants.SUBMIT_REGISTER,
      username: username,
      password: password,
      password2: password2,
      email: email
    });
  },
  
  clearSignInError: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.CLEAR_SIGN_IN_ERROR
    });
  },
  
  clearRegisterError: function() {
    AppDispatcher.handleViewAction({
      actionType: Constants.CLEAR_REGISTER_ERROR
    });
  }

};

module.exports = Actions;

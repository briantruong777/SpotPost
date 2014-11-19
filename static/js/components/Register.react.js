/**
 * @jsx React.DOM
 */

var React = require('react');
var Actions = require('../actions/Actions');
var ErrorMessage = require('./ErrorMessage.react');

var ENTER_KEY = 13;

var Register = React.createClass({

  _clearError: function() {
    var error = this.props.error;
    if (error !== undefined && error !== null) {
      Actions.clearRegisterError();
    }
  },

  _onKeyDown: function(event) {
    this._clearError();
    if (event.keyCode === ENTER_KEY) {
      this._submit();
    }
  },
  
  _onClickSubmit: function(event) {
    event.preventDefault();
    this._submit();
  },
  
  _onClickClear: function(event) {
    event.preventDefault();
    this._clear();
  },
  
  _submit: function() {
    Actions.submitRegister(
      this.refs.username.state.value,
      this.refs.password.state.value,
      this.refs.password2.state.value,
      this.refs.email.state.value
    );
  },
  
  _clear: function() {
    this._clearError();
    this.refs.username.setState({
      value: null
    });
    this.refs.password.setState({
      value: null
    });
    this.refs.password2.setState({
      value: null
    });
    this.refs.email.setState({
      value: null
    });
  },

  render: function() {
    var isBusy = this.props.isBusy;
    var error = this.props.error;
    
    return (
      <div>
        <form className="form-horizontal">
          <div className="col-sm-offset-2 col-sm-10">
            <h2>Register</h2>
          </div>
          <div className="form-group">
            <label className="col-md-2 control-label" >Username: </label>
            <div className="col-md-2">
              <input className="col-md-2 form-control" ref="username" type="text" onKeyDown={this._onKeyDown} placeholder="username" disabled={isBusy} /><br/>
            </div>
          </div>
          <div className="form-group">
            <label className="col-md-2 control-label" >Password: </label>
            <div className="col-md-2">
              <input className="col-md-2 form-control" ref="password" type="password" onKeyDown={this._onKeyDown} placeholder="password" disabled={isBusy} /><br/>
            </div>
          </div>
          <div className="form-group">
            <label className="col-md-2 control-label" >Retype password: </label>
            <div className="col-md-2">
              <input className="col-md-2 form-control" ref="password2" type="password" onKeyDown={this._onKeyDown} placeholder="password" disabled={isBusy} /><br/>
            </div>
          </div>
          <div className="form-group">
            <label className="col-md-2 control-label" >Email address: </label>
            <div className="col-md-2">
              <input className="col-md-2 form-control"  ref="email" type="text" onKeyDown={this._onKeyDown} placeholder="email" disabled={isBusy} /><br/>
            </div>
          </div>
          <div className="form-group">
            <div className="col-sm-offset-2 col-sm-10">
              <button className="btn btn-primary" onClick={this._onClickSubmit} disabled={isBusy} >Register</button>
              <button className="btn btn-default" onClick={this._onClickClear} disabled={isBusy} >Clear</button>
            </div>
          </div>
          <div className="col-sm-offset-2 col-sm-10">
            <ErrorMessage error={error} />
          </div>
        </form>
      </div>
    );
  }

});

module.exports = Register;

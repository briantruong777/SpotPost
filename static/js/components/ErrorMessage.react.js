/**
 * @jsx React.DOM
 */

var React = require('react');

var ErrorMessage = React.createClass({

  render: function() {
    var error = this.props.error;
    
    if (error === undefined || error === null) {
      return (<div></div>);
    }
    
    return (
      <div>
        <span className="help-block">
          {error}
        </span>
      </div>
    );
  }

});

module.exports = ErrorMessage;

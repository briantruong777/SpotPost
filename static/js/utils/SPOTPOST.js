var BASE = 'http://spotpost.me/';
//var BASE = 'http://localhost:5000/';

var addParameters = function(url, parameters) {
  var first = true;
  for (var parameter in parameters) {
    if (first && parameters.hasOwnProperty(parameter)) {
      url += '?' + parameter + '=' + parameters[parameter];
      first = false;
    }
    else if (parameters.hasOwnProperty(parameter)) {
      url += '&' + parameter + '=' + parameters[parameter];
    }
  }

  return url;
};

function getGetUrl(parameters) {
  var url = BASE + '_get';
  return addParameters(url, parameters);
}

function getUpvoteUrl() {
  var url = BASE + '_upvote';
  return url;
}

function getDownvoteUrl() {
  var url = BASE + '_downvote';
  return url;
}

function getDeleteSpotPostUrl() {
  var url = BASE + '_delete';
  return url;
}

function getCreateSpotPostUrl() {
  var url = BASE + '_create';
  return url;
}

function getLoginUrl() {
  var url = BASE + 'login';
  return url;
}

function getRegisterUrl() {
  var url = BASE + '_register';
  return url;
}

module.exports = {
  getGetUrl: getGetUrl,
  getUpvoteUrl: getUpvoteUrl,
  getDownvoteUrl: getDownvoteUrl,
  getDeleteSpotPostUrl: getDeleteSpotPostUrl,
  getCreateSpotPostUrl: getCreateSpotPostUrl,
  getLoginUrl: getLoginUrl,
  getRegisterUrl: getRegisterUrl
};
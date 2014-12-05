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

function getSpotPostUpvoteUrl(id) {
  var url = BASE + 'spotpost/_upvote/' + id;
  return url;
}

function getSpotPostDownvoteUrl(id) {
  var url = BASE + 'spotpost/_downvote/' + id;
  return url;
}

function getSpotPostDeleteUrl(id) {
  var url = BASE + '_delete/' + id;
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

function getUserStatusUrl() {
  var url = BASE + '_userstatus';
  return url;
}

module.exports = {
  getGetUrl: getGetUrl,
  getSpotPostUpvoteUrl: getSpotPostUpvoteUrl,
  getSpotPostDownvoteUrl: getSpotPostDownvoteUrl,
  getSpotPostDeleteUrl: getSpotPostDeleteUrl,
  getCreateSpotPostUrl: getCreateSpotPostUrl,
  getLoginUrl: getLoginUrl,
  getRegisterUrl: getRegisterUrl,
  getUserStatusUrl: getUserStatusUrl
};
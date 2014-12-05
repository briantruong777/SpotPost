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

function getBase() {
  return BASE;
}

function getSpotPostGetUrl(parameters) {
  var url = BASE + 'spotpost/_get';
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

function getSpotPostUpdateUrl() {
  var url = BASE + 'spotpost/_update';
  return url;
}

function getSpotPostDeleteUrl(id) {
  var url = BASE + 'spotpost/_delete/' + id;
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

function getLogoutUrl() {
  var url = BASE + '_logout';
  return url;
}

function getCommentPostUrl() {
  var url = BASE + 'comment/_post';
  return url;
}

function getCommentUpvoteUrl(commentId) {
  var url = BASE + 'comment/_upvote/' + commentId;
  return url;
}

function getCommentDownvoteUrl(commentId) {
  var url = BASE + 'comment/_downvote/' + commentId;
  return url;
}

module.exports = {
  getBase: getBase,
  getSpotPostGetUrl: getSpotPostGetUrl,
  getSpotPostUpvoteUrl: getSpotPostUpvoteUrl,
  getSpotPostDownvoteUrl: getSpotPostDownvoteUrl,
  getSpotPostUpdateUrl: getSpotPostUpdateUrl,
  getSpotPostDeleteUrl: getSpotPostDeleteUrl,
  getCreateSpotPostUrl: getCreateSpotPostUrl,
  getLoginUrl: getLoginUrl,
  getLogoutUrl: getLogoutUrl,
  getRegisterUrl: getRegisterUrl,
  getUserStatusUrl: getUserStatusUrl,
  getCommentPostUrl: getCommentPostUrl,
  getCommentUpvoteUrl: getCommentUpvoteUrl,
  getCommentDownvoteUrl: getCommentDownvoteUrl
};
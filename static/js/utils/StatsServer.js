// not actual server, just the interface to it
var BASE = 'http://127.0.0.1:8000/';
var API = 'api/';
var TTT = 'tic-tac-toe/';

function getWinnerUrl() {
  return BASE + API + TTT + 'winner';
}

function getUpdateUrl() {
  return BASE + API + TTT + 'update';
}

module.exports = {
  getWinnerUrl: getWinnerUrl,
  getUpdateUrl: getUpdateUrl
};

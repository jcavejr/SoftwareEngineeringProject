var searchItems = [
  "physics",
  "computer networks",
  "operating systems",
  "spanish",
  "calculus"
];

var _timer = 0;
function wait() {
  if (_timer) window.clearTimeout(_timer);
  _timer = window.setTimeout(function() {
    search();
  }, 500);
}

function search() {
  var input;
  input = document.getElementById("search-container").value;

  var node = document.getElementById("search-results");
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }

  for (var i = 0; i < searchItems.length; i++) {
    if (searchItems[i].includes(input)) {
      var ul = document.getElementById("search-results");
      var li = document.createElement("li");
      li.innerHTML = searchItems[i];
      ul.appendChild(li);
      console.log(searchItems[i]);
    }
  }
}

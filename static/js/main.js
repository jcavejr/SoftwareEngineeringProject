var searchItems = [
  "Physics",
  "Computer networks",
  "Operating systems",
  "Spanish",
  "Calculus"
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
  input = document.getElementById("search-container").value.toLowerCase();

  var node = document.getElementById("search-results");
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }

  for (var i = 0; i < searchItems.length; i++) {
    if (
      searchItems[i].toLowerCase().includes(input) &&
      input != "" &&
      input != " "
    ) {
      var ul = document.getElementById("search-results");
      var a = document.createElement("a");
      var li = document.createElement("li");
      li.innerHTML = searchItems[i];
      a.setAttribute("href", "#");
      a.appendChild(li);
      ul.appendChild(a);
    }
  }
}

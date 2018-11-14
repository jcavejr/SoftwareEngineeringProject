var searchItems = [
  "Physics",
  "Computer networks",
  "Operating systems",
  "Spanish",
  "Calculus",
  "Databases",
  "Music",
  "Art"
];

var _timer = 0;
function wait() {
  if (_timer) window.clearTimeout(_timer);
  _timer = window.setTimeout(function() {
    search();
  }, 500);
}

function search() {
  var input,
    count = 0;
  input = document.getElementById("search-container").value.toLowerCase();

  var node = document.getElementById("search-results");
  while (node.firstChild) {
    node.removeChild(node.firstChild);
  }

  for (var i = 0; i < searchItems.length; i++) {
    if (
      searchItems[i].toLowerCase().includes(input) &&
      input != "" &&
      input != " " &&
      count < 5
    ) {
      var ul = document.getElementById("search-results");
      var a = document.createElement("a");
      var li = document.createElement("li");
      li.innerHTML = searchItems[i];
      a.setAttribute("onclick", "addClass(this.id)");
      a.setAttribute("href", "#");
      a.setAttribute("id", searchItems[i]);
      a.appendChild(li);
      ul.appendChild(a);
      count++;
    }
  }
}

function addClass(id) {
  var ul = document.getElementById("class-cells");
  var li = document.createElement("li");
  li.innerHTML = id;
  ul.appendChild(li);
}

//var searchItems = [
//  "Physics",
//  "Computer networks",
//  "Operating systems",
//  "Spanish",
//  "Calculus",
//  "Databases",
//  "Music",
//  "Art"
//];

var searchItems = list_of_classes

var added = [];

var _timer = 0;
function wait() {
  if (_timer) window.clearTimeout(_timer);
  _timer = window.setTimeout(function() {
    search();
  }, 500);
}

function getAdded(){
    return added
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
      count < 5 &&
      added.includes(searchItems[i]) != true
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
  li.setAttribute("onmouseover", "mouseOver(this.id)");
  li.setAttribute("onmouseout", "mouseOut(this.id)");
  li.setAttribute("id", id);
  li.innerHTML = id;
  added.push(id);
  ul.appendChild(li);

  closeList = document.getElementById("search-results");
  while (closeList.firstChild) {
    closeList.removeChild(closeList.firstChild);
  }
}

var orig;

function mouseOver(id) {
  var li = document.getElementById(id);
  li.style.backgroundColor = "#cc0033";
  li.style.color = "black";
  orig = li.innerHTML;
  li.innerHTML = "X";
  li.style.paddingLeft = "20px";
  li.style.paddingRight = "20px";
  li.setAttribute("onclick", "removeItem(this.id)");
}

function mouseOut(id) {
  var li = document.getElementById(id);
  li.style.backgroundColor = "black";
  li.style.color = "#cc0033";
  li.innerHTML = orig;
  li.style.paddingLeft = "10px";
  li.style.paddingRight = "10px";
}

function removeItem(id) {
  var li = document.getElementById(id);
  li.remove();
  for (var i = 0; i < added.length; i++) {
    if (added[i] == id) {
      added.splice(i);
    }
  }
}

function addOverlay(id) {
  const ids = ["question", "post-expanded", "post-overlay", "new-class"];
  ids.forEach((i) => {
    if(i == id){
      document.getElementById(i).style.display = "block"; 
    }
  })
  document.getElementById("overlay").style.display = "block";
}

function removeOverlay() {
  const ids = ["question", "post-expanded", "post-overlay", "new-class"];
  ids.forEach((i) => {
    document.getElementById(i).style.display = "none";
    })
  document.getElementById("overlay").style.display = "none";
}

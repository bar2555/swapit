function ajax_request(event) {
  // create AJAX object
  var req = new XMLHttpRequest();
  // callback function to pre-fill item div once page is loaded
  req.onreadystatechange = function() {
    if (req.readyState == 4 && req.status == 200) {
      // update the item using the response to the ajax request
      $('#item').html(req.responseText);
      }
    };
  req.open("GET", 'nextitem', true);
  req.send();
  };

let form = document.getElementById("form-container");
let formButton = document.getElementById("show-form-button");

formButton.addEventListener("click", function() {
    
    if (form.style.display === "none") {
      form.style.display = "block";
    } else {
      form.style.display = "none";
    }
  });

let buttons = document.querySelectorAll(".show-game-button");

buttons.forEach(button => {
  button.addEventListener("click", function(event) {
    event.preventDefault();
    let gameInfo = this.nextElementSibling;
    if (gameInfo.style.display === "none") {
      gameInfo.style.display = "block";
    } else {
      gameInfo.style.display = "none";
    }
  });
});

var deleteForm = document.getElementById("delete-form");
var deleteButton = document.getElementById("delete-button");

deleteButton.addEventListener("click", function(event) {
  if (!confirm("Are you sure you want to delete this game?")) {
    event.preventDefault();
  }
});

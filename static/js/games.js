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

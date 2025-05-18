const searchInput = document.getElementById("search-input");
const searchCards = document.querySelectorAll(".search_card"); // select all book cards

searchInput.addEventListener("input", () => {
  const keyword = searchInput.value.trim().toLowerCase();

  searchCards.forEach((card) => {
    const titleElement = card.querySelector(".search__title"); // get the h2 inside the card
    const bookTitle = titleElement.textContent.trim().toLowerCase(); // get the title text

    if (keyword === "" || bookTitle.includes(keyword)) {
      card.style.display = "";
    } else {
      card.style.display = "none";   // Hide the card
    }
  });
});

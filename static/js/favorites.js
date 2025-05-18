// document.addEventListener('DOMContentLoaded', () => {
//     const favoritesContainer = document.getElementById('favorites-container');
//     const backButton = document.getElementById('back-button');

//     // Retrieve favorites from local storage
//     const favorites = JSON.parse(localStorage.getItem('favorites')) || [];

//     // Check if favorites is empty
//     if (favorites.length === 0) {
//         favoritesContainer.innerHTML = '<p>You have no favorite books yet.</p>';
//         return;
//     }

//     // Display each favorite card
//     favorites.forEach((item) => {
//         const card = document.createElement('article');
//         card.classList.add('featured__card');

//         card.innerHTML = `
//             <img src="${item.image}" alt="image" class="featured__img">
//             <h2 class="featured__title">${item.title}</h2>
//             <div class="featured__prices">
//                 <span class="featured__discount">${item.discount}</span>
//                 <span class="featured__price">${item.price}</span>
//             </div>
//             <button class="button remove-favorite-button">Remove from Favorites</button>
//         `;

//         // Add the card to the container
//         favoritesContainer.appendChild(card);

//         // Add event listener to the remove button
//         const removeButton = card.querySelector('.remove-favorite-button');
//         removeButton.addEventListener('click', () => {
//             removeFromFavorites(item.title);
//             card.remove(); // Remove the card from the DOM
//         });
//     });

//     // Function to remove a card from favorites
//     function removeFromFavorites(title) {
//         const favorites = JSON.parse(localStorage.getItem('favorites')) || [];

//         // Remove the card from the favorites array
//         const updatedFavorites = favorites.filter((item) => item.title !== title);

//         // Save the updated favorites array to local storage
//         localStorage.setItem('favorites', JSON.stringify(updatedFavorites));
//     }

//     // Handle back button click
//     backButton.addEventListener('click', () => {
//         window.history.back();
//     });
// }); 
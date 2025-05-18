// // Cart functionality
// document.addEventListener('DOMContentLoaded', function () {
//     // Add to cart buttons
//     const addToCartButtons = document.querySelectorAll('.book-details__add-cart, .favorites__add-cart');
//     addToCartButtons.forEach(button => {
//         button.addEventListener('click', function () {
//             const bookId = this.dataset.bookId;
//             addToCart(bookId);
//         });
//     });

//     // Remove from cart buttons
//     const removeFromCartButtons = document.querySelectorAll('.cart__remove');
//     removeFromCartButtons.forEach(button => {
//         button.addEventListener('click', function () {
//             const bookId = this.dataset.bookId;
//             removeFromCart(bookId);
//         });
//     });

//     // Quantity buttons
//     const quantityButtons = document.querySelectorAll('.cart__quantity-btn');
//     quantityButtons.forEach(button => {
//         button.addEventListener('click', function () {
//             const input = this.parentElement.querySelector('.cart__quantity-input');
//             const bookId = this.closest('.cart__card').querySelector('.cart__remove').dataset.bookId;
//             const currentValue = parseInt(input.value);

//             if (this.classList.contains('minus') && currentValue > 1) {
//                 input.value = currentValue - 1;
//                 updateCartQuantity(bookId, currentValue - 1);
//             } else if (this.classList.contains('plus')) {
//                 input.value = currentValue + 1;
//                 updateCartQuantity(bookId, currentValue + 1);
//             }
//         });
//     });

//     // Favorite buttons
//     const favoriteButtons = document.querySelectorAll('.book-details__favorite, .favorites__remove');
//     favoriteButtons.forEach(button => {
//         button.addEventListener('click', function () {
//             const bookId = this.dataset.bookId;
//             toggleFavorite(bookId, this);
//         });
//     });
// });

// // Add to cart function
// function addToCart(bookId) {
//     fetch('/add-to-cart/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//             book_id: bookId
//         })
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 showNotification('Book added to cart successfully!');
//             } else {
//                 showNotification(data.error || 'Failed to add book to cart.', 'error');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             showNotification('An error occurred while adding to cart.', 'error');
//         });
// }

// // Remove from cart function
// function removeFromCart(bookId) {
//     fetch('/remove-from-cart/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//             book_id: bookId
//         })
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 const cartItem = document.querySelector(`.cart__card [data-book-id="${bookId}"]`).closest('.cart__card');
//                 cartItem.remove();
//                 updateCartTotal();
//                 showNotification('Book removed from cart successfully!');
//             } else {
//                 showNotification(data.error || 'Failed to remove book from cart.', 'error');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             showNotification('An error occurred while removing from cart.', 'error');
//         });
// }

// // Update cart quantity function
// function updateCartQuantity(bookId, quantity) {
//     fetch('/update-cart-quantity/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//             book_id: bookId,
//             quantity: quantity
//         })
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 updateCartTotal();
//             } else {
//                 showNotification(data.error || 'Failed to update cart quantity.', 'error');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             showNotification('An error occurred while updating cart quantity.', 'error');
//         });
// }

// // Toggle favorite function
// function toggleFavorite(bookId, button) {
//     fetch('/toggle-favorite/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//             book_id: bookId
//         })
//     })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 if (button.classList.contains('book-details__favorite')) {
//                     button.classList.toggle('active');
//                     const icon = button.querySelector('i');
//                     icon.classList.toggle('ri-heart-line');
//                     icon.classList.toggle('ri-heart-fill');
//                 } else {
//                     const favoriteCard = button.closest('.favorites__card');
//                     favoriteCard.remove();
//                     if (document.querySelectorAll('.favorites__card').length === 0) {
//                         location.reload();
//                     }
//                 }
//                 showNotification(data.message);
//             } else {
//                 showNotification(data.error || 'Failed to update favorites.', 'error');
//             }
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             showNotification('An error occurred while updating favorites.', 'error');
//         });
// }

// // Update cart total function
// function updateCartTotal() {
//     const cartItems = document.querySelectorAll('.cart__card');
//     let total = 0;

//     cartItems.forEach(item => {
//         const price = parseFloat(item.querySelector('.cart__discount, .cart__price').textContent.replace('$', ''));
//         const quantity = parseInt(item.querySelector('.cart__quantity-input').value);
//         total += price * quantity;
//     });

//     document.querySelector('.cart__total span:last-child').textContent = `$${total.toFixed(2)}`;
// }

// // Show notification function
// function showNotification(message, type = 'success') {
//     const notification = document.createElement('div');
//     notification.className = `notification ${type}`;
//     notification.textContent = message;

//     document.body.appendChild(notification);

//     setTimeout(() => {
//         notification.remove();
//     }, 3000);
// }

// // Get CSRF token function
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// } 
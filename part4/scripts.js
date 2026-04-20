const API_BASE = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  updateAuthLinks(token);

  const page = document.body.dataset.page;

  if (page === 'login') {
    initLoginPage();
  }

  if (page === 'index') {
    checkAuthenticationIndex();
  }

  if (page === 'place') {
    initPlacePage();
  }

  if (page === 'add-review') {
    initAddReviewPage();
  }
});

function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(';') : [];
  for (const cookie of cookies) {
    const trimmed = cookie.trim();
    if (trimmed.startsWith(`${name}=`)) {
      return decodeURIComponent(trimmed.substring(name.length + 1));
    }
  }
  return null;
}

function setTokenCookie(token) {
  document.cookie = `token=${encodeURIComponent(token)}; path=/`;
}

function updateAuthLinks(token) {
  const isAuthenticated = Boolean(token);
  const loginButton = document.getElementById('login-link');
  const navLoginLinks = document.querySelectorAll('[data-auth-link="true"]');

  if (loginButton) {
    loginButton.style.display = isAuthenticated ? 'none' : 'inline-block';
  }

  navLoginLinks.forEach((link) => {
    link.style.display = isAuthenticated ? 'none' : 'inline';
  });
}

function getPlaceIdFromURL() {
  return new URLSearchParams(window.location.search).get('id');
}

async function parseResponse(response) {
  const text = await response.text();
  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text);
  } catch (error) {
    return { error: text };
  }
}

async function apiRequest(path, options = {}) {
  const { method = 'GET', token = null, body = null } = options;
  const headers = {};

  if (body !== null) {
    headers['Content-Type'] = 'application/json';
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body !== null ? JSON.stringify(body) : undefined,
  });

  const data = await parseResponse(response);
  return { response, data };
}

function escapeHTML(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function renderEmptyState(container, text) {
  container.innerHTML = `<p class="empty-state">${escapeHTML(text)}</p>`;
}

function initLoginPage() {
  const loginForm = document.getElementById('login-form');
  const loginError = document.getElementById('login-error');

  if (!loginForm || !loginError) {
    return;
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    loginError.textContent = '';

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
      await loginUser(email, password);
      window.location.href = 'index.html';
    } catch (error) {
      loginError.textContent = error.message;
    }
  });
}

async function loginUser(email, password) {
  const { response, data } = await apiRequest('/auth/login', {
    method: 'POST',
    body: { email, password },
  });

  if (!response.ok || !data.access_token) {
    throw new Error(data.error || 'Invalid credentials');
  }

  setTokenCookie(data.access_token);
}

function checkAuthenticationIndex() {
  const token = getCookie('token');
  updateAuthLinks(token);
  attachPriceFilterHandler();
  fetchPlaces(token);
}

function attachPriceFilterHandler() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter || priceFilter.dataset.bound === 'true') {
    return;
  }

  priceFilter.addEventListener('change', applyPriceFilter);
  priceFilter.dataset.bound = 'true';
}

async function fetchPlaces(token) {
  const { response, data } = await apiRequest('/places/', { token });
  const placesList = document.getElementById('places-list');

  if (!placesList) {
    return;
  }

  if (!response.ok) {
    renderEmptyState(placesList, data.error || 'Failed to load places.');
    return;
  }

  const places = Array.isArray(data) ? data : [];
  const placesWithPrices = await Promise.all(
    places.map(async (place) => {
      if (getPlacePrice(place) > 0) {
        return place;
      }

      const detailedPlace = await fetchPlaceSummary(place.id, token);
      return detailedPlace ? { ...place, ...detailedPlace } : place;
    })
  );

  displayPlaces(placesWithPrices);
}

async function fetchPlaceSummary(placeId, token) {
  const { response, data } = await apiRequest(`/places/${placeId}`, { token });
  if (!response.ok) {
    return null;
  }
  return data;
}

function getPlacePrice(place) {
  const candidates = [
    place.price,
    place.price_per_night,
    place.pricePerNight,
  ];

  for (const candidate of candidates) {
    const normalized = Number(candidate);
    if (Number.isFinite(normalized)) {
      return normalized;
    }
  }

  return 0;
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');

  if (!placesList) {
    return;
  }

  placesList.innerHTML = '';

  if (places.length === 0) {
    renderEmptyState(placesList, 'No places available.');
    return;
  }

  places.forEach((place) => {
    const card = document.createElement('article');
    card.className = 'place-card';

    const placeName = place.title || place.name || 'Unnamed Place';
    const placePrice = getPlacePrice(place);
    card.dataset.price = String(placePrice);

    const title = document.createElement('h3');
    title.textContent = placeName;

    const price = document.createElement('p');
    price.textContent = `Price per night: $${placePrice}`;

    const detailsButton = document.createElement('a');
    detailsButton.className = 'details-button';
    detailsButton.href = `place.html?id=${encodeURIComponent(place.id)}`;
    detailsButton.textContent = 'View Details';

    card.append(title, price, detailsButton);
    placesList.appendChild(card);
  });

  applyPriceFilter();
}

function applyPriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  const cards = document.querySelectorAll('.place-card');

  if (!priceFilter) {
    return;
  }

  const selected = priceFilter.value;

  cards.forEach((card) => {
    const cardPrice = Number(card.dataset.price || 0);
    const isVisible = selected === 'All' || cardPrice <= Number(selected);
    card.style.display = isVisible ? 'flex' : 'none';
  });
}

async function initPlacePage() {
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();

  updateAuthLinks(token);

  if (!placeId) {
    showPlaceLoadError('Invalid place id.');
    return;
  }

  checkAuthenticationPlace(token);
  await fetchPlaceDetails(token, placeId);

  const reviewForm = document.getElementById('review-form');
  if (token && reviewForm && reviewForm.dataset.bound !== 'true') {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const reviewText = document.getElementById('review-text').value.trim();
      const rating = Number(document.getElementById('review-rating').value);

      try {
        await submitReview(token, placeId, reviewText, rating);
        alert('Review submitted successfully!');
        reviewForm.reset();
        await fetchPlaceDetails(token, placeId);
      } catch (error) {
        alert(error.message || 'Failed to submit review');
      }
    });

    reviewForm.dataset.bound = 'true';
  }
}

function checkAuthenticationPlace(token) {
  const addReviewSection = document.getElementById('add-review');
  if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';
  }
}

async function fetchPlaceDetails(token, placeId) {
  const { response, data } = await apiRequest(`/places/${placeId}`, { token });

  if (!response.ok) {
    showPlaceLoadError(data.error || 'Failed to load place details.');
    return;
  }

  const reviews = await fetchPlaceReviews(token, placeId);
  const enrichedReviews = await enrichReviewsWithUsers(reviews, token);
  displayPlaceDetails(data, enrichedReviews);
}

async function fetchPlaceReviews(token, placeId) {
  const { response, data } = await apiRequest(`/places/${placeId}/reviews`, { token });
  if (!response.ok || !Array.isArray(data)) {
    return [];
  }
  return data;
}

async function enrichReviewsWithUsers(reviews, token) {
  return Promise.all(
    reviews.map(async (review) => {
      let reviewerName = 'Anonymous';

      if (review.user && (review.user.first_name || review.user.last_name)) {
        reviewerName = `${review.user.first_name || ''} ${review.user.last_name || ''}`.trim();
      } else if (review.user_name) {
        reviewerName = review.user_name;
      } else if (review.user_id) {
        reviewerName = await fetchUserName(review.user_id, token);
      }

      return {
        ...review,
        reviewerName,
      };
    })
  );
}

async function fetchUserName(userId, token) {
  const { response, data } = await apiRequest(`/users/${userId}`, { token });
  if (!response.ok) {
    return userId;
  }

  const fullName = `${data.first_name || ''} ${data.last_name || ''}`.trim();
  return fullName || userId;
}

function displayPlaceDetails(place, reviews) {
  const placeDetails = document.getElementById('place-details');
  if (!placeDetails) {
    return;
  }

  const ownerFirstName = place.owner?.first_name || '';
  const ownerLastName = place.owner?.last_name || '';
  const ownerName = `${ownerFirstName} ${ownerLastName}`.trim() || 'Unknown Host';
  const placePrice = getPlacePrice(place);
  const amenities = Array.isArray(place.amenities)
    ? place.amenities.map((amenity) => amenity.name).join(', ')
    : '';

  placeDetails.innerHTML = '';

  const title = document.createElement('h2');
  title.textContent = place.title || 'Place Details';

  const info = document.createElement('div');
  info.className = 'place-info';
  info.innerHTML = `
    <p><strong>Host:</strong> ${escapeHTML(ownerName)}</p>
    <p><strong>Price per night:</strong> $${escapeHTML(placePrice)}</p>
    <p><strong>Description:</strong> ${escapeHTML(place.description || 'No description available.')}</p>
    <p><strong>Amenities:</strong> ${escapeHTML(amenities || 'No amenities listed.')}</p>
  `;

  placeDetails.append(title, info);
  renderReviews(reviews);
}

function renderReviews(reviews) {
  const reviewsList = document.getElementById('reviews-list');

  if (!reviewsList) {
    return;
  }

  reviewsList.innerHTML = '';

  if (!Array.isArray(reviews) || reviews.length === 0) {
    renderEmptyState(reviewsList, 'No reviews yet.');
    return;
  }

  reviews.forEach((review) => {
    const reviewCard = document.createElement('article');
    reviewCard.className = 'review-card';

    const text = document.createElement('p');
    text.textContent = `"${review.text || ''}"`;

    const meta = document.createElement('p');
    meta.textContent = `— ${review.reviewerName || 'Anonymous'}, Rating: ${review.rating}/5`;

    reviewCard.append(text, meta);
    reviewsList.appendChild(reviewCard);
  });
}

function showPlaceLoadError(message) {
  const placeDetails = document.getElementById('place-details');
  if (placeDetails) {
    placeDetails.innerHTML = `<p class="empty-state">${escapeHTML(message)}</p>`;
  }

  const reviewsList = document.getElementById('reviews-list');
  if (reviewsList) {
    reviewsList.innerHTML = '';
  }
}

async function initAddReviewPage() {
  const token = checkAuthenticationForAddReview();
  if (!token) {
    return;
  }

  const placeId = getPlaceIdFromURL();
  if (!placeId) {
    alert('Invalid place selected.');
    window.location.href = 'index.html';
    return;
  }

  await setAddReviewTitle(token, placeId);

  const reviewForm = document.getElementById('review-form');
  if (!reviewForm || reviewForm.dataset.bound === 'true') {
    return;
  }

  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const reviewText = document.getElementById('review-text').value.trim();
    const rating = Number(document.getElementById('review-rating').value);

    try {
      await submitReview(token, placeId, reviewText, rating);
      alert('Review submitted successfully!');
      reviewForm.reset();
    } catch (error) {
      alert(error.message || 'Failed to submit review');
    }
  });

  reviewForm.dataset.bound = 'true';
}

function checkAuthenticationForAddReview() {
  const token = getCookie('token');
  updateAuthLinks(token);

  if (!token) {
    window.location.href = 'index.html';
    return null;
  }

  return token;
}

async function setAddReviewTitle(token, placeId) {
  const title = document.getElementById('add-review-title');
  if (!title) {
    return;
  }

  const { response, data } = await apiRequest(`/places/${placeId}`, { token });
  if (response.ok && data.title) {
    title.textContent = `Reviewing: ${data.title}`;
  }
}

async function submitReview(token, placeId, reviewText, rating) {
  const { response, data } = await apiRequest('/reviews/', {
    method: 'POST',
    token,
    body: {
      text: reviewText,
      rating,
      place_id: placeId,
    },
  });

  if (!response.ok) {
    throw new Error(data.error || 'Failed to submit review');
  }

  return data;
}

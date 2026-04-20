const API_BASE = 'http://127.0.0.1:5000/api/v1';
let sessionExpiredOnLoad = false;

document.addEventListener('DOMContentLoaded', () => {
  const token = getValidToken();
  updateAuthLinks(token);
  initLogoutControls();

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

function clearTokenCookie() {
  document.cookie = 'token=; path=/; Max-Age=0';
}

function decodeTokenPayload(token) {
  const segments = token.split('.');
  if (segments.length !== 3) {
    return null;
  }

  try {
    const normalized = segments[1].replace(/-/g, '+').replace(/_/g, '/');
    const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, '=');
    return JSON.parse(atob(padded));
  } catch (error) {
    return null;
  }
}

function isTokenExpired(token) {
  const payload = decodeTokenPayload(token);
  if (!payload || typeof payload.exp !== 'number') {
    return true;
  }

  const now = Math.floor(Date.now() / 1000);
  return payload.exp <= now;
}

function getValidToken() {
  const token = getCookie('token');
  if (!token) {
    return null;
  }

  if (isTokenExpired(token)) {
    clearTokenCookie();
    sessionExpiredOnLoad = true;
    return null;
  }

  return token;
}

function updateAuthLinks(token) {
  const isAuthenticated = Boolean(token);
  const loginButton = document.getElementById('login-link');
  const navLoginLinks = document.querySelectorAll('[data-auth-link="true"]');
  const logoutButtons = document.querySelectorAll('[data-logout-link="true"]');

  if (loginButton) {
    loginButton.style.display = isAuthenticated ? 'none' : 'inline-block';
  }

  navLoginLinks.forEach((link) => {
    link.style.display = isAuthenticated ? 'none' : 'inline';
  });

  logoutButtons.forEach((button) => {
    button.style.display = isAuthenticated ? 'inline-block' : 'none';
  });
}

function initLogoutControls() {
  const logoutButtons = document.querySelectorAll('[data-logout-link="true"]');

  logoutButtons.forEach((button) => {
    if (button.dataset.bound === 'true') {
      return;
    }

    button.addEventListener('click', () => {
      clearTokenCookie();
      window.location.href = 'login.html?logged_out=1';
    });

    button.dataset.bound = 'true';
  });
}

function getPlaceIdFromURL() {
  return new URLSearchParams(window.location.search).get('id');
}

function getCurrentPageWithQuery() {
  const pageName = window.location.pathname.split('/').pop() || 'index.html';
  return `${pageName}${window.location.search}`;
}

function buildLoginURL(reason, nextPath = '') {
  const params = new URLSearchParams();

  if (reason) {
    params.set('reason', reason);
  }

  if (nextPath) {
    params.set('next', nextPath);
  }

  const query = params.toString();
  return query ? `login.html?${query}` : 'login.html';
}

function getPostLoginDestination() {
  const nextPath = new URLSearchParams(window.location.search).get('next');

  if (!nextPath) {
    return 'index.html';
  }

  if (nextPath.startsWith('http://') || nextPath.startsWith('https://') || nextPath.startsWith('//')) {
    return 'index.html';
  }

  if (/^[a-zA-Z][a-zA-Z\d+.-]*:/.test(nextPath)) {
    return 'index.html';
  }

  return nextPath.startsWith('/') ? nextPath.slice(1) : nextPath;
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

  if (token && isTokenExpired(token)) {
    clearTokenCookie();
    sessionExpiredOnLoad = true;
    return {
      response: { ok: false, status: 401 },
      data: { error: 'Your session expired. Please log in again.' },
    };
  }

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

  if (response.status === 401 && token) {
    clearTokenCookie();
    sessionExpiredOnLoad = true;
    updateAuthLinks(null);
  }

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

  const params = new URLSearchParams(window.location.search);
  const reason = params.get('reason');

  if (params.get('logged_out') === '1') {
    loginError.textContent = 'You have been logged out.';
  } else if (reason === 'session_expired' || sessionExpiredOnLoad) {
    loginError.textContent = 'Your session expired. Please log in again.';
  } else if (reason === 'auth_required') {
    loginError.textContent = 'Please log in to continue.';
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    loginError.textContent = '';

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
      await loginUser(email, password);
      window.location.href = getPostLoginDestination();
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
  const token = getValidToken();
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
    if (response.status === 401 && token) {
      updateAuthLinks(null);
      await fetchPlaces(null);
      return;
    }

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
  const token = getValidToken();
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
        const result = await submitReview(token, placeId, reviewText, rating);
        if (!result) {
          return;
        }

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
    if (response.status === 401 && token) {
      updateAuthLinks(null);
      checkAuthenticationPlace(null);
      await fetchPlaceDetails(null, placeId);
      return;
    }

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
      const result = await submitReview(token, placeId, reviewText, rating);
      if (!result) {
        return;
      }

      alert('Review submitted successfully!');
      reviewForm.reset();
    } catch (error) {
      alert(error.message || 'Failed to submit review');
    }
  });

  reviewForm.dataset.bound = 'true';
}

function checkAuthenticationForAddReview() {
  const token = getValidToken();
  updateAuthLinks(token);

  if (!token) {
    const reason = sessionExpiredOnLoad ? 'session_expired' : 'auth_required';
    window.location.href = buildLoginURL(reason, getCurrentPageWithQuery());
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
    if (response.status === 401) {
      window.location.href = buildLoginURL('session_expired', getCurrentPageWithQuery());
      return null;
    }

    throw new Error(data.error || 'Failed to submit review');
  }

  return data;
}

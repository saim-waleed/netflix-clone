// Navbar scroll effect
document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.querySelector(".navbar");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });
});

// Chatbot functionality
const chatbotWindow = document.getElementById("chatbot-window");
const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");

function toggleChatbot() {
  chatbotWindow.style.display =
    chatbotWindow.style.display === "none" ? "block" : "none";
  if (chatbotWindow.style.display === "block") {
    chatInput.focus();
  }
}

function addMessage(message, isUser = false) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `chat-message ${
    isUser ? "user-message" : "bot-message"
  }`;
  messageDiv.textContent = message;
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener("submit", async function (e) {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

  // Add user message
  addMessage(message, true);
  chatInput.value = "";

  try {
    // Send message to backend
    const response = await fetch("/chatbot/message/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    // Add bot response
    addMessage(data.response);
  } catch (error) {
    console.error("Error:", error);
    addMessage("Sorry, I encountered an error. Please try again later.");
  }
});

// Movie hover effect
document.addEventListener("DOMContentLoaded", function () {
  const movieCards = document.querySelectorAll(".movie-card");

  movieCards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      const video = this.querySelector("video");
      if (video) {
        video.play();
      }
    });

    card.addEventListener("mouseleave", function () {
      const video = this.querySelector("video");
      if (video) {
        video.pause();
        video.currentTime = 0;
      }
    });
  });
});

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


// Search functionality
const searchForm = document.querySelector(".search-form");
if (searchForm) {
  searchForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const searchInput = this.querySelector('input[type="search"]');
    if (searchInput.value.trim()) {
      window.location.href = `/search/?q=${encodeURIComponent(
        searchInput.value.trim()
      )}`;
    }
  });
}

// Infinite scroll for movie lists
let isLoading = false;
let page = 1;

window.addEventListener("scroll", function () {
  if (
    window.innerHeight + window.scrollY >=
    document.body.offsetHeight - 1000
  ) {
    loadMoreContent();
  }
});

async function loadMoreContent() {
  if (isLoading) return;

  const movieContainer = document.querySelector(".movie-container");
  if (!movieContainer) return;

  isLoading = true;

  try {
    const response = await fetch(`/api/movies/?page=${page + 1}`);
    const data = await response.json();

    if (data.movies.length > 0) {
      data.movies.forEach((movie) => {
        const movieCard = createMovieCard(movie);
        movieContainer.appendChild(movieCard);
      });
      page++;
    }
  } catch (error) {
    console.error("Error loading more content:", error);
  } finally {
    isLoading = false;
  }
}

function createMovieCard(movie) {
  const card = document.createElement("div");
  card.className = "movie-card";
  card.innerHTML = `
        <img src="${movie.thumbnail}" alt="${movie.title}">
        <div class="movie-info">
            <h5>${movie.title}</h5>
            <p>${movie.description}</p>
            <button class="btn btn-netflix" onclick="playMovie('${movie.id}')">
                <i class="fas fa-play me-2"></i>Play
            </button>
        </div>
    `;
  return card;
}

// Play movie function
function playMovie(movieId) {
  window.location.href = `/watch/${movieId}`;
}

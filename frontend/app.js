let accessToken = '';  // Store the JWT token

// Register a new user
async function register() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const name = document.getElementById('name').value;

    const response = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
    });

    const data = await response.json();
    if (response.status === 201) {
        alert('User registered successfully!');
    } else {
        alert(data.msg);
    }
}

// Login an existing user
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (response.status === 200) {
        accessToken = data.access_token;  // Store JWT token
        alert('Login successful!');
        document.getElementById('post-form').style.display = 'block';
        fetchPosts();  // Fetch posts after login
    } else {
        alert(data.msg);
    }
}

// Create a new post
async function createPost() {
    const caption = document.getElementById('caption').value;
    const image = document.getElementById('image-url').value;

    const response = await fetch('http://127.0.0.1:5000/posts', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ caption, image }),
    });

    const data = await response.json();
    if (response.status === 201) {
        alert('Post created successfully!');
        fetchPosts();  // Refresh posts
    } else {
        alert(data.msg);
    }
}

// Add a comment to a post
async function addComment() {
    const postId = document.querySelector('.post.selected').dataset.id;
    const text = document.getElementById('comment-text').value;

    const response = await fetch(`http://127.0.0.1:5000/posts/${postId}/comments`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
    });

    const data = await response.json();
    if (response.status === 201) {
        alert('Comment added successfully!');
        fetchPosts();  // Refresh posts
    } else {
        alert(data.msg);
    }
}

// Fetch and display all posts
async function fetchPosts() {
    const response = await fetch('http://127.0.0.1:5000/posts', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
        },
    });

    const posts = await response.json();
    const postsDiv = document.getElementById('posts');
    postsDiv.innerHTML = '';  // Clear existing posts

    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.classList.add('post');
        postDiv.dataset.id = post.id;

        let commentsHtml = '';
        post.comments.forEach(comment => {
            commentsHtml += `<div class="comment">${comment.text}</div>`;
        });

        postDiv.innerHTML = `
            <h3>Post #${post.id}</h3>
            <p><strong>Caption:</strong> ${post.caption}</p>
            <img src="${post.image}" alt="Post image" width="100">
            <div><strong>Comments:</strong></div>
            ${commentsHtml}
            <button onclick="selectPost(${post.id})">Add Comment</button>
        `;
        postsDiv.appendChild(postDiv);
    });
}

// Select post to add comment
function selectPost(postId) {
    const selectedPost = document.querySelector('.post.selected');
    if (selectedPost) {
        selectedPost.classList.remove('selected');
    }

    const post = document.querySelector(`.post[data-id="${postId}"]`);
    post.classList.add('selected');
    document.getElementById('comment-form').style.display = 'block';
}

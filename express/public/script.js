// Load all products
fetch('/products')
    .then(res => res.json())
    .then(products => {
        const list = document.getElementById('product-list');
        list.innerHTML = '';
        products.forEach(product => {
            const li = document.createElement('li');
            li.textContent = product.name || `Product ${product.id}`;
            li.style.cursor = 'pointer';
            li.onclick = () => showProduct(product.id);
            list.appendChild(li);
        });
    });

function showProduct(id) {
    fetch(`/products/${id}`)
        .then(res => {
            if (!res.ok) throw new Error("Not found");
            return res.json();
        })
        .then(product => {
            document.getElementById('product-details').style.display = 'block';
            document.getElementById('product-info').textContent = JSON.stringify(product, null, 2);
        })
        .catch(err => alert("Product not found"));
}

// Register user
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());

    const res = await fetch('/users', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    });

    if (res.ok) {
        alert('User registered');
    } else {
        alert('Failed to register');
    }
});

// Login
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const data = Object.fromEntries(form.entries());

    const res = await fetch('/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
        credentials: 'include'
    });

    if (res.ok) {
        const user = await res.json();
        alert('Login successful');
        fetchUserInfo(user.id);
    } else {
        alert('Login failed');
    }
});

function fetchUserInfo(userId) {
    fetch(`/users/${userId}`, {
        credentials: 'include'
    })
        .then(res => {
            if (!res.ok) throw new Error("Unauthorized");
            return res.json();
        })
        .then(user => {
            document.getElementById('user-info').style.display = 'block';
            document.getElementById('user-data').textContent = JSON.stringify(user, null, 2);
        })
        .catch(err => {
            alert("Failed to fetch user data");
        });
}

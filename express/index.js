const express = require('express');
const app = express();
const port = 3000;

const {productStore, addUser, getUser} = require('./store');

app.get('/products', (req, res) => {
    res.json(Object.values(productStore));
});

app.get('/products/:id', (req, res) => {
    const product = productStore[req.params.id];
    if (product) {
        res.json(product);
    } else {
        res.status(404).send('Product not found');
    }
});

app.post('/login', express.json(), (req, res) => {
    const { id, password } = req.body;
    const user = login(id, password);
    if (user) {
        const sessionId = generateSession(id);
        res.cookie('sessionId', sessionId, { httpOnly: true });
        res.json(user);
    } else {
        res.status(401).send('Invalid credentials');
    }
});

const sessionMiddleware = (req, res, next) => {
    const sessionId = req.cookies?.sessionId;
    if (sessionId) {
        const user = Object.values(userStore).find(u => u.sessionId === sessionId);
        if (user) {
            req.session.userId = user.id;
            req.session.user = getUser(user.id);
        }
    }
    next();
}

app.get('/users/:id', sessionMiddleware, (req, res) => {
    if (!req?.session?.userId) {
        return res.status(401).send('Unauthorized');
    }
    if (req?.session?.userId !== req.params.id) {
        return res.status(403).send('Forbidden');
    }

    const user = getUser(req.params.id);
    if (user) {
        res.json(user);
    } else {
        res.status(404).send('User not found');
    }
});

app.post('/users', express.json(), (req, res) => {
    const newUser = addUser(req.body);
    res.status(201).json(newUser);
});

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});
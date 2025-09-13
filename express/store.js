const { generateRandomString } = require('./utils');

const productStore = {
    "1": { id: "1", name: "Product 1", price: 100 },
    "2": { id: "2", name: "Product 2", price: 200 },
    "3": { id: "3", name: "Product 3", price: 300 },
};

let userStore = {
    "1": { id: "1", name: "User 1", age: 30, "password": "password1" },
    "2": { id: "2", name: "User 2", age: 25, "password": "password2" },
    "3": { id: "3", name: "User 3", age: 35, "password": "password3" },
};

const getUser = (id) => {
    const { password, ...userWithoutPassword } = userStore[id];
    return userWithoutPassword;
}

const addUser = (user) => {
    const id = String(Object.keys(userStore).length + 1);
    userStore[id] = { id, ...user };
    return getUser(id);
}

const updateUser = (id, user) => {
    if (userStore[id]) {
        userStore[id] = { ...userStore[id], ...user };
        return getUser(id);
    }
    return null;
}

const login = (id, password) => {
    const user = userStore[id];
    if (user && user.password === password) {
        return getUser(id);
    }
    return null;
}

const generateSession = (id) => {
    const sessionId = generateRandomString(16);
    updateUser(id, { sessionId });
    return sessionId
}

module.exports = { productStore, getUser, addUser, login, generateSession };

const port = 3000;
const socketio = require('socket.io');
const socketOptions = {
    cors: {
        origin: 'http://localhost:5500',
        credentials: true
    }
};

const io = socketio(port, socketOptions);

const users = {};

io.on('connection', socket => {
    socket.on('new-user', name => {
        users[socket.id] = name;
        socket.broadcast.emit('user-connected', name);
    });

    socket.on('send-chat-message', message => {
        socket.broadcast.emit('chat-message', {
            message: message,
            name: users[socket.id]
        });
    });

    socket.on('disconnect', () => {
        socket.broadcast.emit('user-disconnected', users[socket.id]);
        delete users[socket.id];
    });
})
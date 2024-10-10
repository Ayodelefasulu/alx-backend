import redis from 'redis';

// Create a Redis client
const subscriber = redis.createClient();

// Event handler for successful connection
subscriber.on('connect', () => {
    console.log('Redis client connected to the server');
});

// Event handler for connection error
subscriber.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the channel
subscriber.subscribe('holberton school channel');

// Listen for messages on the subscribed channel
subscriber.on('message', (channel, message) => {
    console.log(message);

    // Unsubscribe and quit if the message is KILL_SERVER
    if (message === 'KILL_SERVER') {
        subscriber.unsubscribe();
        subscriber.quit();
    }
});

import redis from 'redis';

// Create a Redis client
const publisher = redis.createClient();

// Event handler for successful connection
publisher.on('connect', () => {
    console.log('Redis client connected to the server');
});

// Event handler for connection error
publisher.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

// Define constants for delay times
const DELAY_1 = 100,
    DELAY_2 = 200,
    DELAY_3 = 300,
    DELAY_4 = 400,

    // Function to publish messages after a specified delay
    publishMessage = (message, time) => {
        setTimeout(() => {
            console.log(`About to send ${message}`);
            publisher.publish('holberton school channel', message);
        }, time);
    };

// Call publishMessage with different arguments
publishMessage('Holberton Student #1 starts course', DELAY_1);
publishMessage('Holberton Student #2 starts course', DELAY_2);
publishMessage('KILL_SERVER', DELAY_3);
publishMessage('Holberton Student #3 starts course', DELAY_4);

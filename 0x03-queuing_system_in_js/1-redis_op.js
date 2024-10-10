import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

// Event handler for successful connection
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

// Event handler for connection error
client.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
});

// Function to display the value of a school from Redis
const displaySchoolValue = (schoolName) => {
        client.get(schoolName, (err, reply) => {
            if (err) {
                console.log(`Error getting ${schoolName}: ${err.message}`);
            } else {
                console.log(reply);
            }
        });
    },

    // Function to set a new school value in Redis
    setNewSchool = (schoolName, value) => {
        client.set(schoolName, value, redis.print);
    };

// Calling the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

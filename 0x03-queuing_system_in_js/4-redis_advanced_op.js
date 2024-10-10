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

// Function to create a hash
const createHash = () => {
        const schoolData = {
            'Portland': 50,
            'Seattle': 80,
            'New York': 20,
            'Bogota': 20,
            'Cali': 40,
            'Paris': 2
        };

        // Use hset to store the hash values
        Object.entries(schoolData).forEach(([
            key,
            value
        ]) => {
            client.hset('HolbertonSchools', key, value, redis.print);
        });
    },

    // Function to display the hash
    displayHash = () => {
        client.hgetall('HolbertonSchools', (err, reply) => {
            if (err) {
                console.log(`Error getting hash: ${err.message}`);
            } else {
                console.log(reply);
            }
        });
    };

// Create the hash and display it
createHash();
displayHash();

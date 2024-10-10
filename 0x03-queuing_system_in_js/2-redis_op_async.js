import {promisify} from 'util';
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

const getAsync = promisify(client.get).bind(client),

    // Function to display the value of a school from Redis using async/await
    displaySchoolValue = async (schoolName) => {
        try {
            const reply = await getAsync(schoolName);

            if (reply) {
                console.log(reply);
            } else {
                console.log(`No value found for ${schoolName}`);
            }
        } catch (err) {
            console.log(`Error getting ${schoolName}: ${err.message}`);
        }
    },

    // Function to set a new school value in Redis
    setNewSchool = (schoolName, value) => {
        client.set(schoolName, value, redis.print);
    };

// Calling the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

import express from 'express';
import kue from 'kue';
import redis from 'redis';
import {promisify} from 'util';

const app = express(),
    PORT = 1245,

    // Initialize Redis client
    client = redis.createClient();

client.on('error', (err) => {
    console.error(`Redis error: ${err}`);
});

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client),
    setAsync = promisify(client.set).bind(client),

    // Initialize Kue queue
    queue = kue.createQueue(),

    // Initialize available seats and reservation status
    initialAvailableSeats = 50;
let reservationEnabled = true;

// Set initial available seats in Redis
setAsync('available_seats', initialAvailableSeats);

/**
 * Reserve a seat in Redis.
 * @param {number} number - The number of available seats to set.
 */
async function reserveSeat (number) {
    await setAsync('available_seats', number);
}

/**
 * Get the current number of available seats from Redis.
 * @returns {Promise<number>} - The number of available seats.
 */
async function getCurrentAvailableSeats () {
    const availableSeats = await getAsync('available_seats');


    return availableSeats ? parseInt(availableSeats, 10) : 0;
}

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();

    res.json({'numberOfAvailableSeats': availableSeats.toString()});
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({'status': 'Reservations are blocked'});
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({'status': 'Reservation failed'});
        }

        return res.json({'status': 'Reservation in process'});
    });
});

// Process queue
app.get('/process', async (req, res) => {
    res.json({'status': 'Queue processing'});

    queue.process('reserve_seat', async (job, done) => {
        const currentAvailableSeats = await getCurrentAvailableSeats(),
            newAvailableSeats = currentAvailableSeats - 1;

        if (newAvailableSeats < 0) {
            done(new Error('Not enough seats available'));

            return;
        }

        await reserveSeat(newAvailableSeats);

        if (newAvailableSeats === 0) {
            reservationEnabled = false;
        }

        console.log(`Seat reservation job ${job.id} completed`);
        done();
    });

    // Handle job failure
    queue.on('job failed', (job, err) => {
        console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
    });
});

// Start the Express server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});


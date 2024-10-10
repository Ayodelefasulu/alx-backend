import kue from 'kue';

// Create a queue named push_notification_code
const queue = kue.createQueue();

// Function to send a notification
const sendNotification = (phoneNumber, message) => {
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
};

// Process new jobs in the push_notification_code queue
queue.process('push_notification_code', (job, done) => {
    const { phoneNumber, message } = job.data;

    // Call the sendNotification function with job data
    sendNotification(phoneNumber, message);

    // Mark the job as complete
    done();
});

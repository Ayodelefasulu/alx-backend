import kue from 'kue';

// Create a queue named push_notification_code
const queue = kue.createQueue(),

    // Create a job data object with keys sorted in ascending order
    jobData = {
        'message': 'This is a test notification message',
        'phoneNumber': '1234567890'
    },

    // Create a job with the job data
    job = queue.create('push_notification_code', jobData).save((err) => {
        if (err) {
            console.error(`Error creating job: ${err}`);
        } else {
            console.log(`Notification job created: ${job.id}`);
        }
    });

// Listen for job completion
job.on('complete', () => {
    console.log('Notification job completed');
});

// Listen for job failure
job.on('failed', (errorMessage) => {
    console.log(`Notification job failed: ${errorMessage}`);
});

/*
 * Optional: Listen for job progress (if needed)
 * job.on('progress', (progress) => {
 *     console.log(`Notification job ${job.id} is ${progress}% complete`);
 * });
 */

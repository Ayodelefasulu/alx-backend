import kue from 'kue';

// Create a queue to process jobs from the push_notification_code_2 queue
const queue = kue.createQueue({
  concurrency: 2, // Process two jobs at a time
});

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Constants for job progress tracking
const INITIAL_PROGRESS = 0;
const HALF_PROGRESS = 50;
const FULL_PROGRESS = 100;

// Function to send notifications
const sendNotification = (phoneNumber, message, job, done) => {
  // Track the progress of the job
  job.progress(INITIAL_PROGRESS, FULL_PROGRESS);

  // Check if the phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    const errorMessage = `Phone number ${phoneNumber} is blacklisted`;
    done(new Error(errorMessage)); // Fail the job
    return; // Exit the function
  }

  // Track the progress to 50%
  job.progress(HALF_PROGRESS);

  // Log the notification being sent
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

  // Call done to indicate that the job is completed successfully
  done();
};

// Process jobs from the push_notification_code_2 queue
queue.process('push_notification_code_2', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message, job, done);
});

// Listen for job events
queue.on('job failed', (job, err) => {
  console.log(`Notification job ${job.id} failed: ${err.message}`);
});

queue.on('job complete', (job) => {
  console.log(`Notification job ${job.id} completed`);
});

queue.on('job progress', (job, progress) => {
  console.log(`Notification job ${job.id} ${progress}% complete`);
});

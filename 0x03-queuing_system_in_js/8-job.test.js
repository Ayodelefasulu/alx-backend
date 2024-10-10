import chai from 'chai';
import createPushNotificationsJobs from './8-job.js';
import kue from 'kue';
import sinon from 'sinon';

const {expect} = chai,

    // Create a queue with Kue
    queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
    beforeEach(() => {
    // Enter test mode before executing tests
        queue.testMode.enter();
    });

    afterEach(() => {
    // Clear the queue and exit test mode after executing tests
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('should display an error message if jobs is not an array', () => {
        expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
    });

    it('should create two new jobs in the queue', () => {
        const jobs = [
            {
                'phoneNumber': '4153518780',
                'message': 'This is the code 1234 to verify your account'
            },
            {
                'phoneNumber': '4153518743',
                'message': 'This is the code 5678 to verify your account'
            }
        ];

        createPushNotificationsJobs(jobs, queue);

        // Validate which jobs are inside the queue
        const jobIds = queue.testMode.jobs.map((job) => job.id);

        expect(jobIds).to.have.lengthOf(2);
    });

    it('should log job creation messages', () => {
        const jobs = [
                {
                    phoneNumber: '4153518780',
                    message: 'This is the code 1234 to verify your account'
                }
            ],

            consoleSpy = sinon.spy(console, 'log');

        createPushNotificationsJobs(jobs, queue);

        // Check if the job creation log was made
        expect(consoleSpy.calledWithMatch(/Notification job created: \d+/)).to.be.true;
        consoleSpy.restore();
    });
});

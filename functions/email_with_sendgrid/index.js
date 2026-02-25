const { PubSub } = require('@google-cloud/pubsub');
const sgMail = require('@sendgrid/mail');

const pubsub = new PubSub();

// Set up SendGrid
sgMail.setApiKey('SENDGRID_APIKEY');

// Define the subscription name and topic name
const subscriptionName = 'projects/temp-416704/subscriptions/new-product-sub';

// Get a reference to the subscription
const subscription = pubsub.subscription(subscriptionName);
console.log(`Subscribed to topic ${subscriptionName}`);

// Email sending function
exports.sendEmail = async (data) => {
  const { event_type, created_type, event_context } = data;
  console.log(event_context)
  const { to, subject, text } = event_context;

  const msg = {
    to,
    from: "cat8@sfu.ca",
    subject,
    text,
  };

  await sgMail
    .send(msg)
    .then((response) => console.log(response))
    .catch((error) =>console.error('Failed to send email:', error));
}

// Subscribe to the topic
subscription.on('message', async (message) => {
  // Handle the message here
  console.log(`Received message: ${message.id}`);
  console.log(`Data: ${message.data}`);
  
  // Parse the message data
  const data = JSON.parse(message.data.toString());
  
  // Call your email sending function
  await exports.sendEmail(data);
  
  // Acknowledge the message
  message.ack();
});
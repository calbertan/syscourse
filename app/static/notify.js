const projectId = 'temp-416704';
const topicName = 'send-email';
const url = `https://pubsub.googleapis.com/v1/projects/${projectId}/topics/${topicName}:publish`;

const pubsub = new google.pubsub.v1.PublisherClient();

function publishMessage() {
  const topicName = 'send-email';
  const formattedTopic = pubsub.topicPath(projectId, topicName);

  const data = {
    to: '02c.albert@gmail.com',
    subject: 'Test Email',
    text: 'This is a test email.'
  };

  const message = Buffer.from(JSON.stringify(data)).toString('base64');

  const request = {
    topic: formattedTopic,
    messages: [{ data: message }]
  };

  pubsub.publish(request)
    .then(() => console.log('Message published to Pub/Sub'))
    .catch(err => console.error('Failed to publish message:', err));
}

document.getElementById('bell').addEventListener('click', publishMessage);

importScripts('https://www.gstatic.com/firebasejs/8.7.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.7.1/firebase-messaging.js');

firebase.initializeApp({
    apiKey: "AIzaSyBvihU6T4SowXC95lEAdd_gIzAtoIhzOhQ",
    authDomain: "espazum.firebaseapp.com",
    databaseURL: "https://espazum.firebaseio.com",
    projectId: "espazum",
    storageBucket: "espazum.appspot.com",
    messagingSenderId: "1009225536861",
    appId: "1:1009225536861:web:05d7089e8163933a4bc4b4",
    measurementId: "G-MJ080XNJ8F"
});

const messaging = firebase.messaging();

onBackgroundMessage(messaging);

function onBackgroundMessage(messaging) {
  
    // [START messaging_on_background_message]
    messaging.onBackgroundMessage((payload) => {
      console.log('[firebase-messaging-sw.js] Received background message ', payload);
      // Customize notification here

      const notificationPayload = payload.notification

      const notificationTitle = notificationPayload.title
      const notificationOptions = {
        body: notificationPayload.body,
        icon: '/static/images/logo/Ezpazum.png'
      };
    
      self.registration.showNotification(notificationTitle,
        notificationOptions);
    });
    // [END messaging_on_background_message]
}
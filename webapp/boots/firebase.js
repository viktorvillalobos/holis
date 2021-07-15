import firebase from "firebase/app";
import 'firebase/firebase-messaging'

// Agregar configuración firebase:
const firebaseConfig = {
    apiKey: "AIzaSyBvihU6T4SowXC95lEAdd_gIzAtoIhzOhQ",
    authDomain: "espazum.firebaseapp.com",
    databaseURL: "https://espazum.firebaseio.com",
    projectId: "espazum",
    storageBucket: "espazum.appspot.com",
    messagingSenderId: "1009225536861",
    appId: "1:1009225536861:web:05d7089e8163933a4bc4b4",
    measurementId: "G-MJ080XNJ8F"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);
//const messaging = firebase.messaging();
/*messaging.getToken({ vapidKey: '<YOUR_PUBLIC_VAPID_KEY_HERE>' }).then((currentToken) => {
    if (currentToken) {
      // Send the token to your server and update the UI if necessary
      // ...
    } else {
      // Show permission request UI
      console.log('No registration token available. Request permission to generate one.');
      // ...
    }
  }).catch((err) => {
    console.log('An error occurred while retrieving token. ', err);
    // ...
  });
//let db = firebase.firestore(); */
export { firebase };

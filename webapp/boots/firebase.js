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

firebase.initializeApp(firebaseConfig);
export default firebase.messaging()

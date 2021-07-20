importScripts('https://www.gstatic.com/firebasejs/8.2.7/firebase-app.js')
importScripts('https://www.gstatic.com/firebasejs/8.2.7/firebase-messaging.js')

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

const app = firebase.initializeApp(firebaseConfig)
// Copyright 2018 Google LLC.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Script for configuring Firebase Authentication (Sign In/Out with Google).
// See https://firebase.google.com/docs/auth/web/google-signin for more information.

import { app } from "./initFirebase.js";
import { getAuth, signInWithRedirect, getRedirectResult, GoogleAuthProvider, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// Initialize Firebase
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

function signInWithGoogle() {
  signInWithRedirect(auth, provider);
}

function signOutWithGoogle() {
  signOut(auth).then(() => {
    document.cookie = "firebase_id_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    window.location.replace('/');
  }).catch((error) => {
    console.log(error);
  });
}

getRedirectResult(auth).then((result) => {
  if (result && result.user) {
    document.getElementById("message_body").innerText = "You have successfully signed in. Now redirecting you back to the site.";
    result.user.getIdToken(true).then((firebaseIdToken) => {
      document.cookie = `firebase_id_token=${firebaseIdToken};path=/;`;
      setTimeout(() => { window.location.replace("/"); }, 1500);
    });
  } else {
    document.getElementById("message_body").innerText = "Now redirecting you to Google."
    setTimeout(function () { signInWithGoogle(); }, 1500);
  }
}).catch((error) => {
  console.log(error);
});

// Optionally expose signInWithGoogle and signOutWithGoogle for use in the global scope, 
// e.g., in onclick attributes in HTML.
window.signInWithGoogle = signInWithGoogle;
window.signOutWithGoogle = signOutWithGoogle;
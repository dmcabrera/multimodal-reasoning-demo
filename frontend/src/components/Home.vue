<template>
    <div id="home_div" class="container-fluid">
        <!-- Navigation bar -->
        <nav class="navbar navbar-light bg-light">
            <a class="navbar-brand" href="#">
                <img src="./../assets/google_logo.png" width="35" height="35" class="d-inline-block align-top" alt="">
                {{ t("multimodal_reasoning.title") }}
            </a>
            <!--
            <div v-if="logeado" class="align-right" id="logout">
                {{ usuario }}
                <button v-if="logeado" type="button" class="btn btn-dark align-right" @click="logout">{{
                    t("home.logout")
                    }}</button>
            </div>
            -->
        </nav>

        <!-- Welcome and login -->
        <p></p>
        <h4 v-if="!logeado">{{ t("home.welcome") }}</h4>
        <button v-if="!logeado" type="button" class="btn btn-primary" @click="login">{{ t("home.login") }}</button>

        <div v-if="logeado" class="row justify-content-md-center">

            <div class="container">
                <div class="row">
                    <div class="col-xs-12 col-md-6">
                        <video id="video" controls autoplay playsinline style="height: 100%;width: 100%;"></video>
                    </div>
                    <div class="col-xs-12 col-md-6">
                        <h2>{{ respuesta_modelo }}</h2>
                    </div>
                </div>
                <div v-if="!streaming" class="row pt-2">
                    <div class="col">
                        <div class="dropdown">
                            <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton1"
                                data-bs-toggle="dropdown" aria-expanded="false">
                                {{ selectedVideoDevice }}
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1" role="menu">
                                <li v-for="camera in videoDevicesNames" :key="camera">
                                    <a class="dropdown-item" @click="cameraChanged" href="javascript:void(0)">{{ camera
                                        }}</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <audio v-if="streaming && isIOS()" id="answer_sound" src="" autoPlay muted></audio>
                <div class="row pt-4">
                    <div class="col">
                        <button class="btn btn-primary" id="btn-start-streaming" @click="startStopStreaming">{{
                            streaming_button_label }}</button>
                    </div>
                    <div class="col">
                        <button v-if="streaming" :class="record_button_class" id="btn-start-stop-recording"
                            @click="startStopRecording">{{
                                recording_button_label }}</button>
                    </div>
                    <div class="col">
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
// Imports
import { ref, reactive, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { getAuth, signInWithPopup, signInWithEmailAndPassword, GoogleAuthProvider, signOut } from "firebase/auth";
import { initializeApp } from "firebase/app";

// Create Firebase config
const firebaseConfig = {
    apiKey: "AIzaSyB-EcsQ6PeetnYzQpgjuJ1moAT7v-oZ92I",
    authDomain: "cecl-genai-demos.firebaseapp.com",
    databaseURL: "https://cecl-genai-demos-default-rtdb.firebaseio.com",
    projectId: "cecl-genai-demos",
    storageBucket: "cecl-genai-demos.appspot.com",
    messagingSenderId: "401653266392",
    appId: "1:401653266392:web:57f88df25ceefa843fe4ad",
    measurementId: "G-R79N39PJVD"
};

// Initialize Firebase
// 401653266392-jsk8fhjvoa0s2um5bl54flngb867p5a7.apps.googleusercontent.com
const firebase_app = initializeApp(firebaseConfig);

// View state
const logeado = ref(true);
const usuario = ref('');
const id_token = ref('');
const { t } = useI18n()
const streaming = ref(false);
const recording = ref(false);
const streaming_button_label = ref(t("multimodal_reasoning.start_streaming_button_label"));
const recording_button_label = ref(t("multimodal_reasoning.start_recording_button_label"));
const respuesta_modelo = ref('')
const record_button_class = ref('btn btn-success');
var video_stream;
var recorder;
var recorded_video;
var videoDevices = new Map();
var videoDevicesNames = [];
const selectedVideoDevice = ref('');


// View initialization event
onMounted(() => {
    window.addEventListener("load", () => loadCameras());
})

// Login
async function login() {
    const auth = getAuth(firebase_app);
    signInWithEmailAndPassword(auth, "demos@demosgenai.com", "!demosgenai")
        .then(async (result) => {
            auth.currentUser.getIdToken(true).then(function (idToken) {
                id_token.value = idToken;
                usuario.value = "Demo User"
                logeado.value = true;
                console.log('Login successful');
            }).catch(function (error) {
                console.log("Error al obtener el id token: " + error)
            });
        }).catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            const email = error.customData.email;
            const credential = GoogleAuthProvider.credentialFromError(error);
        });
}

// Logout
function logout() {
    const auth = getAuth();
    signOut(auth).then(() => {
        logeado.value = false;
        usuario.value = t("home.not_connected_user");
        console.log('Logout successful');

    }).catch((error) => {
        console.log('Logout error');
    });
}

// Detecto si estoy en iOS
function isIOS() {
    return /iPad|iPhone|iPod/.test(navigator.userAgent);
}

// Cargo las cámaras disponibles
async function loadCameras() {
    if (isIOS()) {
        videoDevicesNames.push("Front Camera");
        videoDevices.set("Front Camera", "user");
        videoDevicesNames.push("Back Camera");
        videoDevices.set("Back Camera", "environment");
    } else {
        const devices = await navigator.mediaDevices.enumerateDevices();
        console.log(devices);
        devices.forEach(device => {
            if (device.kind === "videoinput") {
                videoDevices.set(device.label, device.deviceId);
                videoDevicesNames.push(device.label);
            }
        });
    }
    selectedVideoDevice.value = videoDevicesNames[0];
}

// Actualizo la camera seleccionada
function cameraChanged(event) {
    selectedVideoDevice.value = event.target.innerText;
}

// Inicia o detiene el streaming
async function startStopStreaming() {
    if (streaming.value) {
        stopStreaming();
        streaming_button_label.value = t("multimodal_reasoning.start_streaming_button_label");
    } else {
        startStreaming();
        streaming_button_label.value = t("multimodal_reasoning.stop_streaming_button_label");
    }
}

// Detiene el streaming
async function stopStreaming() {
    // Inicializo el video
    var video = document.getElementById('video')
    video.muted = true;
    video.volume = 0;
    video.srcObject = null;

    // Cambio el flag
    video_stream = null;
    streaming.value = false;
    respuesta_modelo.value = '';
}

// Inicio el streaming
async function startStreaming() {

    // Obtengo el stream
    console.log("Obteniendo stream de video...");
    var selected_camera = selectedVideoDevice.value;
    var video_constraints = {}
    if (isIOS()) {
        video_constraints = {
            audio: true,
            video: {
                //width: 640/*320-640-1280*/,
                facingMode: videoDevices.get(selected_camera)
            }
        }
    } else {
        video_constraints = {
            audio: true,
            video: {
                deviceId: videoDevices.get(selected_camera)
            }
        };
    }
    try {
        var stream = await navigator.mediaDevices.getUserMedia(video_constraints)
        console.log("Stream de video obtenido.");

        // Inicializo el video
        var video = document.getElementById('video')
        video.muted = true;
        video.volume = 0;
        if (isIOS()) {
            video.setAttribute('autoplay', '');
            video.setAttribute('muted', '');
            video.setAttribute('playsinline', '');
        }
        video.srcObject = stream;

        // Cambio el flag
        video_stream = stream;
        streaming.value = true;
        console.log("Streaming iniciado.");
    } catch (error) {
        console.log("Error al obtener el stream de video: " + error);
        alert("Error al obtener el stream de video: " + error);
    }
}

// Inicio o detengo la grabacion
function startStopRecording() {
    if (recording.value) {
        stopRecording();
        recording.value = false;
        recording_button_label.value = t("multimodal_reasoning.start_recording_button_label");
        record_button_class.value = 'btn btn-success';
    }
    else {
        startRecording();
        recording.value = true;
        recording_button_label.value = t("multimodal_reasoning.stop_recording_button_label");
        record_button_class.value = 'btn btn-danger';
    }
}

// Función que inicia el recording.
async function startRecording() {
    try {
        respuesta_modelo.value = '';
        recorder = RecordRTC(video_stream, {
            type: 'video',
            mimeType: 'video/webm'
        });
        recorder.startRecording();
        recorder.camera = video_stream;
    } catch (error) {
        console.log("Error al iniciar el recording: " + error);
        alert("Error al iniciar el recording: " + error);
    }
}

// Callback que se invoca al detener el recording
function stopRecordingCallback() {
    try {
        // Detengo el recorder
        recorded_video = recorder.getBlob();
        recorder.camera.stop();
        recorder.destroy();
        recorder = null;

        // Inicio el streaming nuevamente
        startStreaming();

        // LLamo al servicio de razonamiento
        reason();
    } catch (error) {
        console.log("Error al detener el recording: " + error);
        alert("Error al detener el recording: " + error);
    }
}

// Función que finaliza el recording
function stopRecording() {
    recorder.stopRecording(stopRecordingCallback);
}

// Transformo el video grabado a base64
async function toBase64(blob) {
    var buf = await blob.arrayBuffer();
    var bytes = new Uint8Array(buf);
    var bin = [...bytes].reduce((acc, byte) => acc += String.fromCharCode(byte), '');
    var b64 = btoa(bin);
    return b64;
}

// Invoco al servicio que razona
async function reason() {
    try {
        // Armo el request
        var video_data = await toBase64(recorded_video)
        const request =
        {
            "video_data": video_data
        };

        // Invoco el servicio
        const API_ENDPOINT = import.meta.env.VITE_API_ENDPOINT;
        const response = await fetch(`${API_ENDPOINT}/reason`, {
            method: 'POST',
            body: JSON.stringify(request),
            headers: {
                'Authorization': 'Bearer ' + id_token.value,
                'content-type': 'application/json'
            }
        });

        // Obtengo la respuesta.
        var data = '';
        if (isIOS()) {
            data = await response.text();
            data = JSON.parse(data);
        } else {
            data = await response.json();
        }
        respuesta_modelo.value = data.response_text

        // Reproduzco el audio
        try {
            if (isIOS()) {
                //var audio = new Audio();
                //audio.autoplay = true;
                //audio.volume = 1;
                //audio.src = 'data:audio/mp3;base64,' + data.response_audio;
                //audio.play();
                var audio = document.getElementById('answer_sound');
                audio.autoplay = true;
                audio.src = 'data:audio/mp3;base64,' + data.response_audio;
                audio.muted = false;
                audio.play();
            } else {
                var audio = new Audio("data:audio/mp3;base64," + data.response_audio);
                audio.play();
            }

        } catch (error) {
            console.log("Error al reproducir el audio: " + error);
            alert("Error al reproducir el audio: " + error);
        }

    } catch (error) {
        console.log("Error al razonar: " + error);
        alert("Error al razonar: " + error);
    }
}

</script>

<style></style>

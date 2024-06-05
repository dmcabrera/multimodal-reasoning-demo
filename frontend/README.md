# frontend

This is a simple Vue 3 app that records the video using the webrtc library and the sends the video to the backend. After the backends process the video, it generates a response with the text response from the model and also the audio response generated in the backend using the TTS API. After receiving the audio in base64, the frontend reproduces the audio to generate the cool effect of the model speaking.

## Recommended IDE Setup


## Customize configuration


## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

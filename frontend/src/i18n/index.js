import { createI18n } from "vue-i18n";

const messages = {
  es: {
    home: {
      welcome: "Bienvenido a la demo Gemini Multimodal Reasoning",
      login: "Ingresar",
      logout: "Logout",
      not_connected_user: "Usuario no conectado"
    },
    multimodal_reasoning: {
      title: "Gemini Multimodal Reasoning Demo",
      start_streaming_button_label: "▶️ Streaming",
      stop_streaming_button_label: "⏺️ Streaming",
      start_recording_button_label: "⏺️ Grabar",
      stop_recording_button_label: "⏹️ Detener"
    }
  },
  pt: {
    home: {
      welcome: "Bem-vindo à demo Gemini Multimodal Reasoning",
      login: "Entrar",
      logout: "Logout",
      not_connected_user: "Usuário não logado"
    },
    multimodal_reasoning: {
      title: "Gemini Multimodal Reasoning Demo",
      start_streaming_button_label: "▶️ Transmissão",
      stop_streaming_button_label: "⏺️ Transmitir",
      start_recording_button_label: "⏺️ Gravar",
      stop_recording_button_label: "⏺️ Pare"
    }
  },
  en: {
    home: {
      welcome: "Welcome to Gemini Multimodal Reasoning",
      login: "Login",
      logout: "Logout",
      not_connected_user: "Not connected user"
    },
    multimodal_reasoning: {
      title: "Gemini Multimodal Reasoning Demo",
      start_streaming_button_label: "▶️ Streaming",
      stop_streaming_button_label: "⏺️ Streaming",
      start_recording_button_label: "⏺️ Record",
      stop_recording_button_label: "⏺️ Stop"
    }
  }
}

function getLang() {
  let language = 'en';
  if (navigator.languages != undefined) {
    language = navigator.languages[0].substring(0, 2);
  } 
  console.log('The default language is: ' + language)
  return language;
}

export default createI18n({
  locale: getLang(), //import.meta.env.VITE_DEFAULT_LOCALE,
  fallbackLocale: import.meta.env.VITE_FALLBACK_LOCALE,
  legacy: false,
  messages
})
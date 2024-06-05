# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Imports
import os
import random
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

from google.cloud import texttospeech
from google.cloud import storage
from google.cloud import translate_v2 as translate
from google.cloud import pubsub_v1

# Constantes
PROJECT_ID = "cecl-genai-demos"
LOCATION = "us-central1"
TOPIC_ID = "delete_video_topic"
GENERATION_CONFIG = {
    "max_output_tokens": 8192,
    "temperature": 0.3,
    "top_p": 0.95,
}

SAFETY_SETTINGS = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
}

SUPPORTED_LANGUAGES = {
    "es": {
        "language_code": "es-US",
        "name": "es-US-Neural2-A",
    },
    "en": {
        "language_code": "en-US",
        "name": "en-US-Neural2-G",
    },
    "pt": {
        "language_code": "pt-BR",
        "name": "pt-BR-Neural2-C",
    },
    "fr": {
        "language_code": "fr-FR",
        "name": "fr-FR-Neural2-E",
    },
    "de": {
        "language_code": "de-DE",
        "name": "de-DE-Neural2-A",
    },
    "hi": {
        "language_code": "hi-IN",
        "name": "hi-IN-Neural2-A",
    },
    "ja": {
        "language_code": "ja-JP",
        "name": "ja-JP-Neural2-B",
    },
    "it": {
        "language_code": "it-IT",
        "name": "it-IT-Neural2-A",
    }
}

# Sube un archivo a gcs
def upload_file_to_cs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0
    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)
    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

# Tool que implementa el razonamiento multimodal
class MultimodalReasoningTool(object):

    # Constructor
    def __init__(self):
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        self.model = GenerativeModel(
            "gemini-1.5-flash-preview-0514",
        )

        # Instancio el cliente tts
        self.tts_client = texttospeech.TextToSpeechClient()

        # Instancio el cliente translate
        self.translate_client = translate.Client()

        # Instancio el cliente pubsub
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(PROJECT_ID, TOPIC_ID)


    # Funcion que razona generando un request multimodal y
    # llamando al modelo
    def reason(self, video_data):

        # Salvo el video como un archivo y lo subo a gcs
        VIDEO_FILE = "video" + str(random.randrange(100, 1000000)) + ".mkv"
        with open(VIDEO_FILE, "wb") as out:
            out.write(video_data)
        #delete_file_from_cs("cecl-genai-demos-vertex2", "videos/" + VIDEO_FILE)
        upload_file_to_cs(
            "cecl-genai-demos-vertex2",
            VIDEO_FILE,
            "videos/" + VIDEO_FILE)

        # Genero el request multimodal
        video = Part.from_uri(
            "gs://cecl-genai-demos-vertex2/videos/" + VIDEO_FILE,
            mime_type="video/x-matroska")
        #video = Part.from_data(
        #    mime_type="video/x-matroska",
        #    data=bytes(video_data))

        # Invoco al modelo
        responses = self.model.generate_content(
            [video, "Answer the question indicated in the video in the same language and in less than 50 words"],
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
            stream=False,
        )

        # Elimino el archivo y envio el mensaje
        # al topico
        os.remove(VIDEO_FILE)
        self.publisher.publish(self.topic_path, VIDEO_FILE.encode("utf-8"))

        # Retorno la respuesta
        response_text = responses.candidates[0].text
        return response_text

    # Detecto el idioma del texto
    def detect_language(self, text: str) -> dict:
        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = self.translate_client.detect_language(text)

        print(f"Text: {text}")
        print("Confidence: {}".format(result["confidence"]))
        print("Language: {}".format(result["language"]))

        return result["language"]

    # Hago el tts
    def talk(self, response_text):
        # Seteo el texto a sintetizar
        synthesis_input = texttospeech.SynthesisInput(text=response_text)

        # Detecto el idioma del texto
        language_code = self.detect_language(response_text)

        # Genero el request
        detecteded_language = SUPPORTED_LANGUAGES["en"]
        if language_code in SUPPORTED_LANGUAGES:
            detecteded_language = SUPPORTED_LANGUAGES[language_code]
        voice = texttospeech.VoiceSelectionParams(
            language_code=detecteded_language["language_code"],
            name=detecteded_language["name"]
        )

        # Seleccion el tipo de audio a generar
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Hago el tts
        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Escribo retorno el audio generado
        return response.audio_content

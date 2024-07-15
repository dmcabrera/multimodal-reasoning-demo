import os
import base64
from flask import Flask
from flask import request
from flask_cors import CORS
from middleware import jwt_authenticated

from multimodal_reasoning_tool import MultimodalReasoningTool

# Main Flask app
app = Flask(__name__)
CORS(app)

# Multimodal reasoning tool
multimodal_reasoning_tool = MultimodalReasoningTool()

# Validate the ID token before every request
@app.before_request
def before_request_func():
    print('')

# Chat endpoint
@app.route("/reason", methods=['POST'])
#@jwt_authenticated
def reason():
    # Get the json request
    request_json = request.get_json(silent=True)
    #print(request_json)

    # Get the video data
    video_data = request_json["video_data"]
    
    # Transform video data to base64
    video_data = base64.b64decode(video_data)
    #print(video_data)

    # Razono
    response_text = multimodal_reasoning_tool.reason(video_data)
    print(response_text)

    # Genero el audio de la respuesta
    response_audio = multimodal_reasoning_tool.talk(response_text)
    response_audio = base64.b64encode(response_audio).decode('ascii')
    # Transformo el audio a base64

    # Retorno la respuesta
    return {
        "response_text" : response_text,
        "response_audio" : response_audio
    }

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))




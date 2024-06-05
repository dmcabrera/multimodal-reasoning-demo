gcloud auth application-default login

TOKEN="ya29.a0Ael9sCO0G_VHuITkka1hJwNeO069i4vPvlW8eYu1-UGvbvNW-mDKafZr6Nwq0GaUgGOGjiBgwdTcn3HdvvQKGMfdjC0Naw8_K6UyfmKBh5hqx1Gza9bPl1rl4Joud0NSFZB5dT7Du6AdXRNqkX-GeDqYXzFw_AaCgYKAY4SAQ4SFQF4udJhubwumz3dKzR6_MqqJKIlKw0165"
API_ENDPOINT="us-central1-aiplatform.googleapis.com"
PROJECT_ID="cloud-large-language-models"
ENDPOINT_ID="4511608470067216384"

curl \
-X POST \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
"https://${API_ENDPOINT}/v1/projects/${PROJECT_ID}/locations/us-central1/endpoints/${ENDPOINT_ID}:predict" -d $'{
  "instances": [
    { "content": "cuál es el producto más caro de la siguiente lista?

Id,Description,Group,Stock,Price
1000,Celulosa Kraft Blanca de Fibra,Celulosa,100,1500
1001,Celulosa Kraft Gris de Fibra,Celulosa,50,1700
1003,Papeles Sack Kraft,Papel,250,2500
1004,Envase para Productos Pequeños,Envases,120,3500
1005,Envase para Productos Medianos,Envases,150,2500
1006,Envase para Productos Grandes,Envases,170,1500"}
  ],
  "parameters": {
    "temperature": 0.2,
    "maxDecodeSteps": 256,
    "topP": 0.8,
    "topK": 40
  }
}'

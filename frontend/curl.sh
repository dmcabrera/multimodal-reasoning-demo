curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"localhost:8080" -d \
$'{
  "prompt": "Hola"
}'
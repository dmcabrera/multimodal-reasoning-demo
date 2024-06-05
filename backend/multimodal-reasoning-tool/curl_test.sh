curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"https://sales-bot-service-5m5mdb55ja-uc.a.run.app/chat" -d \
$'{
  "criterio" : "zapatos rojos con lazo negro"}
}'

curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"http://localhost:8080/buscar_articulos" -d \
$'{
  "criterio" : "zapatos rojos de mujer con un lazo negro"
}'


curl \
-X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
"http://127.0.0.1:8080/chat" -d \
$'{
  "message" : {"text" : "Hola cómo estás?"}
}'

curl \
-X POST \
-H "Content-Type: application/json" \
"https://telco-bot-api-gtw-c0nyzj85.uc.gateway.dev/chat" -d \
$'{
  "message" : {"text" : "Hola, cómo estás?"}
}'
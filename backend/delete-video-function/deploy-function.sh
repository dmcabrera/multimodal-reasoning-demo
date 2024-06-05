gcloud functions deploy delete-video-function \
--gen2 \
--region="us-central1" \
--runtime="python312" \
--source=. \
--entry-point="delete_video" \
--trigger-topic="delete_video_topic"
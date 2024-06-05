import base64
import functions_framework
from google.cloud import storage

# Elimino un archivo de gcs
def delete_file_from_cs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None
    blob.reload()
    generation_match_precondition = blob.generation
    blob.delete(if_generation_match=generation_match_precondition)
    print(f"Blob {blob_name} deleted.")

# Trigger function for video deletion
@functions_framework.cloud_event
def delete_video(cloud_event):
  video_name = base64.b64decode(cloud_event.data["message"]["data"]).decode()
  print(f"Deleting video {video_name}...")
  delete_file_from_cs("cecl-genai-demos-vertex2", "videos/" + video_name)
  print(f"Video {video_name} deleted.")
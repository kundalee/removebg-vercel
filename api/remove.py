from transparent_background import Remover
import base64
import io
from PIL import Image

def handler(request):
    if request.method != "POST":
        return {"statusCode": 405, "body": "Method Not Allowed"}

    try:
        body = request.get_json()
        image_b64 = body.get("image_base64")
        if not image_b64:
            return {"statusCode": 400, "body": "Missing image_base64"}

        image_data = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_data))

        remover = Remover()
        result = remover.remove(image)

        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        result_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"image_base64": "{result_b64}"}}'
        }

    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

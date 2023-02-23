from flask import Flask, request
import asyncio

from services.aws import AWS
from services.image_classification import image_classification as predict

app = Flask(__name__)

aws = AWS(app)
s3 = aws.s3()
sqs = aws.sqs()

asyncio.get_event_loop().run_until_complete(sqs.setIntervalPolling())

@app.route('/')
def hello_world():
	return 'Hello World from Group : EC3!'

@app.route('/predict_image')
def predict_image():
    url = request.args.get("image_url")
    if(url):
        name, prediction = predict(url)
        # s3.store(name,'({},{})'.format(name,prediction))
        # sqs.push_to_sqs(name,prediction)
        return {
            "url": url,
            "success": True,
            "result": {
                "name": name,
                "prediction": prediction
            }
        }
    return {
            "url": url,
            "success": False
        } 


if __name__ == "__main__":
	app.run()
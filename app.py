import time
from flask import Flask, stream_with_context, request, Response
app = Flask(__name__, static_url_path='',static_folder='static')

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.route('/compute-image')
def compute_image():
    def generate():
        huge_number = 100000
        progress = 0

        # Start by sending total JSON value to the client stream
        yield "{\"total\": %d}" % huge_number

        for i in range(huge_number):
            # If there is a 100 step progress, send progress JSON value to the client stream
            if progress >= 100:
                progress = 0
                yield "{\"progress\": %d}" % (i)
            # Else increment progress by 1 and sleep a bit
            else:
                progress = progress + 1
                time.sleep(0.0005)
        
        # Send the generated image location to the client when we're done
        yield "{\"img_url\": \"/some/generated/image.png\"}"
    
    # Return the stream context with out generator function
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

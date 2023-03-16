# Description: handlers
# Flask adapter
from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler
from flask import Request
from ponzu_bot.app import app


slack_handler = SlackRequestHandler(app)

# Cloud Function
def ponzu_bolt_app(req: Request):
    """HTTP Cloud Function.
    Args:
        req (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    return slack_handler.handle(req)


# For local development
if __name__ == "__main__":
    from flask import Flask, request

    flask_app = Flask(__name__)

    @flask_app.route("/slack/events", methods=["GET", "POST"])
    def handle_anything():
        return slack_handler.handle(request)
    flask_app.run(port=3000)
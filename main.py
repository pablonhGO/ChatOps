from typing import Any, Mapping
from introduction import introduce
from chat import chat

import flask
import functions_framework


# Google Cloud Function that responds to messages sent in
# Google Chat.
#
# @param {Object} req Request sent from Google Chat.
# @param {Object} res Response to send back.
@functions_framework.http
def hello_chat(req: flask.Request) -> Mapping[str, Any]:
  if req.method == "GET":
    return "Hello! This function must be called from Google Chat."

  request_json = req.get_json(silent=True)

  print(request_json["message"]["slashCommand"]["commandId"])

  if slash_command := request_json.get('message', dict()).get('slashCommand'):
    command_id = slash_command['commandId']
    print(command_id)
    match command_id:
      case "1":
        display_name = request_json["message"]["sender"]["displayName"]
        avatar = request_json["message"]["sender"]["avatarUrl"]
        return introduce(name=display_name, image_url=avatar)
      case "2":
        print(request_json["message"]["text"])
        user_input = request_json["message"]["text"]
        return chat(user_input)
      case _:
        return "Oh no! Something broke."

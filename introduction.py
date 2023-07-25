from typing import Any, Mapping

import functions_framework

# Creates a card with two widgets.
# @param {string} name the sender's display name.
# @param {string} image_url the URL for the sender's avatar.
# @return {Object} a card with the user's avatar.
def introduce(name: str, image_url: str) -> Mapping[str, Any]:
  
  avatar_text_widget = {"textParagraph": {"text": "Hi there! I'm Go Reply's ChatOps bot, a DevOps assistant. I can help you find out information about your GCP project."}}
  avatar_section = {"widgets": [avatar_text_widget]}

  header = {"title": f"Hello {name}!"}

  cards = {
      "cardsV2": [
          {
              "cardId": "avatarCard",
              "card": {
                  "name": "Avatar Card",
                  "header": header,
                  "sections": [avatar_section],
              },
          }
      ]
  }

  return cards

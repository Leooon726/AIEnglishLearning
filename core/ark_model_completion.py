import os
import logging
from volcenginesdkarkruntime import Ark
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ArkModelCompletion:
    def __init__(self):
        api_key = os.getenv('ARK_API_KEY')
        assert api_key is not None, "ARK_API_KEY is not set"
        self.client = Ark(
            api_key=api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        logging.info("ArkModelCompletion initialized with API key.")

    def query_model(self, system_content, user_content):
        logging.info("Querying model with system content and user content.")
        # Non-streaming request
        completion = self.client.chat.completions.create(
            model="ep-20240930222858-7mzmx",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
        )
        response = completion.choices[0].message.content
        logging.info("Model query completed.")
        return response

if __name__ == "__main__":
    ark_model = ArkModelCompletion()
    # print(ark_model.query_model("You are a chatbot.", "I am fine, thank you."))
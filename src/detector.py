from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from src.config import Config
from src.prompt import SYSTEM_PROMPT

class EvaluationVerdict(BaseModel):
    is_contradictory: bool = Field(description="True if the text contains an internal logical conflict or self-contradiction; False otherwise.")
    reason: str = Field(description="A clear, concise explanation pinpointing exactly why the text does or does not contradict itself.")

class ContradictionDetector:
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in your .env file.")
        # Correctly initialize the standard Google GenAI Client
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def analyze_text(self, text: str) -> EvaluationVerdict:
        try:
            response = self.client.models.generate_content(
                model=Config.MODEL_NAME,
                contents=f"Text to evaluate:\n\n{text}",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.0,
                    response_mime_type="application/json",
                    response_schema=EvaluationVerdict,
                ),
            )
            # The official SDK automatically converts the JSON string straight into your Pydantic object!
            return response.parsed
        except Exception as e:
            return EvaluationVerdict(
                is_contradictory=False,
                reason=f"Error executing Gemini assessment: {str(e)}"
            )
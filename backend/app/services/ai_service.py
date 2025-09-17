import openai
import os
from typing import Dict, Any
import asyncio
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        """Inicializa el cliente de OpenAI"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if self.api_key:
            self.client = openai.OpenAI(api_key=self.api_key)
            self.use_openai = True
        else:
            self.client = None
            self.use_openai = False
            print("PPENAI_API_KEY no configurada. Usando respuestas simuladas.")

    async def generate_roast_and_feedback(self, cv_text: str) -> Dict[str, Any]:
        """
        Genera roast y feedback usando OpenAI o respuesta simulada
        Args:
            cv_text: Texto extraído del CV
        Returns:
            Dict con roast, feedback y metadata
        """
        try:
            if not self.use_openai:
                return self._generate_mock_response(cv_text) #respuesta simulada cuando no hay API key
            
            roast_prompt = self._create_roast_prompt(cv_text) #creamos el prompt
            response = await asyncio.to_thread(
                self._call_openai, 
                roast_prompt
            ) #llamamos la api
                        
            return self._parse_ai_response(response) #devolvemos la respuesta parseada
            
        except Exception as e:
            print(f"Error con OpenAI, usando respuesta simulada: {str(e)}")
            return self._generate_mock_response(cv_text)

    def _create_roast_prompt(self, cv_text: str) -> str:
        """Crea el prompt optimizado para generar el roast, pasando el texto del cv"""
        return f"""
You are a brutally honest but constructive CV reviewer with a sharp sense of humor. 
Your job is to roast this resume while providing actionable feedback.

TONE: Sarcastic, witty, brutally honest, but ultimately helpful
LANGUAGE: Mix of professional insights with savage humor
GOAL: Point out flaws in an entertaining way, then provide real solutions

CV TO ROAST:
{cv_text}

RESPOND IN THIS EXACT JSON FORMAT:
{{
    "roast": "Your brutal but funny roast here (2-3 sentences max, be savage but not mean-spirited)",
    "feedback": [
        "Specific actionable improvement 1",
        "Specific actionable improvement 2", 
        "Specific actionable improvement 3",
        "Specific actionable improvement 4"
    ],
    "brutality_level": 75
}}

ROAST EXAMPLES (for inspiration):
- "This CV reads like it was written during a coffee shop earthquake"
- "Your bullet points say everything and nothing at the same time"
- "Excel Expert? I bet you can't even make a proper SUM formula"

FEEDBACK SHOULD BE:
- Actionable and specific
- Professional advice disguised as roast recovery
- Focus on: formatting, content, quantification, relevance

Make it hurt (a little) but help them win! 🔥
"""

    def _call_openai(self, prompt: str) -> str:
        """Llama a la API de OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a witty, brutal but constructive CV reviewer. Always respond in valid JSON format."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.8,
                response_format={"type": "json_object"} #Fuerza respuesta JSON
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error en API de OpenAI: {str(e)}")

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea y valida la respuesta de la IA"""
        try:
            import json
            
            data = json.loads(response_text) #Parsear JSON
            
            #Validar estructura
            required_fields = ["roast", "feedback", "brutality_level"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Campo requerido faltante: {field}")
            
            #Validar tipos
            if not isinstance(data["roast"], str):
                raise ValueError("'roast' debe ser string")
            if not isinstance(data["feedback"], list):
                raise ValueError("'feedback' debe ser lista")
            if not isinstance(data["brutality_level"], int):
                raise ValueError("'brutality_level' debe ser entero")
            
            data["brutality_level"] = max(1, min(100, data["brutality_level"]))
            
            return data
            
        except json.JSONDecodeError:
            #Fallback si falla el JSON
            return {
                "roast": "Your CV is so confusing, even AI couldn't process it properly. That's... actually impressive in a terrible way.",
                "feedback": [
                    "Make your CV more readable and properly formatted",
                    "Use standard fonts and clear section headers",
                    "Avoid weird formatting that breaks text extraction",
                    "Keep it simple - if AI can't read it, humans will struggle too"
                ],
                "brutality_level": 85
            }
        except Exception as e:
            raise Exception(f"Error procesando respuesta de IA: {str(e)}")

    def _generate_mock_response(self, cv_text: str) -> Dict[str, Any]:
        """Genera una respuesta simulada cuando no hay API key de OpenAI"""
        import random
        
        roasts = [
            "Well, well, well... looks like someone copy-pasted their CV from a template and called it a day. The lack of originality here is so impressive, it should be its own skill on your resume.",
            "This CV is like a participation trophy - technically it exists, but nobody's really proud of it. I've seen more personality in a tax form.",
            "Your CV reads like it was written by someone who learned about jobs from watching sitcoms. 'Hardworking team player'? Come on, even my spam folder has more creativity.",
            "I've seen grocery lists with more compelling narratives than this CV. At least those tell a story about dinner plans.",
            "This resume is so generic, I'm pretty sure I could fill in Mad Libs and get something more personalized."
        ]
        
        feedback_options = [
            "Add specific achievements with numbers and metrics",
            "Remove generic buzzwords like 'hardworking' and 'team player'",
            "Include relevant projects or portfolio links",
            "Tailor your experience to the job you're applying for",
            "Use action verbs to start each bullet point",
            "Quantify your impact wherever possible",
            "Keep it to 1-2 pages maximum",
            "Use a cleaner, more professional format",
            "Add relevant technical skills",
            "Include education and certifications if relevant"
        ]
        
        selected_feedback = random.sample(feedback_options, random.randint(3, 6))
        
        return {
            "roast": random.choice(roasts),
            "feedback": selected_feedback,
            "brutality_level": random.randint(75, 95)
        }
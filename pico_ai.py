from groq import Groq

api_key="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"



client = Groq(api_key=api_key)

class PicoAI:
	def __init__(self):
		self.chat_history = []


	def chat(self,user_message):
		# add user message to history
		self.chat_history.append({
			"role": "user",
			"content": user_message
		})
		
		# send full history every time
		response = client.chat.completions.create(
			model="llama-3.1-8b-instant",
			messages=self.chat_history
		)
		
		assistant_message = response.choices[0].message.content
		
		# add assistant response to history
		self.chat_history.append({
			"role": "assistant",
			"content": assistant_message
		})
		
		return assistant_message
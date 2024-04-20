import google.generativeai as genai

# Configure the generative model
genai.configure(api_key="Your Api key")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

# Initialize the generative model
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Start a conversation
convo = model.start_chat(history=[])

def respond(user_input):
  convo.send_message(user_input)
  print(convo.last.text)

  if convo.last.text == None:
    return("none")
  else:
    return(convo.last.text)


respond("my gal friend left me")

from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY", #add your api key here
)
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a virtual assistant skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
) 

print(completion.choices[0].message.content)


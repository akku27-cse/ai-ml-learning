const response = await fetch("https://api.openai.com/v1/chat/completions", 
  {
    method: "POST",
    headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer YOUR_API_KEY`
  },    
  body: JSON.stringify({
    model: "gpt-3.5-turbo",
    messages: [
      { role: "system", content: "You are a friendly chatbot for Apexium App." },
      { role: "user", content: "Hello!" }
    ]
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
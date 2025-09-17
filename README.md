# PDF-Text-Converter
This project is about converting the uploaded PDF into a different Tempalate.The flow of the code is Text in the PDF is extracted,converted into JSON using Groq API an the JSON output is converted to whichever tempalate the user wans.The libraries used are PyPDF2 for reading the Pdf ,io.Bytes for reading the raw Data of the PDF in form of Bytes and storing it in the RAM and then extracted into a plain text .
The model used here for converting the data into JSON is openai/gpt-oss-2b.
For API go through this website https://console.groq.com/home

import torch
from transformers import BioGptTokenizer, BioGptForCausalLM, set_seed
import ollama
import streamlit as st

bio_model_name = "microsoft/biogpt"
bio_tokenizer = BioGptTokenizer.from_pretrained(bio_model_name)
bio_model = BioGptForCausalLM.from_pretrained(bio_model_name)

llama_model_name = "llama2"

set_seed(42)

def generate_biogpt_response(sentence):
    """Generate a short biomedical explanation from BioGPT."""
    inputs = bio_tokenizer(sentence, return_tensors="pt")
    
    with torch.no_grad():
        beam_output = bio_model.generate(
            **inputs,
            min_length=50,
            max_length=100,
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2
        )
    
    output_text = bio_tokenizer.decode(beam_output[0], skip_special_tokens=True)
    return output_text

def generate_genewise_response(user_query):
    """Generate a combined response using BioGPT and LLaMA 2."""
    bio_response = generate_biogpt_response(user_query)
    
    full_response = ollama.chat(
        model=llama_model_name,
        messages=[{"role": "user", "content": f"Expand on this biomedical explanation: {bio_response}"}]
    )
    
    return f"**GeneWise Response:**\n\n{full_response['message']['content']}"

# Streamlit interface
st.title("GeneWise: AI-Powered Biomedical Insights")

st.write("""
    Enter a biomedical-related query below.
    GeneWise will provide a scientifically accurate response.
    The chat history will be saved until you exit.
""")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your biomedical query (type 'exit' to stop):")

if user_input:
    if user_input.lower() == "exit":
        st.write("Chat ended. Refresh the page to start a new session.")
    else:
        genewise_response = generate_genewise_response(user_input)
        st.session_state.chat_history.append((user_input, genewise_response))

# Display chat history
st.subheader("Chat History:")
for query, response in st.session_state.chat_history:
    st.write(f"**You:** {query}")
    st.write(response)
    st.write("---")
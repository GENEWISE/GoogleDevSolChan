import torch
from transformers import BioGptTokenizer, BioGptForCausalLM, set_seed
import ollama
import streamlit as st

@st.cache_resource
def load_biogpt_model():
    tokenizer = BioGptTokenizer.from_pretrained("microsoft/biogpt")
    model = BioGptForCausalLM.from_pretrained("microsoft/biogpt")
    return tokenizer, model

bio_tokenizer, bio_model = load_biogpt_model()
llama_model_name = "llama2"

set_seed(42)

def generate_biogpt_response(sentence, min_length=50, max_length=150):
    """Generate a biomedical explanation from BioGPT."""
    inputs = bio_tokenizer(sentence, return_tensors="pt")
    
    with torch.no_grad():
        beam_output = bio_model.generate(
            **inputs,
            min_length=min_length,
            max_length=max_length,
            num_beams=5,
            early_stopping=True,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2
        )
    
    output_text = bio_tokenizer.decode(beam_output[0], skip_special_tokens=True)
    return output_text

def generate_llama_response(expanded_info):
    """Generate a longer, more detailed explanation using LLaMA 2."""
    prompt = f"""
    You are a helpful biomedical assistant. The following is a brief explanation of a biomedical concept:
    
    "{expanded_info}"
    
    Please expand on this explanation with more details, examples, and context. Make it educational and informative.
    """
    
    try:
        response = ollama.chat(model=llama_model_name, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {str(e)}\n\nPlease make sure Ollama is running with the llama2 model."

st.title("BioMedical Information System")
st.write("### Powered by BioGPT and LLaMA 2")

st.markdown("""
    This application combines two AI models to provide comprehensive biomedical information:
    - **BioGPT**: Provides concise, scientifically accurate biomedical explanations
    - **LLaMA 2**: Expands the explanation with additional context and details
""")

st.sidebar.header("Configuration")
min_length = st.sidebar.slider("Minimum Length (BioGPT)", 30, 100, 50)
max_length = st.sidebar.slider("Maximum Length (BioGPT)", 100, 500, 150)

st.sidebar.header("Example Queries")
examples = [
    "What is the mechanism of action for statins?",
    "How does CRISPR-Cas9 gene editing work?",
    "Explain the pathophysiology of type 2 diabetes.",
    "What are the effects of ACE inhibitors on the renin-angiotensin system?",
    "How do mRNA vaccines provide immunity?"
]
for example in examples:
    if st.sidebar.button(example):
        st.session_state.user_input = example

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

user_input = st.text_area("Enter a biomedical query:", 
                          value=st.session_state.user_input,
                          height=100)

if st.button("Generate Information") or (user_input and user_input != st.session_state.user_input):
    st.session_state.user_input = user_input
    
    if user_input:
        with st.spinner("Generating BioGPT response..."):
            bio_info = generate_biogpt_response(user_input, min_length, max_length)
            
        st.subheader("BioGPT Explanation:")
        st.info(bio_info)
        
        with st.spinner("Expanding information with LLaMA 2..."):
            
            llama_expansion = generate_llama_response(bio_info)
        
        st.subheader("LLaMA 2 Detailed Explanation:")
        st.success(llama_expansion)
        
       
        st.markdown("---")
        st.caption("Note: This information is generated by AI models and should be verified with authoritative medical sources before use in clinical settings.")

st.sidebar.markdown("---")
st.sidebar.subheader("System Status")
st.sidebar.text("BioGPT: Loaded ")


try:
    ollama.list()
    st.sidebar.text("Ollama: Connected ")
except:
    st.sidebar.text("Ollama: Not connected ")
    st.sidebar.warning("Please make sure Ollama is running with the llama2 model installed.")
    st.sidebar.markdown("Installation instructions: [Ollama](https://github.com/ollama/ollama)")
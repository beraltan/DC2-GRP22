import streamlit as st
import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

# Function to generate embeddings using a transformer model
def generate_embeddings(data, text_columns, model_name='bert-base-uncased'):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for column in text_columns:
        embeddings = []
        texts = data[column].astype(str).tolist()
        total_texts = len(texts)
        
        progress_bar = st.progress(0)
        for i, text in enumerate(texts):
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
            inputs = {key: value.to(device) for key, value in inputs.items()}
            with torch.no_grad():
                outputs = model(**inputs)
            embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy().flatten()
            embeddings.append(embedding)
            
            # Update progress bar
            progress = (i + 1) / total_texts
            progress_bar.progress(progress)
        
        data[f'{column}_embedding'] = embeddings
    return data

st.title("Text Embedder using Transformers")

# Step 1: Upload dataset
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())
    
    # Step 2: Select text columns to embed
    text_columns = st.multiselect("Select text columns to embed", options=data.columns)
    
    if st.button("Generate Embeddings"):
        with st.spinner("Generating embeddings..."):
            data = generate_embeddings(data, text_columns)
        st.write("Data with Embeddings:")
        st.write(data.head())
        
        # Step 3: Download the updated dataset
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download updated data as CSV",
            data=csv,
            file_name='embedded_data.csv',
            mime='text/csv',
        )

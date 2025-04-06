import streamlit as st
import requests
import json
import random
import os
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Variant Pathogenicity Checker",
    page_icon="🧬",
    layout="wide"
)

API_URL_GET = "https://myvariant.info/v1/variant/"
API_URL_POST = "https://myvariant.info/v1/variant"

def generate_filename():
    """Generate a unique filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"variant_result_{timestamp}_{random.randint(1000, 9999)}.txt"

def fetch_single_variant(chromosome, position, ref, alt):
    """Fetch pathogenicity data for a single variant using a GET request."""
    variant_id = f"chr{chromosome}:g.{position}{ref}>{alt}"  # HGVS format
    
    with st.spinner(f"Fetching data for variant {variant_id}..."):
        try:
            response = requests.get(API_URL_GET + variant_id, params={"fields": "all"})
            response.raise_for_status()
            data = response.json()
            return data if "error" not in data else None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API Request Failed: {e}")
            return None

def fetch_batch_variants(variant_list):
    with st.spinner(f"Fetching data for {len(variant_list)} variants..."):
        try:
            response = requests.post(
                API_URL_POST,
                json={"ids": variant_list, "fields": "all"},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else None
        except requests.exceptions.RequestException as e:
            st.error(f"❌ API Request Failed: {e}")
            return None

def save_to_file(data):
    """Save data to a text file and provide download link"""
    filename = generate_filename()
    
    try:
        # Convert data to JSON string
        if isinstance(data, (dict, list)):
            file_content = json.dumps(data, indent=2)
        else:
            file_content = str(data)
            
        # Create download button
        st.download_button(
            label="⬇️ Download Results",
            data=file_content,
            file_name=filename,
            mime="text/plain"
        )
        
        return True
    except Exception as e:
        st.error(f"❌ Error preparing file: {e}")
        return False

def extract_pathogenicity_info(variant_data):
    """Extract key pathogenicity information from variant data"""
    if not variant_data:
        return None
        
    pathogenicity = {}
    
    if "clinvar" in variant_data:
        clinvar = variant_data["clinvar"]
        pathogenicity["clinvar_significance"] = clinvar.get("rcv", [{}])[0].get("clinical_significance") if "rcv" in clinvar and clinvar["rcv"] else "Not available"
        
    if "dbsnp" in variant_data:
        pathogenicity["rsid"] = variant_data["dbsnp"].get("rsid", "Not available")
    
    if "gnomad_exome" in variant_data:
        pathogenicity["gnomad_af"] = variant_data["gnomad_exome"].get("af", {}).get("af", "Not available")
    
    if "cadd" in variant_data:
        pathogenicity["cadd_score"] = variant_data["cadd"].get("phred", "Not available")
    
    return pathogenicity

st.title("🧬 Variant Pathogenicity Checker")
st.sidebar.image("https://img.icons8.com/plasticine/100/000000/dna-helix.png", width=100)
st.sidebar.title("Tool Options")

st.markdown("""
This tool queries the MyVariant.info API to retrieve pathogenicity data for genomic variants.
Enter variant information either individually or in batch to check potential clinical significance.
""")

mode = st.sidebar.radio(
    "Select Query Mode:",
    ["Single Variant", "Batch Query", "Upload Variant File"]
)

main_col, results_col = st.columns([1, 2])

with main_col:
    if mode == "Single Variant":
        st.subheader("Single Variant Query")
        
        chromosome = st.selectbox(
            "Chromosome:",
            options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                     "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                     "21", "22", "X", "Y", "MT"]
        )
        
        position = st.number_input("Position:", min_value=1, value=100000, format="%d")
        ref = st.selectbox("Reference Allele:", options=["A", "T", "G", "C"])
        alt = st.selectbox("Alternate Allele:", options=["A", "T", "G", "C"])

        if ref == alt:
            st.warning("⚠️ Reference and alternate alleles cannot be the same.")
            is_valid = False
        else:
            is_valid = True
        
        if st.button("🔍 Check Variant", disabled=not is_valid):
            variant_id = f"chr{chromosome}:g.{position}{ref}>{alt}"
            st.session_state.variant_id = variant_id
            st.session_state.result = fetch_single_variant(chromosome, position, ref, alt)
            
            if not st.session_state.result:
                st.error(f"❌ No data found for variant {variant_id}")
            else:
                st.success(f"✅ Data retrieved for {variant_id}")
                
    elif mode == "Batch Query":
        st.subheader("Batch Variant Query")
        
        # Use a form for batch input
        with st.form("batch_form"):
            num_variants = st.slider("Number of variants to query:", min_value=1, max_value=50, value=3)
            
            variants = []
            variant_ids = []
            
            for i in range(num_variants):
                st.markdown(f"**Variant {i+1}**")
                cols = st.columns(4)
                
                with cols[0]:
                    chrom = st.selectbox(
                        f"Chromosome {i+1}:",
                        options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 
                                "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                                "21", "22", "X", "Y", "MT"],
                        key=f"chrom_{i}"
                    )
                
                with cols[1]:
                    pos = st.number_input(f"Position {i+1}:", min_value=1, value=100000, format="%d", key=f"pos_{i}")
                
                with cols[2]:
                    ref = st.selectbox(f"Ref {i+1}:", options=["A", "T", "G", "C"], key=f"ref_{i}")
                
                with cols[3]:
                    alt = st.selectbox(f"Alt {i+1}:", options=["A", "T", "G", "C"], key=f"alt_{i}")
                
                if ref != alt:
                    variant_id = f"chr{chrom}:g.{pos}{ref}>{alt}"
                    variants.append({
                        "id": variant_id,
                        "chromosome": chrom,
                        "position": pos,
                        "ref": ref,
                        "alt": alt
                    })
                    variant_ids.append(variant_id)
            
            submitted = st.form_submit_button("🔍 Check Variants")
            
            if submitted:
                if not variant_ids:
                    st.error("❌ No valid variants to query.")
                else:
                    st.session_state.batch_variants = variants
                    st.session_state.variant_ids = variant_ids
                    st.session_state.batch_results = fetch_batch_variants(variant_ids)
                    
                    if not st.session_state.batch_results:
                        st.error("❌ No data found for the specified variants.")
                    else:
                        st.success(f"✅ Data retrieved for {len(variant_ids)} variants.")
    
    elif mode == "Upload Variant File":
        st.subheader("Upload Variant File")
        
        st.markdown("""
        Upload a CSV or TSV file with variant information.
        
        **Required columns**:
        - `chromosome` (1-22, X, Y, MT)
        - `position` (positive integer)
        - `ref` (A, T, G, C)
        - `alt` (A, T, G, C)
        
        Optional header row.
        """)
        
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "tsv", "txt"])
        
        if uploaded_file is not None:
            try:
                # Determine if it's CSV or TSV
                file_extension = uploaded_file.name.split(".")[-1].lower()
                delimiter = "," if file_extension == "csv" else "\t"
                
                # Read the file
                df = pd.read_csv(uploaded_file, delimiter=delimiter)
                
                # Normalize column names (case-insensitive)
                df.columns = [col.lower().strip() for col in df.columns]
                
                # Validate the required columns exist
                required_cols = ["chromosome", "position", "ref", "alt"]
                missing_cols = [col for col in required_cols if col not in df.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                else:
                    # Display preview
                    st.write("File Preview:")
                    st.dataframe(df.head())
                    
                    # Process variants
                    variants = []
                    variant_ids = []
                    
                    for _, row in df.iterrows():
                        chrom = str(row["chromosome"]).strip()
                        pos = str(row["position"]).strip()
                        ref = str(row["ref"]).strip().upper()
                        alt = str(row["alt"]).strip().upper()
                        
                        # Validate variant
                        if (pos.isdigit() and int(pos) > 0 and 
                            ref in ["A", "T", "G", "C"] and 
                            alt in ["A", "T", "G", "C"] and 
                            ref != alt):
                            
                            variant_id = f"chr{chrom}:g.{pos}{ref}>{alt}"
                            variants.append({
                                "id": variant_id,
                                "chromosome": chrom,
                                "position": pos,
                                "ref": ref,
                                "alt": alt
                            })
                            variant_ids.append(variant_id)
                    
                    st.write(f"Found {len(variant_ids)} valid variants in file.")
                    
                    if variant_ids and st.button("🔍 Check Variants"):
                        # Limit batch size
                        batch_size = min(len(variant_ids), 1000)
                        if batch_size < len(variant_ids):
                            st.warning(f"⚠️ Limiting query to first {batch_size} variants (API limit).")
                        
                        variant_ids = variant_ids[:batch_size]
                        variants = variants[:batch_size]
                        
                        st.session_state.batch_variants = variants
                        st.session_state.variant_ids = variant_ids
                        st.session_state.batch_results = fetch_batch_variants(variant_ids)
                        
                        if not st.session_state.batch_results:
                            st.error("❌ No data found for the specified variants.")
                        else:
                            st.success(f"✅ Data retrieved for {len(variant_ids)} variants.")
                    
            except Exception as e:
                st.error(f"❌ Error processing file: {e}")

with results_col:
    st.subheader("Results")
    
    if mode == "Single Variant" and "result" in st.session_state and st.session_state.result:

        variant_id = st.session_state.variant_id
        result = st.session_state.result
        pathogenicity = extract_pathogenicity_info(result)
    
        st.markdown(f"**Variant ID:** {variant_id}")
        
        if pathogenicity:
            st.markdown("### Key Pathogenicity Information")
            for key, value in pathogenicity.items():
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Display tabs for different views
        tab1, tab2 = st.tabs(["Formatted View", "Raw JSON"])
        
        with tab1:
            st.json(result)
            
        with tab2:
            st.code(json.dumps(result, indent=2))
        
        # Save results to file
        st.markdown("### Download Results")
        save_to_file(result)
        
    elif (mode in ["Batch Query", "Upload Variant File"] and 
          "batch_results" in st.session_state and 
          st.session_state.batch_results):
        
        batch_results = st.session_state.batch_results
        variants = st.session_state.batch_variants
        
        # Create a summary table
        st.markdown("### Variants Summary")
        
        summary_data = []
        
        for i, (variant, result) in enumerate(zip(variants, batch_results)):
            variant_info = {
                "Variant ID": variant["id"],
                "Chromosome": variant["chromosome"],
                "Position": variant["position"],
                "Ref": variant["ref"],
                "Alt": variant["alt"],
            }
            
            # Check if data was found
            if "notfound" in result:
                variant_info["Status"] = "❌ Not Found"
                variant_info["ClinVar"] = "N/A"
                variant_info["CADD Score"] = "N/A"
            else:
                variant_info["Status"] = "✅ Found"
                
                # Extract pathogenicity info
                pathogenicity = extract_pathogenicity_info(result)
                if pathogenicity:
                    variant_info["ClinVar"] = pathogenicity.get("clinvar_significance", "N/A")
                    variant_info["CADD Score"] = pathogenicity.get("cadd_score", "N/A")
                else:
                    variant_info["ClinVar"] = "N/A"
                    variant_info["CADD Score"] = "N/A"
            
            summary_data.append(variant_info)
        
        # Display summary table
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df)
        
        # Display detailed results
        st.markdown("### Detailed Results")
        
        # Use expanders for each variant
        for i, (variant, result) in enumerate(zip(variants, batch_results)):
            with st.expander(f"Variant {i+1}: {variant['id']}"):
                if "notfound" in result:
                    st.warning("❌ No data found for this variant.")
                else:
                    st.json(result)
        
        # Create a comprehensive output with variant details and results
        output_data = {
            "query_info": {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "query_type": "batch",
                "variants_submitted": len(variants),
                "variants_with_data": len([r for r in batch_results if "notfound" not in r])
            },
            "variant_details": variants,
            "results": batch_results,
            "summary": summary_data
        }
        
        # Save results to file
        st.markdown("### Download Results")
        save_to_file(output_data)

# Add footer
st.markdown("---")
st.markdown("""
**About this tool**: This Streamlit app queries the MyVariant.info API to retrieve 
pathogenicity information for genomic variants.

**Disclaimer**: This tool is for research purposes only. Clinical decisions should 
not be made based solely on the results provided here.
""")
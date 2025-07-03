import streamlit as st
from Src.extractor import extract_all

st.set_page_config(page_title="📄 Doc Loader Bot", layout="centered")

st.title("🤖 Chatbot Peraturan Perusahaan - Tahap 1")
st.write("Upload dokumen peraturan perusahaan untuk diekstrak dan diproses.")

st.markdown("---")
uploaded_file = st.file_uploader("📤 Upload file (PDF, DOCX, Excel, CSV)", type=["pdf", "docx", "xlsx", "xls", "csv"])

if uploaded_file is not None:
    with st.spinner("⏳ Mengekstrak isi dokumen..."):
        results = extract_all(uploaded_file)

    if "❌" in results["text"]:
        st.error(results["text"])
    else:
        st.success("✅ Dokumen berhasil diproses!")

        with st.expander("📄 Lihat Isi Dokumen"):
            st.text_area("Isi Dokumen", results["text"], height=400)

        if results["layout"]:
            for page in results["layout"]:
                with st.expander(f"📄 Halaman {page['halaman']}"):
                    st.text(page['konten'])
else:
    st.info("📝 Silakan upload dokumen terlebih dahulu.")

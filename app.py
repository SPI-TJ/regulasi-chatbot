# file: app.py

import streamlit as st
from Src.extractor import extract_all

st.set_page_config(page_title="📄 Doc Loader Bot", layout="wide")

st.title("🤖 Chatbot Peraturan Perusahaan - Tahap 1")
st.write("Upload dokumen peraturan perusahaan (PDF, DOCX, Excel, CSV) untuk diekstrak dan diproses.")

st.markdown("---")
uploaded_file = st.file_uploader(
    "📤 Upload dokumen:",
    type=["pdf", "docx", "xlsx", "xls", "csv"]
)

if uploaded_file:
    with st.spinner("⏳ Mengekstrak isi dokumen..."):
        results = extract_all(uploaded_file)

    if results["status"] == "error":
        st.error(results["text"])
    else:
        st.success("✅ Dokumen berhasil diproses!")

        # Show basic metadata
        st.markdown(f"**📁 Nama File:** `{results['filename']}`")
        st.markdown(f"**📄 Tipe File:** `{results['file_ext']}`")
        st.markdown("---")

        # Show full text (raw extraction)
        with st.expander("📝 Teks Lengkap Dokumen"):
            st.text_area("Isi Teks:", results["text"], height=400)

        # Show layout per halaman (PDF only)
        if results["layout"]:
            st.markdown("## 🧾 Layout Per Halaman (PDF)")
            for page in results["layout"]:
                with st.expander(f"📄 Halaman {page['halaman']}"):
                    st.text(page['konten'])

else:
    st.info("📝 Silakan upload dokumen terlebih dahulu.")

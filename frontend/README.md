Streamlit Frontend for DeepSearcher

Run locally:

1. Create and activate a Python environment.
2. Install dependencies:

```bash
pip install -r frontend/requirements.txt
```

3. Start the Streamlit app (backend must be running at http://127.0.0.1:8000):

```bash
set DEEPSEARCHER_BACKEND=http://127.0.0.1:8000
streamlit run frontend/streamlit_app.py --server.port 8501
```

Notes:

- The app uses `DEEPSEARCHER_BACKEND` environment variable to locate the API.
- Uploads are posted to `/upload` endpoint as multipart form-data.
- If your Gemini model is quota-limited, endpoints will return descriptive errors.

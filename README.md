# JobFinder

JobFinder is an intelligent job search and ranking application that leverages AI to match candidates with relevant job opportunities. It parses resumes, generates optimized titles, and ranks jobs based on user preferences.

## Features

- AI-powered job search and ranking
- Resume parsing and analysis
- Title generation for improved job matching
- Streamlit web interface
- Modular agent-based architecture

## Folder Structure

```
JobFinder-main/
│
├── main.py                # Entry point for the application
├── streamlit_app.py       # Streamlit web app
├── requirements.txt       # Python dependencies
├── utils.py               # Utility functions
│
├── agents/                # Core AI agents
│   ├── job_search.py
│   ├── ranker.py
│   ├── resume_parser.py
│   └── title_generator.py
│
├── api/                   # API routes
│   ├── __init__.py
│   └── routes.py
│
├── models/                # Data models
│   └── job_model.py
│
├── tests/                 # Unit tests
│   ├── test_job_search.py
│   ├── test_ranker.py
│   ├── test_resumeparser.py
│   └── test_title_generator.py
└── README.md
```

## Installation

1. Clone the repository:
   ```powershell
   git clone https://github.com/yourusername/JobFinder-main.git
   cd JobFinder-main
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

- To run the Streamlit app:
  ```powershell
  streamlit run streamlit_app.py
  ```

- To run the main script:
  ```powershell
  python main.py
  ```

## API

The API is defined in the `api/routes.py` file. You can extend or modify endpoints as needed.

## Testing

Run unit tests using:
```powershell
python -m unittest discover tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License

This project is licensed under the MIT License.

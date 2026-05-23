# Contributing

Thanks for your interest in this teaching project. The goal of the repo is to keep a small, readable example of a Streamlit plus LangChain CSV chat app. Contributions that keep it simple and easy to learn from are most welcome.


## Before you start

- Read the existing `README.md` to understand what the app does.
- Read `docs/architecture.md` for a short tour of how the pieces fit together.
- Read `SECURITY.md` so you understand the trust model of the pandas agent.

If you are unsure whether a change fits the spirit of the project, please open an issue first to discuss it.


## Local setup

```bash
# 1. Clone
git clone https://github.com/ANI-IN/Hello-Agent.git
cd Hello-Agent

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # macOS or Linux
# venv\Scripts\activate          # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your OpenAI key
cp .env.example .env
# edit .env and put your real key in OPENAI_API_KEY=...

# 5. Run the app
streamlit run app.py
```

You can also run the app in Docker:

```bash
docker build -t chat-with-csv .
docker run --rm -p 8501:8501 -e OPENAI_API_KEY=sk-... chat-with-csv
```


## How to propose a change

1. Open an issue describing the change. For tiny fixes (typos, broken links) you can skip straight to a pull request.
2. Fork the repo and create a branch from `main`. Use a short, descriptive branch name, for example `feat/sample-csv-hr-policies` or `fix/csv-parse-error`.
3. Make your change. Keep it focused, one logical change per pull request.
4. If the change touches `app.py`, run it locally with at least one of the sample CSV files and confirm the app still answers a basic question.
5. Open a pull request against `main`. In the description, explain what you changed and why.


## Style guide

This is a small Python project, so the conventions are light:

- Follow PEP 8 for formatting. `black .` is fine to use.
- Keep functions short and named for what they do.
- Avoid adding heavy dependencies. The project is intentionally lean.
- Do not commit secrets. The `.gitignore` already excludes `.env`, but please double-check.
- Use plain ASCII punctuation in code and docs. Straight quotes, normal hyphens. No smart quotes, no long dashes.


## Sample CSVs

If you add a new sample CSV, please:

- Keep it small (a handful of rows is enough for teaching).
- Use only synthetic, non-personal data.
- Document the columns at the top of the file or in a short note in your pull request.


## What is out of scope

To keep the project a clear teaching example, the following changes are unlikely to be accepted:

- Adding a vector store or full retrieval-augmented-generation pipeline. There are other tutorials for that.
- Adding a database. The whole point is to read CSVs.
- Large refactors that split the app into many files. The single-file layout is intentional.

Improvements that make the app safer, clearer, or easier for a learner to follow are always welcome.


## Reporting bugs

Open an issue with:

- What you did
- What you expected to happen
- What actually happened
- Any error messages, ideally as text rather than screenshots
- Your Python version and operating system

For security issues, please follow `SECURITY.md` and do not open a public issue.


## License

By contributing you agree that your contribution will be licensed under the MIT License, the same license as the rest of the project (see `LICENSE`).

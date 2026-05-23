# Security Policy

This is a small teaching project, not production software. Please read the notes below before you deploy it or run it on data you do not control.


## Reporting a vulnerability

If you find a security issue, please do not open a public GitHub issue.

- Open a private security advisory on GitHub: https://github.com/ANI-IN/Hello-Agent/security/advisories/new
- Or email the maintainer privately at the address on the GitHub profile https://github.com/ANI-IN

Please include:

- A short description of the issue
- Steps to reproduce
- The version (commit hash) you tested against
- Your assessment of the impact

You should expect an acknowledgement within a few days. There is no formal SLA on fixes, since this is a personal teaching repository.


## Known risk areas you should be aware of

These are documented so that anyone using or extending the app understands the trust model.

### 1. The pandas DataFrame agent executes Python on your machine

`app.py` uses `create_pandas_dataframe_agent(..., allow_dangerous_code=True)` from `langchain_experimental`. That agent gives the language model a Python REPL with the loaded DataFrames in scope. The model can, in principle, be steered (by a crafty user question, or by instructions embedded in a CSV cell) to run code beyond pandas, including reading files or making network calls.

What this means in practice:

- Only run the app locally, on data you trust.
- Do not host this app on the open internet without sandboxing the Python execution.
- Be cautious with CSV files from unknown sources.

### 2. The OpenAI API key is read from a sidebar text input

The key is masked in the UI but held in the Streamlit session and passed to the OpenAI client. Do not paste your key on a shared or untrusted machine. Prefer the `OPENAI_API_KEY` environment variable (see `.env.example`) on your own machine.

### 3. Dependencies are not pinned

`requirements.txt` lists package names without version pins. A fresh install may pull newer versions than the ones the project was tested with. If reproducibility matters to you, generate a lock file with `pip-compile` (from `pip-tools`).


## Supported versions

Only the latest commit on `main` is supported. There are no released versions.

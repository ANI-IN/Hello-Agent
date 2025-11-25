# Chat With Your CSV  
A Streamlit and LangChain Tutorial

This document explains everything you need to run and understand the project.  
It covers setup, how the app works, and how to use it with your own CSV files.



## 1. Project Overview

This project is a simple web app that lets you talk to your CSV files in normal language.

You can

* Upload one or many CSV files through a Streamlit user interface  
* Ask questions in normal language such as  
  * What is the return policy  
  * How long does standard shipping take
  * What does the extended warranty cover  
  * Show complaints about delivery
* Get answers from the actual data in the CSV files, not from general knowledge

The app uses

* Streamlit for the user interface  
* Pandas to load and work with CSV data  
* LangChain to create a data frame agent  
* OpenAI chat model to reason about the data and answer questions

The goal is to keep the project simple and easy to understand  
There is no vector database and no advanced retrieval  
The model uses the LangChain data frame agent to inspect the data and reply from it


## 2. Technology Stack

The project uses the following main tools and libraries

* Python  
* Streamlit for the web app  
* Pandas for CSV handling  
* LangChain core package  
* LangChain OpenAI integration  
* LangChain experimental agents for data frame agent support  
* OpenAI chat model (for example gpt 4o mini)  
* Tabulate library for neat table formatting in the background

Python packages are listed in `requirements.txt`:

```txt
streamlit
pandas
langchain
langchain-openai
langchain-experimental
openai
tabulate
````

## 3. Folder Structure

You can keep the project in a simple folder such as

```text
chat-with-csv/
  app.py
  requirements.txt
  credit_card_terms.csv
  ecommerce_faqs.csv
  hospital_policy.csv
  saas_docs.csv
  README.md
```

You can add more CSV files to test other use cases


## 4. Prerequisites

Before you install and run the project, make sure you have

* Python 3.13 or later
* pip to install Python packages
* A valid OpenAI API key

You do not need any database or extra storage


## 5. Installation

Follow these steps in order

### 5.1 Clone or create the project folder

If you already have the files, place them in a folder
If you use git, you can clone your own repository

```bash
mkdir chat-with-csv
cd chat-with-csv
# copy app.py, requirements.txt and CSV files into this folder
```

### 5.2 Create a virtual environment (recommended)

On most systems you can do

```bash
python -m venv venv
```

Activate the environment

On Windows

```bash
venv\Scripts\activate
```

On macOS or Linux

```bash
source venv/bin/activate
```

### 5.3 Install dependencies

Run

```bash
pip install -r requirements.txt
```

This installs Streamlit, Pandas, LangChain and OpenAI related packages


## 6. OpenAI API Key Setup

There are two options

### Option 1 use the text box in the sidebar

The current app already asks for the OpenAI API key in the sidebar

* Start the app
* Go to the left sidebar
* Paste your OpenAI API key in the field
* The key is used only in your session by the app

This is the simplest way and matches the current `app.py` file

### Option 2 set an environment variable (optional)

If you prefer not to paste the key each time, you can export it as an environment variable

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Then you can change the code to read from the environment
At the moment the code reads it from the Streamlit sidebar, so this is optional


## 7. Running the App

Once you have installed the dependencies and prepared your API key

1. Make sure your virtual environment is active

2. In the project folder run

   ```bash
   streamlit run app.py
   ```

3. Streamlit will start a local server and open a browser window
   Usually the address looks like `http://localhost:8501`

You should see

* A sidebar with configuration and instructions
* A main page with the title `Chat with your CSVs (natural language)`
* A file upload area
* A text box for your questions


## 8. Understanding `app.py` Step by Step

This section explains what the main script does

### 8.1 Page configuration

```python
st.set_page_config(page_title="Chat with CSV", page_icon="📊", layout="wide")
```
This line sets the title, emoji icon and layout for the Streamlit page

### 8.2 Sidebar layout

Inside the sidebar the app

* Shows a small icon
* Displays a title
* Asks the user for the OpenAI API key
* Shows a small description of the technology stack
* Shows basic instructions

Key part

```python
openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password",
    help="Enter your OpenAI API key here."
)
```

If the user does not enter a key, the app cannot call the OpenAI model

### 8.3 Main title and description

```python
st.title("📊 Chat with your CSVs (natural language)")
st.write(
    "Upload CSV files and ask questions in normal language. "
    "The AI will look inside the tables and answer using the actual data."
)
```

This tells the user what the app does

### 8.4 File uploader

```python
uploaded_files = st.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)
```

The user can upload one or many CSV files at the same time
Each uploaded file is read into a Pandas data frame later

### 8.5 Reading the CSV files

If both `uploaded_files` and `openai_api_key` are present, the app

* Loops through each uploaded file
* Reads it into a Pandas data frame
* Shows the first three rows of each data frame in a separate column

```python
for i, file in enumerate(uploaded_files):
    df = pd.read_csv(file)
    dfs.append(df)
    df_names.append(file.name)

    with cols[i % len(cols)]:
        st.write(f"**{file.name}**")
        st.dataframe(df.head(3))
```

This gives a quick preview so the user knows which files were loaded

### 8.6 Building a summary of the data frames

The app prepares a short summary that lists each file and its first few column names

```python
summaries = []
for name, df in zip(df_names, dfs):
    cols_sample = [str(c) for c in df.columns[:15]]
    summaries.append(f"- File: '{name}' | Columns: {', '.join(cols_sample)}")
df_summary_text = "\n".join(summaries)
```

This text is passed into the system prompt so the model knows which columns exist in which file

### 8.7 System prompt for strict data use

The app builds a very clear instruction block called `system_prompt`

This prompt tells the model

* Always inspect the data frames using Pandas before answering
* Never answer from general knowledge
* Never answer with phrases such as “it is in column X”
* For text questions

  * Search string columns for relevant rows
  * If a column named Answer, Policy, Description or similar exists, use it as the main answer
  * Return cell text from the best matching row or rows
* For numeric questions

  * Use Pandas operations such as sum, mean, groupby and similar
* Answer in plain English and quote real values from the data

This is the heart of the logic
It keeps the model honest and tied to the CSV files

### 8.8 Creating the LangChain data frame agent

```python
llm = ChatOpenAI(
    temperature=0.0,
    model="gpt-4o-mini",
    openai_api_key=openai_api_key
)

agent = create_pandas_dataframe_agent(
    llm,
    dfs,
    verbose=True,
    agent_type="openai-functions",
    allow_dangerous_code=True
)
```

Explanation

* `ChatOpenAI` creates an OpenAI chat model client
* `create_pandas_dataframe_agent` wraps this model in an agent that knows how to work with Pandas data frames
* The list `dfs` contains all data frames created from the uploaded CSV files
* `verbose=True` lets you see intermediate agent logs in the Streamlit terminal
* `agent_type="openai-functions"` uses the OpenAI function style agent for safer call structure

### 8.9 Question input and answer step

The user types a question

```python
user_question = st.text_input(
    "Example: 'what is the return policy', 'total sales for 2023', 'show all delayed shipments'"
)
```

When the user submits a question

* The app concatenates the system prompt and the user question into `final_query`
* It sends this query to the agent
* The agent uses the model plus Pandas tools to inspect the data frames and returns an answer

```python
final_query = (
    system_prompt
    + "\n\nNow answer this question using the DataFrames only:\n"
    + user_question
)
response = agent.run(final_query)
```

The answer is displayed as Markdown in the app

If something breaks, the app shows an error message using `st.error`


## 9. Sample CSV Files Provided


9.1 `credit_card_terms.csv`

9.2 `ecommerce_faqs.csv`

9.3 `hospital_policy.csv`

9.4 `saas_docs.csv`



## 10. How to Use the App Step by Step

1. Start the app with `streamlit run app.py`
2. In the sidebar paste your OpenAI API key
3. Use the upload area to select one or more CSV files
   
   3.1 You can use the provided sample files or your own
4. Check the preview tables to confirm that the data loaded correctly
5. Scroll down to the question box
6. Type a question in normal language

   * For example

     * “What is the return policy for electronics”
     * “Explain the foreign transaction fee for all cards”
     * “What does the extended warranty cover”
7. Press Enter
8. Wait for the spinner to finish
9. Read the AI response under “AI Response”

If the question matches the data properly, the answer will quote the real cell values
If the agent cannot find anything, it may explain that no matching rows were found


## 11. Customization Ideas

You can extend the project in many ways

* Add more CSV files for other domains such as HR policies, company internal FAQs or product catalogs
* Change the system prompt to enforce a different style of answer
* Switch to a different OpenAI model by changing the `model` parameter in `ChatOpenAI`
* Add caching or logging of questions and answers
* Add file type filters to group certain CSV files by domain

All of these changes can be done inside `app.py`


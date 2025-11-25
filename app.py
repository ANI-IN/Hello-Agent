import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 1. Page Configuration
st.set_page_config(page_title="Chat with CSV", page_icon="📊", layout="wide")

# 2. Sidebar for Setup
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2814/2814668.png", width=50)
    st.title("Configuration")
    
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key here."
    )
    
    st.markdown("---")
    st.markdown("### Technology Stack")
    st.markdown("- Streamlit\n- LangChain\n- OpenAI")
    st.markdown("### Instructions")
    st.markdown(
        """
        - Upload one or more CSV files.
        - Ask in normal language, e.g.:
          - "what is the return policy"
          - "how much did we sell last month"
          - "show complaints about delivery"
        """
    )

# 3. Main Interface
st.title("📊 Chat with your CSVs (natural language)")
st.write(
    "Upload CSV files and ask questions in normal language. "
    "The AI will look inside the tables and answer using the actual data."
)

# 4. File Uploader
uploaded_files = st.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files and openai_api_key:
    dfs = []
    df_names = []

    st.write(f"### Loaded {len(uploaded_files)} CSV file(s):")
    cols = st.columns(len(uploaded_files))

    for i, file in enumerate(uploaded_files):
        df = pd.read_csv(file)
        dfs.append(df)
        df_names.append(file.name)

        with cols[i % len(cols)]:
            st.write(f"**{file.name}**")
            st.dataframe(df.head(3))

    # Build a small summary of dataframes for the model
    summaries = []
    for name, df in zip(df_names, dfs):
        cols_sample = [str(c) for c in df.columns[:15]]
        summaries.append(f"- File: '{name}' | Columns: {', '.join(cols_sample)}")
    df_summary_text = "\n".join(summaries)

    # SYSTEM PROMPT: force the model to actually read and return values
    system_prompt = f"""
You are a strict data assistant working with one or more pandas DataFrames.

GENERAL RULES
- You MUST always inspect the DataFrames using Python / pandas before answering.
- You are NOT allowed to answer from general knowledge or guesses.
- Never respond with "you can find it in column X" or "it is stored in the dataframe".
- Always return the actual values from the DataFrame.

TEXT QUESTIONS (FAQs / policies, etc.)
- For questions like "what is the return policy" or "what is the warranty", do this:
  1. Look through all object/string columns for relevant rows
     (for example using df[col].str.contains(keyword, case=False, na=False)).
  2. If there is a column named 'Answer', 'Policy', 'Description', 'Details'
     or similar, treat that as the main answer column.
  3. Return the cell text from the most relevant row(s).
  4. If multiple rows are relevant, list them clearly (e.g. bullet points).

NUMERIC QUESTIONS
- For numeric questions (totals, counts, averages, etc.), use pandas operations
  on the numeric columns (sum, mean, groupby, etc.) and give the computed result.

ABOUT THE DATA
The following DataFrames are loaded from CSV files:
{df_summary_text}

ANSWER STYLE
- Answer in plain English.
- Quote the actual text or numbers from the DataFrame.
- Only mention file/column names briefly if helpful.
    """.strip()

    try:
        # 5. LLM and Agent
        llm = ChatOpenAI(
            temperature=0.0,
            model="gpt-4o-mini",        # or "gpt-3.5-turbo" if you prefer
            openai_api_key=openai_api_key
        )

        agent = create_pandas_dataframe_agent(
            llm,
            dfs,
            verbose=True,
            agent_type="openai-functions",
            allow_dangerous_code=True
        )

        st.markdown("---")
        st.subheader("Ask a question in normal language")

        user_question = st.text_input(
            "Example: 'what is the return policy', 'total sales for 2023', 'show all delayed shipments'"
        )

        if user_question:
            with st.spinner("Reading your CSVs and answering from the data..."):
                try:
                    # IMPORTANT: we prepend a short, very direct instruction to the question
                    final_query = (
                        system_prompt
                        + "\n\nNow answer this question using the DataFrames only:\n"
                        + user_question
                    )
                    response = agent.run(final_query)

                    st.success("Analysis complete!")
                    st.write("### AI Response:")
                    st.markdown(response)

                except Exception as e:
                    st.error(f"Error while answering: {e}")

    except Exception as e:
        st.error(f"Error initializing the AI agent: {e}")

elif not openai_api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to proceed.")
else:
    st.info("Please upload your CSV files to start.")

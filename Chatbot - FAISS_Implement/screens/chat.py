import streamlit as st
from utils.query import run_similarity_search, query_ollama
from utils.database import load_data_from_snowflake, save_preferences
from utils.planner import display_preference_based_recommendations

def screen_2():
    st.title("🧚‍♀️Chat with the Fairy")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "remaining_recs" not in st.session_state:
        st.session_state.remaining_recs = []
    if "feedback" not in st.session_state:
        st.session_state.feedback = {"disliked": set()}
    
    user_location = st.text_input("📍Where are you located?", placeholder="e.g., Florida")
    user_message = st.chat_input("What are you looking for?")

    if not user_location:
        st.info("Please enter your location to start.")
        return

    if user_message:
        st.chat_message("user").markdown(user_message)
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        if any(x in user_message.lower() for x in ["not a fan", "don't like", "dislike", "another one", "next"]):
            if st.session_state.remaining_recs:
                next_suggestion = st.session_state.remaining_recs.pop(0)
                st.session_state.feedback["disliked"].update(
                    map(str.strip, next_suggestion['CATEGORIES'].lower().split(","))
                )

                next_prompt = f"""
                You are Street Fairy 🧚‍♀️. The last place wasn't quite right.
                Here's another nearby business:
                - {next_suggestion['NAME']} ({next_suggestion['CATEGORIES']}, {next_suggestion.get('CITY', '')}, {next_suggestion['STATE']})
                Describe what makes it special.
                """
                response = query_ollama(next_prompt, model="mistral")
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                return

        df = load_data_from_snowflake()
        results = run_similarity_search(user_location, query_input=user_message, df=df)
        st.session_state["last_results"] = results  # Store full result set

        if results.empty:
            st.chat_message("assistant").warning("⚠️ No results found. Try asking differently.")
            return

        top_result = results.iloc[0]
        st.session_state.remaining_recs = results.iloc[1:].to_dict(orient="records")

        business_str = f"- {top_result['NAME']} ({top_result['CATEGORIES']}, {top_result.get('CITY', '')}, {top_result['STATE']})"

        rec_prompt = f"""
        You are Street Fairy 🧚‍♀️ helping users find places nearby.
        The user asked: "{user_message}"
        Here's a business we found:
        {business_str}
        Describe what makes it special.
        """

        recommendation = query_ollama(rec_prompt, model="mistral")

        with st.chat_message("assistant"):
            st.markdown(recommendation)
            st.markdown("What did you think of this suggestion? You can say something like 'I liked it' or 'Not for me'. ✨")

        st.session_state.chat_history.append({"role": "assistant", "content": recommendation})

    # Capture feedback
    user_feedback = st.text_input("Provide your feedback")
    if user_feedback:
        st.session_state.chat_history.append({"role": "user", "content": user_feedback})
        if "not for me" in user_feedback.lower():
            if st.session_state.remaining_recs:
                next_suggestion = st.session_state.remaining_recs.pop(0)
                next_prompt = f"""
                You are Street Fairy 🧚‍♀️. The last place wasn't quite right.
                Here's another nearby business:
                - {next_suggestion['NAME']} ({next_suggestion['CATEGORIES']}, {next_suggestion['CITY']}, {next_suggestion['STATE']})
                Describe what makes it special.
                """
                next_recommendation = query_ollama(next_prompt, model="mistral")
                with st.chat_message("assistant"):
                    st.markdown(next_recommendation)
                    st.markdown("How about this one?")
                st.session_state.chat_history.append({"role": "assistant", "content": next_recommendation})
                return
        else:
            follow_up_prompt = "How else can I assist you today?"
            follow_up_response = query_ollama(follow_up_prompt, model="mistral")
            with st.chat_message("assistant"):
                st.markdown(follow_up_response)
            st.session_state.chat_history.append({"role": "assistant", "content": follow_up_response})

    # Show preference-based recommendations
    st.session_state["user_location"] = user_location
    display_preference_based_recommendations()

    # Show all assistant messages so far
    if "chat_history" in st.session_state and st.session_state.chat_history:
        with st.expander("📝 View All Assistant Messages So Far"):
            for entry in st.session_state.chat_history:
                if entry["role"] == "assistant":
                    st.markdown(entry["content"])

    # Show full result set for reference
    if "last_results" in st.session_state:
        with st.expander("📊 Businesses Considered"):
            st.dataframe(st.session_state["last_results"][["NAME", "CATEGORIES", "CITY", "STATE"]])

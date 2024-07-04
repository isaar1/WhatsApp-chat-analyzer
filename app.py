import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📁 Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Show analysis for", user_list)

    if st.sidebar.button("📈 Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("📊 Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("💬 Total Messages")
            st.title(num_messages)
        with col2:
            st.header("📝 Total Words")
            st.title(words)
        with col3:
            st.header("📷 Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("🔗 Links Shared")
            st.title(num_links)

        # Monthly Timeline
        st.title("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        ax.set_xlabel("Time")
        ax.set_ylabel("Number of Messages")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("📅 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Messages")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('📈 Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("📅 Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            ax.set_xlabel("Day")
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("📅 Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            ax.set_xlabel("Month")
            ax.set_ylabel("Number of Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("📅 Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap="YlGnBu")
        ax.set_xlabel("Period")
        ax.set_ylabel("Day")
        st.pyplot(fig)

        # Finding the busiest users in the group (Group level)
        if selected_user == 'Overall':
            st.title('👥 Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                ax.set_xlabel("Users")
                ax.set_ylabel("Number of Messages")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("☁️ Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        # Most Common Words
        st.title("🔠 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='blue')
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Words")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.title("😊 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f%%", colors=sns.color_palette("hsv", len(emoji_df)))
            st.pyplot(fig)

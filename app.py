import streamlit as st
import requests

# Streamlit app
def main():
    st.title("AI Blog Content Generator")

    # Sidebar inputs
    st.sidebar.header("Configure Blog Settings")

    # Define the API endpoints
    api_url ="https://dash-inc-blog-gen-backend.hf.space/generate_blog/"
    
    download_url ="https://dash-inc-blog-gen-backend.hf.space/download/"

    # Input fields for blog generation parameters
    blog_type = st.sidebar.selectbox("Type of Blog", ["How to", "Listicle", "Guide", "Review"])
    target_audience = st.sidebar.text_input("Target Audience", "Parents")
    tone = st.sidebar.selectbox("Tone", ["Informative", "Casual", "Formal", "Humorous"])
    point_of_view = st.sidebar.selectbox("Point of View", ["First-person", "Second-person", "Third-person"])
    target_country = st.sidebar.text_input("Target Country", "US")
    keywords = st.sidebar.text_area("Keywords (comma-separated)", "child development, parenting tips, educational activities")
    category = st.sidebar.text_area("Categories (comma-separated)", "Parenting, Child Development")  # Input for categories
    subheadings = st.sidebar.number_input("Number of Subheadings", min_value=1, max_value=10, value=3, step=1)  # Input for subheadings

    # Convert comma-separated keywords and categories to lists
    keywords_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
    category_list = [cat.strip() for cat in category.split(",") if cat.strip()]  # Convert category input to list

    # Button to send the request
    if st.sidebar.button("Generate Blog"):
        # Create the payload based on user inputs
        payload = {
            "TypeOf": blog_type,
            "target_audience": target_audience,
            "tone": tone,
            "point_of_view": point_of_view,
            "target_country": target_country,
            "keywords": keywords_list,
            "category": category_list,  # Pass category as a list of strings
            "subheadings": subheadings  # Pass number of subheadings
        }

        # Show a spinner while the request is being processed
        with st.spinner("Generating blog content... Please wait..."):
            try:
                # Send a POST request to the FastAPI server
                response = requests.post(api_url, json=payload)
                response.raise_for_status()  # Check for HTTP errors

                # Parse the response
                response_data = response.json()
                st.success("Blog generated successfully!")
                st.json(response_data)

                # Retrieve the blog title and download link
                blog_title = response_data.get("title")
                file_path = response_data.get("file_path")  # Added for clarity if the API includes it

                if blog_title:
                    # Provide download button and link
                    download_link = f"{download_url}?title={blog_title}"
                    st.markdown(
                        f"""
                        ### 🎉 Your blog is ready!
                        - **Title**: {blog_title}
                        - [📄 Download Blog Document]({download_link})
                        """,
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        label="Download Blog Document",
                        data=requests.get(download_link).content,  # Fetch content for download
                        file_name=f"{blog_title}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                else:
                    st.warning("Blog title not provided in response. Unable to generate download link.")

            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while generating the blog: {e}")

    # Display information about the app
    st.sidebar.info(
        """
        This app uses AI to generate blog content. 
        Fill in the details in the sidebar and click 'Generate Blog' to create and download your blog.
        """
    )

# Run the app
if __name__ == "__main__":
    main()

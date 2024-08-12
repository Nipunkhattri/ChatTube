# ChatTube

ChatTube is a project that allows users to input a YouTube link, preprocess the video, and query the content of the video using advanced AI technologies. You can ask any question about the video, and ChatTube will provide relevant answers based on the video's content.

## Features

- **YouTube Link Processing**: Input a YouTube link, and the video will be preprocessed for further analysis.
- **Query the Video**: Ask any question related to the video's content and get accurate responses.
- **Generative AI Integration**: Leverage state-of-the-art AI models to understand and respond to queries about the video.
- **Accessibility for Deaf Users**: Provide video data in accessible formats such as subtitles or transcripts, allowing deaf users to access video content effectively.
- **Enhanced Productivity**: Streamline the process of obtaining video information to save time and increase productivity.

![ChatTube](assests/Image.png)

## Tech Stack

- **llamaIndex**: For indexing and querying the video data.
- **ChromaDB**: For managing and querying vector data efficiently.
- **Streamlit**: For building the interactive web interface.
- **Generative AI**: For understanding and generating responses based on the video content.

## Getting Started

To get started with ChatTube, follow these steps:

### Prerequisites

- Python 3.7 or later
- `pip` (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Nipunkhattri/ChatTube.git

2. Navigate to the project directory:

   ```bash
   cd ChatTube
   
3. Install of the packages

   ```bash
   pip install -r requirements.txt
   
4. Run The Streamlit app
   ```bash
   streamlit run app.py

### Thank you for using ChatTube! We hope you find it useful for exploring and querying YouTube videos.
# Career Craft

## Description
This is an GenAI app to assist you in carfting a good resume, cover-letters for a particular job.

## Project Setup 
1. Need to install docker. [installation guidelines
](https://docs.docker.com/engine/install/)

2. Need to install langgraph studio. [installation guidelines](https://github.com/langchain-ai/langgraph-studio)

3. Configure `gcloud` on your system and make sure you have generated the credentials file: `application_default_credentials.json` file.

    Refer: [gcloud default login](https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login)

4. Clone this repository:

    `git clone https://github.com/CyberKnight1803/career-craft`

5. Set up .env file 
   ```
    PP_OPENAI_API_KEY=
    OPENAI_API_KEY=
    LANGCHAIN_TRACING_V2=
    LANGCHAIN_ENDPOINT=
    LANGCHAIN_API_KEY=
    LANGCHAIN_PROJECT=

    GOOGLE_CLOUD_PROJECT=
    SECRET_VERSION=
    GOOGLE_APPLICATION_CREDENTIALS=
    SERVICE_ACCOUNT=
   ```

6. Make sure docker desktop is on. 

7. Open LangGraph Studio and select this project

8. LangGraph Studio will automatically create an image, fire up a contiainer and launch the project for you (locally).

## Usage 




## Troubleshooting
If any error occurs, the first point of debugging should be checking the logs in LangGraph Studio, from there on you can navigate through the source code and figure out the root cause!
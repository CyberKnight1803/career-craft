# Career Craft

## Description
This is an GenAI app to assist you in crafting a good resume, cover-letters for a particular job.

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

<img width="1512" alt="Screenshot 2024-12-17 at 7 10 06 PM" src="https://github.com/user-attachments/assets/7f2ff56b-fdad-45c5-9d67-491bee00c464" />


<img width="1512" alt="Screenshot 2024-12-17 at 7 15 31 PM" src="https://github.com/user-attachments/assets/c5c18285-19c6-4f33-bd27-04cd84459cae" />


<img width="1508" alt="Screenshot 2024-12-17 at 7 16 00 PM" src="https://github.com/user-attachments/assets/1d9a7bb6-9556-41d5-8869-0271ff1b992d" />



## Troubleshooting
If you encounter any issues while running the application, follow these steps:

1. Check the Logs:
    * Access logs from LangGraph Studio's dashboard to identify the root cause.

2. Verify Environment Variables:
    * Ensure the .env file is correctly configured with all required credentials.

3. Docker Container Issues:
    * Restart Docker Desktop and relaunch LangGraph Studio.

4. Credential Problems:
    * Ensure Google Cloud credentials (application_default_credentials.json) are valid and the path is correctly set.

5. General Debugging:
    * Navigate through the source code to debug specific issues.

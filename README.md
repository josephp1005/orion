# orion
Repo for Orion project @ HackGT 12

# Quickstart

You must have Gemini API key in your ```.env```. Additionally, if you wish to use Slack and Github features, add the relevant keys to ```.env```.

1. Install [ollama](https://ollama.com/) for embeddings
2. ```
   ollama pull nomic-embed-text
   ```
3. ```
   git clone https://github.com/josephp1005/orion.git
   ```
4. ```
   pip install -r requirements.txt
   ```
5. ```
   cd local_scripts
   ```
6. ```
   chmod +x local_kill.sh
   ```
7. ```
   ./local_kill.sh
   ```
8. ```
   chmod +x local_setup.sh
   ```
9. ```
    ./local_setup.sh
    ```

Your current terminal is now running ollama, and will show any requests made to ollama. To continue with the next steps, keep this terminal running and open a new terminal window. Navigate to the directory where the cloned repository is located.

10. Upload pdfs to the data directory. 
11. ```
    python dense_embeddings.py
    ```
12. ```
    python sparse_embedding.py
    ```
    
If all of the above was done properly, you can now run:

```
python answer.py <query>
```

where \<query\> is your question.

Now run Flask app on separate terminal.
12. ```
    python app.py
    ```
Finally run the React app on a separate terminal
13. ```
    cd ui
    ```
14. ```
    npm install
    ```
15. ```
    npm run dev
    ```

# Slack
1. Run orion-slack.py to poll slack and update dense
2. Currently would need to manually update sparse

# Terminal
1. You can do it from any directory, but need to run the script oterm/oterm.sh
2. Once done capturing commands, do exit; will update dense
3. Again would need to manually update sparse

# Github
1. Simlar to Slack, run ./run_fetch_prs.sh

# Common Issues
1. If you delete the ChromaDB, make sure you also delete sparse embeddings pickle file.
2. Need to run Flask App and UI for things to work

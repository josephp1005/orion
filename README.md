# orion
Repo for Orion project @ HackGT 12

# Quickstart

### Running locally on MacOS

1. Install [ollama](https://ollama.com/)
2. ```
   ollama pull nomic-embed-text
   ```
3. ```
   ollama pull llama3
   ```
4. ```
   git clone https://github.com/josephp1005/orion.git
   ```
5. ```
   cd local_scripts
   ```
6. ```
   pip install -r requirements.txt
   ```
7. ```
   chmod +x local_kill.sh
   ```
8. ```
   ./local_kill.sh
   ```
9. ```
   chmod +x local_setup.sh
   ```
10. ```
    ./local_setup.sh
    ```
    
Note that if it says "address already in use", that (likely) means ollama is already running. From the Mac taskbar, you can always quit ollama so you can start and stop from command line. Make sure to run step 12 again if you do this.

![image](https://github.com/AD1616/HPC-Training-AI/assets/64157584/2547e651-3ee8-47bf-ba83-4e4eca0764e9)

Your current terminal is now running ollama, and will show any requests made to ollama. To continue with the next steps, keep this terminal running and open a new terminal window. Navigate to the directory where the cloned repository is located.

11. Upload pdfs to the data directory. 
12. ```
    python dense_embeddings.py
    ```
13. ```
    python sparse_embedding.py
    ```
    
If all of the above was done properly, you can now run:

```
python answer.py <query>
```

where \<query\> is your question.

```
python query.py "Some query relevant to your documents." 
```

When finished, run:

```
./local_scripts/kill.sh
```

### Running after initial setup

1. Upload pdfs to the data directory. 
2. ```
   ./local_scripts/start.sh
   ```
3. ```
   python query.py "Some query relevant to your documents." 
   ```
4. ```
   ./local_scripts/kill.sh
   ```

# Usage with slack
1.```
  python orion-test-slack.py
  ```
2. ```
   python dense_embeddings.py
   ```
3. ```
   python sparse_embedding.py
   ```


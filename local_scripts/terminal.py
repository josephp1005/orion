import subprocess
import sqlite3
import datetime
import os
import sys

class TerminalRunner:
    def __init__(self, db_path="command_history.db"):
        self.db_path = db_path
        self.current_dir = os.getcwd()  # Track current working directory
        self.setup_database()
    
    def setup_database(self):
        """Initialize the database with command history table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                output TEXT,
                error TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                exit_code INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    
    def store_command(self, command, output, error, exit_code):
        """Store command execution details in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO command_history (command, output, error, exit_code)
            VALUES (?, ?, ?, ?)
        ''', (command, output, error, exit_code))
        conn.commit()
        conn.close()
    
    def execute_command(self, command):
        """Execute command and return output, error, and exit code"""
        try:
            # Handle cd command specially
            if command.strip().startswith('cd '):
                return self.handle_cd_command(command.strip())
            elif command.strip() == 'cd':
                return self.handle_cd_command('cd ~')
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.current_dir  # Use current directory as working directory
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out after 30 seconds", -1
        except Exception as e:
            return "", f"Error executing command: {str(e)}", -1
    
    def handle_cd_command(self, command):
        """Handle cd command to change current directory"""
        try:
            # Extract path from cd command
            parts = command.split(' ', 1)
            if len(parts) == 1:
                # Just 'cd' - go to home directory
                new_path = os.path.expanduser('~')
            else:
                path = parts[1].strip()
                if path == '~':
                    new_path = os.path.expanduser('~')
                elif os.path.isabs(path):
                    new_path = path
                else:
                    new_path = os.path.join(self.current_dir, path)
            
            # Resolve the path and check if it exists
            new_path = os.path.abspath(new_path)
            if os.path.isdir(new_path):
                self.current_dir = new_path
                return f"Changed directory to: {self.current_dir}", "", 0
            else:
                return "", f"cd: no such file or directory: {parts[1] if len(parts) > 1 else '~'}", 1
                
        except Exception as e:
            return "", f"cd: {str(e)}", 1
    
    def run(self):
        """Main loop for continuous command execution"""
        print("Terminal Command Runner")
        print("Type 'exit' or 'quit' to stop")
        print("Type 'history' to view recent commands")
        print("Type 'pwd' to see current directory")
        print("-" * 40)
        
        while True:
            try:
                # Show current directory in prompt
                prompt = f"{os.path.basename(self.current_dir)}$ "
                command = input(prompt).strip()
                
                # Handle special commands
                if command.lower() in ['exit', 'quit', 'e', 'q']:
                    print("Goodbye!")
                    break
                
                if command.lower() == 'history':
                    self.show_history()
                    continue
                
                if command.lower() == 'pwd':
                    print(self.current_dir)
                    continue
                
                if not command:
                    continue
                
                # Execute the command
                print(f"Executing: {command}")
                output, error, exit_code = self.execute_command(command)
                
                # Display output
                if output:
                    print("Output:")
                    print(output)
                
                if error:
                    print("Error:")
                    print(error)
                
                # Store in database
                self.store_command(command, output, error, exit_code)
                
                print(f"Exit code: {exit_code}")
                print("-" * 40)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to stop gracefully")
            except Exception as e:
                print(f"Unexpected error: {e}")
    
    def show_history(self, limit=10):
        """Display recent command history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT command, timestamp, exit_code 
            FROM command_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            print("Recent command history:")
            for cmd, timestamp, exit_code in results:
                status = "✓" if exit_code == 0 else "✗"
                print(f"{status} {timestamp}: {cmd}")
        else:
            print("No command history found")

if __name__ == "__main__":
    runner = TerminalRunner()
    runner.run()

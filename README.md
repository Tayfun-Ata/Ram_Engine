**Features**:
- **Password Strength Checker**: Analyze the strength of a password based on length, character diversity, and complexity.
- **Dictionary Attack Simulation**: Use a wordlist to attempt to crack a hashed password.
- **Brute-Force Attack Simulation**: Simulate brute-force attacks with customizable character sets and password lengths.
- **Hash Algorithm Support**: Supports SHA-256 and MD5 hashing algorithms.
- **GUI Interface**: User-friendly interface built with `tkinter` for easy interaction.
- **Configuration Management**: Save and load default paths for Hashcat and wordlists using a configuration file (`config.json`).
- **Logging**: Detailed logs of operations and errors are saved in `ram_engine.log` for debugging and auditing.

**Requirements**:
- Python 3.x
- Hashcat installed and accessible
- A valid wordlist file (e.g., `rockyou.txt`)

**How to Use**:
1. Select the Hashcat executable and wordlist file through the GUI.
2. Enter a password to test its strength or simulate attacks.
3. Choose between dictionary attack or brute-force attack.
4. View results directly in the GUI or check logs for detailed information.

Feel free to modify this description to suit your needs! Let me know if you'd like additional details or adjustments. 

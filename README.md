# AI Folder Organizer

AI Folder Organizer is a machine learning-powered application designed to analyze user patterns and automatically organize files into categories. With an intuitive GUI, it provides a user-friendly experience to streamline folder organization while incorporating intelligent pattern recognition.

---

## Features

- **Machine Learning Integration:** Trains a model to recognize and categorize files based on patterns in file names.
- **Customizable Themes:** Offers light and dark modes for a personalized user experience.
- **Dynamic Learning:** Learns from user-selected directories to refine its organization logic.
- **Progress Visualization:** Displays a progress bar during folder organization.
- **Cross-Platform Support:** Works on Windows, macOS, and Linux.

---

## Prerequisites

### Required Libraries

The project uses the following Python libraries:

- `sklearn`
- `tkinter`
- `ctypes`
- `Pillow`
- `pathlib`
- `shutil`
- `pickle`
- `json`
- `threading`

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/ai-folder-organizer.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ai-folder-organizer
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python gui.py
   ```

---

## Usage

1. **Launch the Application:** Run the `gui.py` file to open the GUI.
2. **Select Folder:** Choose a folder to organize.
3. **Train the Model:** Optionally, add directories for the application to learn patterns from.
4. **Start Organizing:** Click the "Start Organizing" button to begin the process.

---

## Project Structure

- `app.py`: Core logic for machine learning, training, and organization.
- `gui.py`: Graphical User Interface (GUI) implementation using `tkinter`.
- `settings.py`: Handles user settings, including theme preferences.
- `settings.json`: Stores user preferences (e.g., theme).

---

## Contributing

Feel free to fork this repository and make contributions. Submit pull requests with detailed descriptions of your changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Acknowledgments

Special thanks to open-source contributors and libraries that made this project possible.



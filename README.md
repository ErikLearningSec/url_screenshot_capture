
# url_screenshot_capture
# Automated Screenshot Capture and HTML Generation

This Python script automates the capture of screenshots for a list of URLs using Selenium and concurrent threading. The script utilizes the Chrome WebDriver in headless mode for efficiency.

## Dependencies

Make sure you have the following dependencies installed:

- `selenium`
- `concurrent.futures`

You can install them using:

```bash
pip install selenium
```

## Setup

- Chrome WebDriver: Ensure you have the Chrome WebDriver installed and set the path accordingly in the `executable_path` variable at line 12 in the script.
- URL File: Provide a text file containing a list of URLs as the first argument when running the script.
- Output Folder: Screenshots are saved in a folder named
    screenshot\_captured. 

## Usage

Run the script by executing the following command:


```python script\_name.py path/to/url\_file.txt```

## Output

Screenshots will be saved in the screenshot\_captured folder, and an HTML file (screenshots.html) will be generated with links to the captured screenshots.

## Note

Adjust the script according to your needs. Feel free to modify the script parameters such as window\_size, timeout, etc.

## Author

_ **ErikLearningSec** _

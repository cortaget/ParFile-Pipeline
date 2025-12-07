# ParFile Pipeline - Automated File Organizer

A multi-threaded Python application that automatically monitors, sorts, and organizes files by their extensions into categorized folders. Built with a user-friendly GUI and real-time logging capabilities.

## Features

- **Automatic File Monitoring**: Continuously watches a selected folder for new files
- **Recursive Folder Monitoring**: Automatically detects subfolders and monitors their contents
- **Smart Organization**: Sorts files by extension (JPG, PNG, PDF, MP4, etc.) into dedicated folders
- **Multi-threaded Processing**: Parallel file handling with 4 loader and 4 mover threads for optimal performance
- **User-Friendly GUI**: Easy folder selection interface with status indicators
- **Real-time Logging**: Complete activity log with timestamps for all file operations
- **Duplicate Handling**: Automatically renames files with duplicate names
- **Cross-platform Support**: Works on Windows, macOS, and Linux

## Installation & Usage

### Running the Application

1. **Navigate to the `dist` folder**:

2. **Run the application**:
   - **Windows**: Double-click `main.exe`
   - **Linux/Mac**: 
     ```
     ./main
     ```

3. **Select folders**:
   - **Unsorted folder**: Choose the folder to monitor for new files
   - **Folder to sort in**: Choose the destination folder where organized files will be placed

4. **Click "Submit"** to start the automated file organization

5. **Optional actions**:
   - **Read logs**: View detailed operation history
   - **Stop Pipeline**: Safely terminate the application

## How It Works

**Pipeline Architecture:**

1. **Watcher**: Monitors the unsorted folder for new files and subfolders
   - When a subfolder is detected, automatically spawns a sub-watcher for that folder
   - Recursively monitors all nested folders
   - Folders themselves remain untouched - only files are processed
2. **Loader**: Identifies file extensions and creates category folders
3. **Mover**: Physically moves files to their designated folders
4. **Logger**: Records all operations with timestamps

## File Organization Example

**Before:**

Unsorted/
├── photo.jpg
├── document.pdf
├── Projects/
│ ├── report.docx
│ └── Assets/
│ └── logo.png
└── video.mp4

text

**After:**

MySorted/
├── JPG/
│ └── photo.jpg
├── PDF/
│ └── document.pdf
├── MP4/
│ └── video.mp4
├── DOCX/
│ └── report.docx
└── PNG/
└── logo.png

Unsorted/
├── Projects/ (empty folder remains)
│ └── Assets/ (empty folder remains)

text

**Note**: Files from nested folders are extracted and organized by type. Empty folders remain in the source directory.

Click the **"Read logs"** button in the GUI to view the log file.

## Error Handling

- **Permission Errors**: If a file is locked by another program, the error is logged and processing continues
- **Duplicate Names**: Files with identical names are automatically renamed with a counter (e.g., `photo_1.jpg`)
- **Missing Extensions**: Files without extensions are placed in an `UNKNOWN` folder

## Performance

- **Multi-threaded**: 4 parallel loader threads and 4 mover threads
- **Non-blocking GUI**: Interface remains responsive during processing
- **Efficient monitoring**: 1-second polling interval to balance responsiveness and CPU usage
- **Dynamic watchers**: Automatically scales to monitor multiple nested folders

## Troubleshooting

**Application won't start:**
- Ensure you're running `main.exe` from the `dist/` folder
- Check antivirus isn't blocking the executable

**Files not moving:**
- Verify both folders are selected and paths are correct
- Check file permissions in source and destination folders

**High CPU usage:**
- This is normal during active file processing
- CPU usage drops when no new files are detected

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open-source and available for personal and commercial use.

## Author

- Developed by Maxim Mazuret
- [https://github.com/cortaget](https://github.com/cortaget)

---

**Happy organizing! 📁✨**
# CardioAnalysis — ECG & Arrhythmia Dashboard

A web-based dashboard for analyzing ECG (electrocardiogram) data and detecting cardiac arrhythmias using machine learning techniques.

## Overview

CardioAnalysis is an interactive data analysis tool that processes and visualizes ECG signals from multiple cardiac databases. The application provides real-time classification of normal and abnormal heart rhythms, along with comprehensive statistical analysis.

## Features

- **ECG Data Analysis**: Process and visualize ECG signals from the MIT-BIH and PTBDB datasets
- **Arrhythmia Detection**: Classify cardiac arrhythmias (normal vs. abnormal)
- **Interactive Dashboard**: Explore data through multiple tabs and visualizations
- **Statistical Summary**: View key metrics and class distributions
- **Chart Visualization**: Interactive charts powered by Chart.js for data exploration

## System Requirements

- **Web Browser**: Modern browser with JavaScript enabled (Chrome, Firefox, Safari, Edge)
- **Internet Connection**: Required for loading external libraries (Chart.js, Google Fonts)
- **Disk Space**: ~10 MB for datasets and HTML files

## Installation & Setup

### Prerequisites
- No external dependencies or package managers required
- All visualizations are handled client-side in the browser

### Running the Program

#### Option 1: Direct File Opening
1. Navigate to the `FINALS-PROJECT` folder
2. Double-click `index.html` to open in your default web browser
3. The dashboard will load immediately with the data visualization

#### Option 2: Local Web Server (Recommended for best performance)
If you have Python installed:

```bash
# Navigate to the FINALS-PROJECT directory
cd path/to/FINALS-PROJECT

# Python 3
python -m http.server 8000

# Or Python 2
python -m SimpleHTTPServer 8000
```

Then open your browser and navigate to:
```
http://localhost:8000
```

#### Option 3: Using Node.js (if available)
```bash
# Install a simple HTTP server globally
npm install -g http-server

# Navigate to the folder and run
http-server
```

## Project Structure

```
FINALS-PROJECT/
├── index.html              # Main dashboard interface
├── finals-proj.html        # Alternative dashboard view
├── README.md              # This file
│
├── Datasets:
├── mitbih_train.csv       # MIT-BIH training dataset
├── mitbih_test.csv        # MIT-BIH test dataset
├── ptbdb_normal.csv       # PTBDB normal ECG recordings
└── ptbdb_abnormal.csv     # PTBDB abnormal ECG recordings
```

## Dataset Information

### MIT-BIH Arrhythmia Database
- Contains 48 half-hour ECG recordings from 47 subjects
- Sampled at 360 Hz
- Includes various types of arrhythmias
- **Reference**: Moody, G.B., Mark, R.G. (1989). "The PhysioNet QT Database"

### PTBDB (PhysioNet PTB Database)
- Contains 290 records from 209 subjects
- Sampled at 125 Hz
- Includes normal and abnormal cardiac conditions
- **Reference**: Goldberger, A.L., et al. (2000). "PhysioBank, PhysioToolkit, and PhysioNet"

## How to Use

1. **Open the Dashboard**: Launch `index.html` in your browser
2. **Navigate Tabs**: Use the navigation tabs at the top to switch between different analysis views
3. **View Statistics**: Check the stat cards for dataset summary information
4. **Interact with Charts**: Hover over charts for detailed information
5. **Explore Data**: Toggle different classes and arrhythmia types to analyze patterns

## Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Visualization**: Chart.js v4.4.1
- **Styling**: Custom CSS with CSS variables for theming
- **Data Format**: CSV (Comma-Separated Values)
- **Fonts**: Google Fonts (DM Mono, DM Sans)

## Browser Compatibility

- ✅ Google Chrome (latest)
- ✅ Mozilla Firefox (latest)
- ✅ Safari (latest)
- ✅ Microsoft Edge (latest)

## Troubleshooting

### Dashboard won't load
- **Check browser console** for JavaScript errors (F12 → Console tab)
- **Verify all CSV files** are in the same directory as index.html
- **Try a different browser** to rule out browser-specific issues
- **Use a local web server** instead of opening the file directly

### Charts not displaying
- Ensure JavaScript is enabled in your browser settings
- Clear browser cache (Ctrl+Shift+Delete)
- Check that Chart.js CDN is accessible (requires internet connection)

### Data not loading
- Verify CSV files exist in the project directory
- Check file permissions (files should be readable)
- Ensure CSV format is correct (UTF-8 encoding, proper delimiters)

## Future Enhancements

- Machine learning model integration for real-time predictions
- Data upload functionality for custom ECG recordings
- Export analysis results as PDF reports
- Multi-dataset comparison tools
- Real-time ECG signal processing

## Credits

**Course**: Data Structures and Algorithms Laboratory (AY 2024-2025)
**Institution**: [Your Institution]
**Student**: PEREZ

## License

Educational use only. Datasets are used under PhysioNet's Creative Commons License.

## Support

For issues or questions, please review the source code comments in `index.html` or contact the development team.

---

*Last Updated: April 2026*

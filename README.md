<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>


<img src="https://github.com/user-attachments/assets/38b8f0ec-304c-4a9c-8e59-c5a451a9c70e">

  <h1>Parti Viewer Insight</h1>

  <p><strong>Note:</strong> This application is currently in Beta Testing phase. Features and functionality may change.</p>

  <p>
    Parti Viewer Insight is a desktop application built with Python and Tkinter to monitor and analyze livestream viewer data from the
    <a href="https://parti.com" target="_blank">Parti</a> platform. It distinguishes between real and fake (bot) viewers based on different viewer ratios.
  </p>

  <h2>Features</h2>
  <ul>
    <li>Fetch livestream viewer data for specified streamer IDs.</li>
    <li>Analyze viewer counts using 8:1 and 12:1 real-to-bot ratios.</li>
    <li>Display streamer avatars, usernames, and viewer statistics.</li>
    <li>Visual indicators for real and fake viewers.</li>
    <li>Auto-refresh data every 60 seconds.</li>
  </ul>

  <h2>Installation</h2>
  <ol>
    <li>Ensure you have Python 3 installed.</li>
    <li>Install required packages:</li>
  </ol>

  <pre><code>pip install -r requirements.txt</code></pre>

  <ol start="3">
    <li>Run the application:</li>
  </ol>

  <pre><code>python parti_viewer_insight.py</code></pre>

  <h2>Usage</h2>
  <ul>
    <li>Click the "Fetch Stream Data" button to retrieve and display viewer statistics.</li>
    <li>The application will auto-refresh data every 60 seconds.</li>
    <li>Viewer statistics are displayed with visual indicators for easy analysis.</li>
  </ul>

  <h2>License</h2>
  <p>This project is licensed under the <a href="https://github.com/Riotcoke123/Parti-Viewer-Insight/blob/main/LICENSE" target="_blank">GPL-3.0 License</a>.</p>



</body>
</html>

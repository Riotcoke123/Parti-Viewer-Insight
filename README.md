
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />

</head>
<body>

<h1>Parti Viewer Insight</h1>

<p><strong>Parti Viewer Insight</strong> is a desktop application built with Python and Tkinter to monitor and analyze livestream viewer data from the <a href="https://parti.com" target="_blank" rel="noopener noreferrer">Parti</a> platform. It distinguishes between real and fake (bot) viewers based on different viewer ratios.</p>

<h2>Features</h2>
<ul>
  <li>Fetch livestream viewer data for specified streamer IDs.</li>
  <li>Calculate and display real vs fake viewers with 8:1 and 12:1 viewer-to-bot ratios.</li>
  <li>Shows streamer profile info including avatar and username.</li>
  <li>Automatic data refresh every 60 seconds.</li>
  <li>User-friendly GUI with progress bars and status indicators.</li>
</ul>

<h2>Installation</h2>
<p>Ensure you have Python 3.7+ installed.</p>

<pre><code>pip install -r requirements.txt
</code></pre>

<h2>Usage</h2>
<p>Run the main application script:</p>

<pre><code>python parti_viewer_insight.py
</code></pre>

<p>Replace the <code>user_ids</code> list in the script with your desired Parti streamer IDs.</p>

<h2>Customization</h2>
<ul>
  <li>You can add or remove streamer IDs in the <code>user_ids</code> list.</li>
  <li>The refresh interval is set to 60 seconds but can be changed in the code.</li>
  <li>The GUI size and appearance can be adjusted in the script.</li>
</ul>

<h2>Contributing</h2>
<p>Feel free to open issues or submit pull requests on <a href="https://github.com/Riotcoke123/Parti-Viewer-Insight" target="_blank" rel="noopener noreferrer">GitHub</a>.</p>

<h2>License</h2>
<p>This project is licensed under the <a href="https://www.gnu.org/licenses/gpl-3.0.en.html" target="_blank" rel="noopener noreferrer">GNU General Public License v3.0</a>.</p>

</body>
</html>

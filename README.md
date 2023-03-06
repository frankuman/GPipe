
# GPipe - The Gerrit Analysis Pipeline
<!DOCTYPE html>
<html>
  
  <body>
    <div align="center">
      <img src="https://github.com/frankuman/GPipe/blob/main/assets/images/introcard.png?raw=true" width="900" title="GPipe Logo">
      <p><strong>GPipe</strong> is a Gerrit Analysis Pipeline</p>
      <p>GPipe was made by Oliver Bölin during a university course at Blekinge Tekniska University (BTH).</p>
      <p>To use and install this tool, it is recommended that you'll need </p>
      <ul>
        <p><b>1. Python 3.x </b></p>
        <p><b>2. Pip </b></p>
       </ul> 
        <p>While there is an executable available, it is not recommended to use it. Instead, it is recommended that you install Python, and pip separately and then run the tool using the provided Python script.</p>
    </div>
    <h2>Setup</h2>
    <p>First-time installation:</p>
    <ul>
      <li><strong>1.</strong> Clone the repository: <code>git clone https://github.com/frankuman/GPipe</code></li>
      <li><strong>2.</strong> Open a terminal window in the folder by typing: <code>cd GPipe</code> or by writing cmd in the fileinput</li>
       <img src="https://i.gyazo.com/aedeeea741fc0d4bf40a54ad337ca14b.png" width="500" title="Write in the fileentry">
      <li><strong>3.</strong> Install the required packages: <code>pip install -r requirements.txt</code></li>
      <li><strong>4.</strong> Ubuntu users also need to run: <code>sudo apt-get python3-tk</code></li>
    </ul>
    <h2>Run</h2>
    <p>How to run:</p>
    <ul>
      <li><strong>(RECOMMENDED)</strong> Run the script with: <code>python main.py</code></li>
      <li><strong>(WINDOWS USERS)</strong> If you don't know about Python or pip, you can just make a shortcut of the GPipe.exe and run that shortcut from anywhere</li>
      <li><strong>Have fun!</strong></li>
    </ul>
    <h2>Usage</h2>
    <p>GPipe is not that sophisticated and should not be that hard to learn!</p>
    <ul>
      <li><strong>Time settings</strong> - Here you can set the time for your search, default is current time - 1 day</li>
      <li><strong>Graph settings</strong> - Here you can choose the X-axis and if you want to pop out pyplot</li>
      <li><strong>Generate graph</strong> - If you have made a run, you can now generate a graph on that data. You can also change the X-axis in graph settings.</li>
      <li><strong>Generate PDF</strong> - If you have made a run, you can now generate a PDF on that data. You can also change the X-axis in graph settings.</li>
      <li><strong>Generate EXCEL</strong> - If you have made a run, you can now generate an EXCEL on that data.</li>
      <li><strong>Platform picker</strong> - Here you choose one of the platforms. I have not added authentication, but it could probably be done easily. Chromium and Android are a bit slower than OpenDEV.</li>
      <li><strong>is:</strong> - Choose a metric, or none, if none, it searches all changes.</li>
      <li><strong>/ Crawl</strong> - Input a username or similar stuff</li>
      <li><strong>/ Run</strong> - Run GPipe with current settings</li>
      <li><strong>/ Quit</strong> - Quit GPipe</li>
  </ul>

  <div align="center">
    <h2>Current GUI with latest additions</h2>
    <img src="https://i.gyazo.com/9f3f3901ad4f274a960b7eb24d18d821.png" width="1000" title="Current UI">
  </div>
   <h2>Testers</h2>
  <p><b>Thank you testers, Gustav B(win10), Elias E(win10)</b></p>
 </body>

</html>

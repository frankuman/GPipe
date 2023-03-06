<!DOCTYPE html>
<html>


<body>
  <div align="center">
    <img src="https://github.com/frankuman/GPipe/blob/main/assets/images/gpipe.png?raw=true" width="500" title="GPipe Logo">
    <p>GPipe is a Gerrit Analysis Pipeline</p>
    <p>GPipe was made by Oliver Bölin during a university course at Blekinge Tekniska University (BTH)</p>
  </div>

  <h2>Setup</h2>
  <p>First time installation</p>
<ul>
    <li><b>1. </b>First use "git clone https://github.com/frankuman/GPipe"</li>
    <li><b>2. </b>Open a terminal window in the folder by writing in the text window</li>
     <img src="https://i.gyazo.com/aedeeea741fc0d4bf40a54ad337ca14b.png" width="500" title="Write in the fileentry">
    <li><b>3. </b>pip install -r requirements.txt</li>
    li><b>Ubuntu users also need to do sudo apt-get python3-tk</b>p</li>
    
   
 </ul>
    <h2>Run</h2>
  <p>How to run</p>
<ul>
    <li><b>(RECOMMENDED)</b> python main.py</li>
    <li><b>(WINDOWS USERS)</b> If you don't know about Python or pip, you can just make a shortcut of the gpipe1.0.exe and run that shortcut from anywhere</li>
    <li><b>Have fun!</b></li>
     
  </ul>
  
  <h2>Usage</h2>
  <p>GPipe is not that sophisticated and should not be that hard to learn!</p>
  <ul>
    <li><b>Time settings</b> - Here you can set the time for your search, default is current time-1 day</li>
    <li><b>Graph settings</b> - Here you can choose the X-axis and if you want to popout pyplot</li>
    <li><b>Generate graph</b> - If you have made a run you can now generate a graph on that data, you can also change the x-axis in graph settings</li>
    <li><b>Generate PDF</b> - If you have made a run you can now generate a PDF on that data, you can also change the x-axis in graph settings</li>
    <li><b>Generate EXCEL</b> - If you have made a run you can now generate an EXCEL on that data</li>
    <li><b>Platform picker</b> - Here you choose one of the platforms. I have not added authentication but it could probably be done easily, chromium and android is a bit slower than OpenDEV</li>
    <li><b>is:</b> - Choose a metric, or none, if none it searches all changes.</li>
    <li><b>/ Crawl</b> - Input a username or similar stuff</li>
    <li><b>/ Run</b> - Run GPipe with current settings</li>
    <li><b>/ Quit</b> - Quit GPipe</li>
  </ul>

  <div align="center">
    <h2>Current GUI with latest additions</h2>
    <img src="https://i.gyazo.com/be6c2c93afa34a7fb7ebd90a8b416764.png" width="1000" title="Current UI">
  </div>
</body>

</html>

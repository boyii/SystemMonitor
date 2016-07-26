# SystemMonitor
Group project for cs115 summer

# Install guide  
We strongly recommend using Anaconda that helps manage packages.  
pip install numpy pyqtgraph pyqt4 wmi psutil  
`git clone https://github.com/boyii/SystemMonitor`  
or  
you can download exe file at  
https://drive.google.com/open?id=0B_SJtFULh0GmXzdiX0hoRlppaU0  

# User guide  
If you execute sysmonitor_version1.py or dist/sysmonitor_version1.exe,  
you can watch general resource usage.
If you click detail button, detail window is popped.  
In detail window, there are resource usage of each processes.  
If you click `>>>` button in main window, network usage with line graph is popped.  
If there are processes that use cpu resource more than 50% or use memory more than 1 GB,  
our software would alert notification.

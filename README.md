# SystemMonitor
Group project for cs115 summer

# Installation guide  
We strongly recommend using Anaconda that helps managing packages.  
pip install numpy pyqtgraph pyqt4 wmi psutil  
`git clone https://github.com/boyii/SystemMonitor`  
or  
you can download exe file at  
https://drive.google.com/open?id=0B_SJtFULh0GmXzdiX0hoRlppaU0  

# User guide  
If you execute sysmonitor_version1.py or dist/sysmonitor_version1.exe,  
you can watch general resource usage (CPU, disk, memory, network).
If you click the detail button, a detailed window will be popped up.  
In the detailed window, you will see resource usages of each process.  
If you click `>>>` button in main window, network usage with a line graph will be popped up.  
If there are processes that use cpu resource more than 50% or use memory more than 1 GB,  
our software will send users an alert notification.

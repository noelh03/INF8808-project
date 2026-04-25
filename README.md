**Overview :**   
This project is an interactive implementation of a data visualization system designed to analyze the determinants of commercial success and popularity of video games on Steam.   
   
The project aims to answer the following central question: *What factors determine the commercial success and popularity of video games on Steam?*. The target user is a market analyst seeking to understand trends and patterns in the video game industry .   
   
The application is built using Dash and Plotly, and follows a scrollytelling approach with multiple interactive visualizations.


**Authors :**    
- Team 11, INF8808 – Data Visualization (H2026)


**Project Structure :**    
```bash
src/    
│    
├──assets/                      # CSS, dataset, icon    
│    
├──viz1_scatter/                # Price vs Success    
│   ├──hover_template.py    
│   ├──plot_generate.py    
│   ├──preprocess.py    
│   └──viz1_scatter.py    
│    
├──viz2_beeswarm/                    #TODO Add brief title     
│    
├──viz3_line/                   #TODO Add brief title     
│    
├──viz4_bubble/                 #TODO Add brief title     
│    
├──viz5_dot/                    #TODO Add brief title     
│    
├──viz6_violin/                 #TODO Add brief title     
│    
├──app.py                       # Main Dash layout    
└──server.py                    # Server entry point    
```

**Reference :**     
- Source files were adapted from Lab 4


**Visualizations & Questions :**     
The application includes 6 interactive visualizations, each answering specific analytical questions :


**Installation :**     
- pip install -r requirements.txt

**Run the App :**        
- cd src & python server.py
- Open : http://127.0.0.1:8050/


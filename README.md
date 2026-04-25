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
├──assets/                      # CSS, dataset, icon, logos    
│    
├──main_components/             # hero and sidebar components
│    
├──utils/                       # util functions
│    
├──viz1_scatter/                # Price & Success    
│   ├──hover_template.py    
│   ├──plot_generate.py    
│   ├──preprocess.py    
│   └──viz1_scatter.py    
│    
├──viz2_beeswarm/               # Game mode & Success     
│    
├──viz3_line/                   # Genres & Success     
│    
├──viz4_bubble/                 # Visibility vs Satisfaction     
│    
├──viz5_dot/                    # Satisfaction vs Time played     
│    
├──viz6_violin/                 # Editors & Success     
│    
├──app.py                       # Main Dash layout    
└──server.py                    # Server entry point    
```

**Reference :**     
- Source files were adapted from Lab 4

**Visualizations & Questions :**     
- The application includes 6 interactive visualizations, each answering specific analytical questions.     

**Installation :**     
- pip install --upgrade -r requirements.txt --upgrade-strategy eager

**Run the App :**       
- Local host :   
    - cd src & python server.py       
    - Open : http://127.0.0.1:8050/        
       
- Website : https://a860086e-dc13-4b4e-ac3c-f7ead9eb360b.plotly.app

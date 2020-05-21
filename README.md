## NBA Spread Predictions 

An app for predicting the point spread for any given NBA basketball game.  

Built off of swar's nba_api ([1])

Occasional predictions found in DATA/Predictions. For predictions on today's games run below code:

**Command Line**
`$ pipenv install`  
`$ python -m NBA todays_bets --display True --save False`    
^^Incredibly slow due to how inputs to the model are currently being generated (i.e. many stats.nba api calls), see
TO DO #6

**Usage**  
`$ pipenv install`   
`$ pipenv shell`   
`$ python`   
`>>> from predcitions.predictions import GamePredict`   
`>>> GamePredict('DEN', 'IND').predict_spread()`   

Output is in terms of the home team (i.e. prediction is DEN wins by 2.3)   
`-->[-2.3]`   


#### **TO DO**
1. ~~Command Line Interface~~
2. Back test input generation method   
    Currently using rolling average from last 6 games
3. ~~Scrape daily lines~~
4. ~~Write bet algo~~
5. Method for recording bets and results  
6. Build database of past games and boxscores; configure methods to constantly update; will speed up prediction time

    

[1]: https://github.com/swar/nba_api

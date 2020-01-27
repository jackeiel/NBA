## NBA Spread Predictions 

*Project in progress*   
*Updates coming soon*   

Built off of swar's nba_api ([1])

**Command Line**
`$ pipenv install`
`$ python -m NBA todays_bets --display True --save False`

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

    

[1]: https://github.com/swar/nba_api
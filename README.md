# Badminton-Project

In June 2022 at the Indonesia Open, Liu Yuchen and Ou Xuanyi became the first men's doubles pair from the reserve list to win a Super 1000 title, winning all matches in straight sets and defeating the 2nd, 5th, and 6th seeds.

This led me to think: is there really that much of a difference between players of different rankings? To answer this problem, I tried to use a T distribution 2 means test to see if there is a difference between the mean score difference between players with rank difference of a and b. If the T test gives a difference between the means, than we can conclude that matches between players with a greater rank difference will have a different mean difference in score than matches between players with a less rank difference. Note that a T test is appropriate because BWF World Tour is one of many badminton tournaments; other competitions include World Championships, Sudirman Cup, Thomas Cup, etc.  

I will only be considering the men's singles (MS) event for this project. The match data is pulled from some BWF World Tour tournaments from 2018 to 2021. There is also week-by-week world ranking data for this time period.

To compute the score difference for a score of x-y, I did (x-(x+y)/2)^2. x-(x+y)/2 kind of expresses the difference from the "expected" score, where both sides are even. We can experiment with different functions to compute the score difference. 

Explanations for each file: 
1. historical_bwf_ranking.csv: MS world rankings
2. ms.csv: MS matches from BWF World Tour
3. compare_players.py: something that I thought was interesting. This file compares two MS players in titles, runner-ups, and head-to-head record (during the timeframe of the data of course). 
4. ranking_affect_points.py: computes the statistics and gives a conclusion about two different ranges of rank differences.

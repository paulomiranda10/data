# Stock's Robot
![plot](./tradder_icon.jpg)

## What does this program do ?

- It reads stocks prices from yahoo finance, calculates the returns and standard deviation for each stock in the informed period.
- Show the data in a graphical interface using streamlit lib
- Besides that it allows a simulation for a stock return using moving averages. 
- From a start date the program uses several parameters to calculate which strategy would be better (buy/hold or day trade) in order to maximize the return.
- The paremeters are: 
    Initial Investiment: The starting value investment
    Increasing days: After how many days of positive valuation before buy
    Decreasing days: After how many days of negative valuation before buy
    Circuit Breaker(%): After lose X% sell the stock
    CB (Circuit Breaker) waiting days: After a Circuit Breaker, how many days of waiting before start buy again
 
## How to execute this program ?
- The Programa works based on .csv files and yahoo finance
- You can use the pre-selected stocks included in the B3_new.csv file, or you can edit this file to include or exclude stocks as you wish.
- After that just call the program: 
   streamlit run strocksrobot.py

![plot](./pic3.png)

- The execution will open in a web browser in the localhost:8501
- It is possible to assign another port (i.e. 8080) by using: streamlit run strocksrobot.py --server.port 8080

## What can go wrong ?
VisualStudio Code uses the "base" version of Anaconda with is incompatible with some libs that I am using in this application, which works great with python version 3.7.9. 
Sometimes the execution from VisualStudio Code presents issues, even selecting the correct environment from Anaconda. 
To avoid that you can call the execution from a command line outside  VS Code.

### Pics from Execution
![plot](./pic1.png)
![plot](./pic2.png)
![plot](./pic4.png)
![plot](./pic5.png)
![plot](./pic6.png)
![plot](./pic7.png)
![plot](./pic8.png)
<!--<img src="./pic1.png">-->

- Have Fun !!!


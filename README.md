### Automatic Trading API

This is a Flask REST API that I created that acts as a hub for users to register, create trading strategies, and set them to automatically execute.

![image](https://github.com/masonhgn/noletradeapi/assets/73012906/b929d8fb-3c3f-4169-a0ae-9d628af40c4c)

Trading strategies are automatically executed in OrderExecutor, via crontab, every trading day.

There is a front end component that connects to this flask rest API allowing for this structure:
![image](https://github.com/masonhgn/noletradeapi/assets/73012906/a1bd86a4-3f90-4c67-b9af-766aa58ad8d6)

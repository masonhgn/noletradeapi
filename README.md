### Automatic Trading API

This is a Flask REST API that I created that acts as a hub for users to register, create trading strategies, and set them to automatically execute.

![image](https://github.com/masonhgn/noletradeapi/assets/73012906/b929d8fb-3c3f-4169-a0ae-9d628af40c4c)

Trading strategies are automatically executed in OrderExecutor, via crontab, every trading day.

> **Warning**
> Please be advised that usage of this tool is entirely at your own risk. I assumes no responsibility for any adverse consequences that may arise from its use, and users are encouraged to exercise caution and exercise their own judgment in utilizing this tool.

# ExitLag auto signup

A tool that auto fetch a temporary email address and creates an account at https://exitlag.com/




## How it works

The process begins by utilizing the [Temp-Mail](https://temp-mail.org/en/) service to obtain a temporary email address. This email address is then utilized to sign up for an [ExitLag](https://exitlag.com) account. Subsequently, another request is made to [Temp-Mail](https://temp-mail.org/en/) to retrieve the email confirmation link. Upon activation of the account, the user is able to log in to the ExitLag application and benefit from its functionality.


## Features

- Be able to prompt to change to your own password instead of using the default one.
- Bypass Cloudflare's bot check.
- Error handling.

> **Warning**
> It is important to note that excessive usage of this tool may result in rate limiting by the API or, in severe cases, IP blocking. To avoid these potential consequences, it is recommended to limit the number of usage. (Maybe 5 times every 10 minutes?)
## Installation / Usage

First, clone this repository:
```shell
git clone https://github.com/qing762/exitLag-auto-signup/
```
Install the necessary dependencies:
```shell
pip install -r requirements.txt
```

Next, run the Python file:
```shell
python main.py
```

And you're all set! Follow the instructions while interacting with the Python file.
    
## Contributing

Contributions are always welcome!

To contribute, fork this repository and improve it. After that, press the contribute button.
## FAQ
#### Why did you create this?

Due to persistent high ping of over 100 while participating in online gaming sessions with my peers, I frequently experienced disconnections from game servers. However, after utilizing ExitLag, my ping was reduced to a more manageable level of 40+. Despite the positive outcome, I was dissatisfied with the cumbersome sign-up process. As a result, I elected to develop a custom code solution that would automate this process, also eliminating the need for monetary expenditure.

Additionally, as the school holiday approached, I found myself with an abundance of free time due to a lack of pressing obligations. To combat boredom, I decided to devote my weekends to this project, which provided a productive and educational outlet for my leisure time.

#### Is it bannable?

I'm not sure but mostly it is as it bypasses Cloudflare's bot check.


#### Do you plan to update it if it's patched?

Unfortunately, I have no plans of updating this project for now. But you can [create an issue](https://github.com/qing762/exitLag-auto-signup/issues/new/) if there is a problem within my code.


#### Any plans on improving the project?

Sadly, no.
## Lessons Learned

I initially perceived this task to be a formidable challenge, as circumventing Cloudflare's bot detection is known to be a complex and arduous process. However, with the aid of several dependencies, I was successful in resolving the issue. Through this experience, I was able to expand my knowledge and understanding of API requests.


## Feedback

If you have any feedback, please reach out to me at [Discord](https://discord.com/users/635765555277725696)
## Authors

- [@qing762](https://www.github.com/qing762)


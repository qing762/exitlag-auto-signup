> [!NOTE]  
> Join the [Discord server](https://qing762.is-a.dev/discord) for issues. Thanks a lot!

> [!WARNING]
> Please be advised that usage of this tool is entirely at your own risk. I assumes no responsibility for any adverse consequences that may arise from its use, and users are encouraged to exercise caution and exercise their own judgment in utilizing this tool.

# ExitLag auto signup

A tool that auto fetch a temporary email address and creates an account at https://exitlag.com/

## How it works

The process begins by utilizing the [Ghostlymail](https://www.ghostlymail.com/) service to obtain a temporary email address. This email address is then utilized to sign up for an [ExitLag](https://exitlag.com) account. Subsequently, another request is made to [Ghostlymail](https://www.ghostlymail.com/) to retrieve the email confirmation link. Upon activation of the account, the user is able to log in to the ExitLag application and benefit from its functionality.


## Features

- Be able to prompt to change to your own password instead of using the default one.
- Bypass Cloudflare's bot check.
- The script does all the job itself, including the captcha (which in the past you need to do it manually)
- Able to choose between email service provider
- No webdriver required
- Fast execution time

> **Warning**
> It is important to note that excessive usage of this tool may result in rate limiting by the API or, in severe cases, IP blocking. To avoid these potential consequences, it is recommended to limit the number of usage. (Maybe 5 times every 10 minutes?)
## Installation / Usage

### [>>> VIDEO GUIDE <<<](https://qing762.is-a.dev/exitlag-guide)

First, clone this repository:
```shell
git clone https://github.com/qing762/exitLag-auto-signup/
```
Install [Google Chrome](https://google.com/chrome/) (IMPORTANT!)
```shell
INSTALL HERE: https://google.com/chrome/
```

Install the necessary dependencies:
```shell
pip install -r requirements.txt
```

Finally, run the Python file:
```shell
python main.py
```

And you're all set! Follow the instructions while interacting with the Python file.


## Known issues
[Here are a list of known issues and on how you can fix it](https://github.com/qing762/exitlag-auto-signup/discussions/4)


## Contributing

Contributions are always welcome!

To contribute, fork this repository and improve it. After that, make a pull request.


## Feedback / Issues

If you have any feedback or issues running the code, please join the [Discord server](https://qing762.is-a.dev/discord)

### FOR EXITLAG EMPLOYEES IF YOU WISH TO REQUEST FOR TAKING DOWN THIS PROJECT

If the company wishes to discontinue or terminate this project, please do not hesitate to reach out to me. I can be reached at [Discord/qing762](https://discord.com/users/635765555277725696). Thank you for your attention to this matter.


## License

[MIT LICENSE](https://choosealicense.com/licenses/mit/)

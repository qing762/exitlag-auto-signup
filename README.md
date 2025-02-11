> [!WARNING]
> Please be advised that usage of this tool is entirely at your own risk. I assumes no responsibility for any adverse consequences that may arise from its use, and users are encouraged to exercise caution and exercise their own judgment in utilizing this tool.

# ExitLag auto signup

A tool that auto fetch a temporary email address and creates an account at https://exitlag.com/

## How it works

The process begins by utilizing the [Mails.org](https://mails.org/) service to obtain a temporary email address. This email address is then utilized to sign up for an [ExitLag](https://exitlag.com) account. Subsequently, another request is made to [Mails.org](https://mails.org/) to retrieve the email confirmation link. Upon activation of the account, the user is able to log in to the ExitLag application and benefit from its functionality.


## Features

- Be able to prompt to change to your own password instead of using the default one.
- Password complexity checker for custom password.
- Error handling.
- Bypass Cloudflare's bot check.
- The script does all the job itself, including the captcha (which in the past you need to do it manually)
- No webdriver required
- Fast execution time


## Installation / Usage

### [>>> VIDEO GUIDE <<<](https://qing762.is-a.dev/exitlag-guide)

#### 1. Portable executable method:
- Just download the executable from the [releases tab](https://github.com/qing762/exitLag-auto-signup/releases) and run it to generate accounts.
- If your antivirus has flagged for potential malware, that should be a false flag so feel free to safely ignore. If you dont trust it enough somehow, feel free to use [Step 2](https://github.com/qing762/exitlag-auto-signup#2-python-file-method) instead.
- The account details should be generated at the `accounts.txt` file under the same directory.

#### 2. Python file method:
 - First, clone this repository:
```shell
git clone https://github.com/qing762/exitLag-auto-signup/
```

- Install the necessary dependencies:
```shell
pip install -r requirements.txt
```

- Finally, run the Python file:
```shell
python main.py
```

- And you're all set! Follow the instructions while interacting with the Python file.


## Known issues
[Here are a list of known issues and on how you can fix it](https://github.com/qing762/exitlag-auto-signup/discussions/4)


## Contributing

Contributions are always welcome!

To contribute, fork this repository and do anything you wish. After that, make a pull request.


## Feedback / Issues

If you have any feedback or issues running the code, please join the [Discord server](https://qing762.is-a.dev/discord)

### FOR EXITLAG EMPLOYEES IF YOU WISH TO REQUEST FOR TAKING DOWN THIS PROJECT

If the company wishes to discontinue or terminate this project, please do not hesitate to reach out to me. I can be reached at [Discord/qing762](https://discord.com/users/635765555277725696). Thank you for your attention to this matter.


## License

[MIT LICENSE](https://choosealicense.com/licenses/mit)

---


![Alt](https://repobeats.axiom.co/api/embed/5fa1c9e927a371aaef22a77745c207680dcac293.svg "Repobeats analytics image")


---

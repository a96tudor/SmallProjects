## Synopsis

This is a website blocker that runs in the background, written in Python 3.6. Currently, it ony has support for Windows, Linux and MacOS X

## Dependencies

The only dependency this project has is [Python 3-6](https://www.python.org/downloads/release/python-360/)

## Usage

There are 2 parts of the application : 

###  1. The setup part.

    It is a command-line UI that collects the information from the user (such as what sites he/she wants blocked or what time intervalto be blocked).

<br \>

It can be run by using the script : 

```bash
   python3 setup.py
```

###  2. The actual website blocker

It is an application that just runs in the background and blocks the websites from the configuration file.
<br \>
What is does is to modify a system file and thus intercept all the websites from the configuration file. 
<br \>
**IMPORTANT : ** You will need administrator rights to run this application.
<br \>
For Mac OS/ Linux just run :
```
    sudo python3 website-blocker.py
```
For Windows, you will have to run cmd as an administrator, use the [cd](https://en.wikipedia.org/wiki/Cd_(command)) command to go to the directory where you donwloaded the application and then run : 
```
    python3 website-blocker.py
```
### Important things: 

1. Remember to **run this application as an administrator**
<br \>
2. Use the setup script **only before** you run the actual blocker. If you do this while the blocker is working, it would just not have any effect. 
<br \>
3. Once you setup once, the website blocker will use the same configuration every time it runs. 
Therefore, it is no need to run the setup script unless the config file is corrupted or you need to change it.

## Licence 

This project is available under standard MIT licence. See [LICENSE](https://github.com/a96tudor/SmallProjects/blob/master/LICENCE.md) file for details.

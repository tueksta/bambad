# Bamboo Artifact Downloader (BambAD)
## What it is, how it works
This is a command line tool for finding, downloading, unpacking and launching Bamboo artifacts for Mac, Windows, and iOS on a Bamboo server via the Bamboo API(s). It will create a folder structure like this example:

```
~/Downloads/Myapp
├── develop/
│   ├── 1543/
│   	├── ios/
│   	├── mac/
│   	└── win/
│   └── 1542/
│   	├── ios/
│   	├── mac/
│   	└── win/
└── feature-my-feature-branch/
│   └── 4/
    	└── win/
```

The highest level folder is specified in the projects ini-file, if none specified the user's Downloads folder will be used. Next folder level is the branch name. The next lower folder level shows the buildnumber. The lowest folder level identifies the platform of the artifact. Inside that folder the artifact is stored as the compressed file that was downloaded from bamboo. If `--extract` wasn't explicitly set to `False` the compressed file will be extracted inside that folder. If `--launch` was specified, the executable will be attempted to launch.

The workflow of the app is:
* Authenticate with Bamboo
* Search/Identify the artifact at Bamboo
* Retrieve the artifact from Bamboo
* Extract the artifact locally
* Trigger launch of the artifact executable

Authentication has to be done manually the first time around and the application will interactively ask for username and password. The provided username and password are stored in the keychain for future uses.

The artifact is identified via a search term that is matched against all branch names of the Bamboo plan. The first match will be retrieved.

Before downloading the artifact it is first checked if the target file already exists, and if it does, the step is skipped.

Before extracting the downloaded artifact is first checked if the target file already exists, and if it does, the step is skipped.

Launching the app triggers a separate process, so the command line tool will continue and finish up and leave the app running.

## Examples
Download and launch on mac the branched tagged with JIRA ticket number `ABC-3035`:

```
python3 /path/to/bambad/bambad.py mac --launch --search ABC-3035
```

Download `develop` branch for all OSs:

```
python3 /path/to/bambad/bambad.py all
```

Download `feature-ABC-3177-sidebar-model` branch for mac and iOS:

```
python3 /path/to/bambad/bambad.py macios --search feature-ABC-3177-sidebar-model
```

Download and execute a branch containing the term `layout` for iOS:

```
python3 /path/to/bambad/bambad.py ios --launch --search layout
```

### Prerequisites
* Python 3
* Python libs getpass, keyring, requests, configparser, configargparse, subprocess (install via `pipenv install`)
* On Windows: curl (install via 'choco install curl')

### Experimental prerequisites
* For iOS launching: ios-deploy ( https://github.com/ios-control/ios-deploy ), but experimental only

### .ini
Every Bamboo repository needs an .ini file. Example inis are provided.

The .ini file has two optional arguments:
```
username            Specify username for bamboo, defaults to active system
                    username. This parameter overrides the username stored
                    in the keychain if any exists
path                Specify download base path for artifacts, defaults to:
                    ~/Downloads/
```


### Usage
```
bamboo.py [--help] [--build] [--config] [--search] [--download] [--extract] [--launch] [--verbose]
		  {mac,ios,macios,win,all}
```

### Arguments
```
{mac,ios,macios,win,all}
```

Choose the platform for which you want the artifacts to be downloaded. Download and extraction works for all platforms, but launching on iOS has some special challenges (needs stable connection, sometimes restart of device required for app to show up).

### Options

```
-h, --help          Show this help message and exit

-c, --config        Name of the .ini-file that is to be used from the config folder

-s, --search        Search term that should be looked for in the branch names.
                    The first branch on bamboo that matches this term will be
                    downloaded.

-d, --download      Should the artifact be downloaded? Default is: True

-x, --extract       Should the artifact be extracted? Default is: True

-l, --launch        Should the application be launched? Default is: False
                    (Mac and Win only)
-v, --verbose       Raise logging level from 'info' to 'debug'.

-b, --build         Give build number that should be tried to retrieve. If
                    build number is not found on server, latest build is
                    retrieved instead.
```

### Windows specialties
You need to install curl first, you can do that via chocolatey `choco install curl`.
If you want the colored output, you need to activate it in Powershell via `Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1` first.

### Helpful bash aliases

This tool is most helpful to speed up your process if you create aliases for your most regular usecases. You should add them to your `.env` in this fashion:
```
branch() { python3 /path/to/bambad/bambad.py mac -l -s "$1"; } # downloads and executes a branch on macOS by name match
bambad() { python3 /path/to/bambad/bambad.py "$@"; }
alias rundev='bambad mac --launch'
alias getbrowser='bambad mac --configfile Example.ini'
```

## Contributing

Step one: Check list of open work:

* Use proper path objects
* Unit tests
* ~~Full Windows support for the tool~~
* ~~More detailed Error Handling~~
* Only store verified credentials
* Force refresh credentials
* ~~Use branch names as folder names instead of bamboo plan keys~~
* Use `--force` to overwrite existing files
* Use `--quiet` to lower logging level
* More generic way of specifying and combining target platforms
* ~~Solve iOS deployment code signing issues~~
* Parameter for cleanup of old/all artifacts
* ~~Move Traktor specifics into a configuration file and make tool work with any bamboo plan~~
* Retrieve as much as possible from bamboo instead of config files


Step two: Submit an issue to discuss your idea

Step three: Open very early PR and collaborate

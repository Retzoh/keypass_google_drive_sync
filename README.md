Keypass sync on google drive
============================

This repository contains a pip package enabling the syncing of a
keypass database (or any file) with google drive.

It provides the necessary functions for in-script use and a
command-line tool.

### Usage

###### From a terminal:

> `python -m keypass_sync -h` -- display the documentation

> `python -m keypass_sync init` -- setup the syncing

You will be asked for:

- The path to the file to sync on your machine
- The id of the corresponding file on your google drive
  - (It's the big chain of digits and letters in the middle of the
  sharing link)
- The path to a OAuth ID file (see [installation](#installation))

> `python -m keypass_sync` -- perform a syncing operation

If you now setup a cron job running `python -m keypass_sync`
periodically your file is now synced with your google drive !

###### From python:

> `import keypass_sync`.

### Installation

- Generate and download an OAuth 2 token for your google account
from the
[google developer console](https://console.developers.google.com/apis/credentials):
  - Select a project or create one (top-left of the window)
  - Go to the
  [drive page on the API library](https://console.developers.google.com/apis/library/drive.googleapis.com?q=drive)
  and activate it
  - From the
  [drive API dashboard](https://console.developers.google.com/apis/api/drive.googleapis.com/overview),
  create new credentials (you may have to re-select the project from step 1)
    - For the drive api
    - For a platform with user-interface
    - With access to the user's data
  - Go to your
  [project-credential page](https://console.developers.google.com/apis/credentials)
  - Download the OAuth ID
- Install the [google-services wrapper package](https://github.com/Retzoh/google_services_wrapper)
- Install this package:
  - Clone
  [this repository](https://github.com/Retzoh/keypass_google_drive_sync.git)
  - Install the dependencies
    - I recommend using
    [anaconda](https://www.anaconda.com/distribution/#download-section)
    (python 3.7)
    - run `conda env update -n base` from the repository folder
  - Install the package by running `pip install .` from the repository
  folder

#### Subscribe to updates

Send a mail to
`~retzoh/keypass-google-drive-sync-updates+subscribe@lists.sr.ht`

#### git.sh.ht repository

[https://git.sr.ht/~retzoh/keypass_google_drive_sync](https://git.sr.ht/~retzoh/keypass_google_drive_sync)

#### github repository

[https://github.com/Retzoh/keypass_google_drive_sync](https://github.com/Retzoh/keypass_google_drive_sync)

The master branches on sr.ht and github are synchronized through this
[manifest](https://git.sr.ht/~retzoh/keypass_google_drive_sync/tree/master/.build.yml)
at each commit on master

### Contributing

#### Issue tracker

[https://todo.sr.ht/~retzoh/keypass-google-drive-sync-discussions](https://todo.sr.ht/~retzoh/keypass-google-drive-sync-discussions)

#### Submit patches

Send your patches to
`~retzoh/keypass-google-drive-sync-contributing@lists.sr.ht`

#### Reviewing

Submitted patches can be found there:
[https://lists.sr.ht/~retzoh/keypass-google-drive-sync-contributing](https://lists.sr.ht/~retzoh/keypass-google-drive-sync-contributing)


Send a mail to
`~retzoh/keypass-google-drive-sync-contributing+subscribe@lists.sr.ht`
to be notified of new patches.

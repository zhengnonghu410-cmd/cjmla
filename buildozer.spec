[app]

# (str) Title of your application
title = Super Mario

# (str) Package name
package.name = supermario

# (str) Package domain (needed for android/ios packaging)
package.domain = org.supermario

# (str) Source code where the main.py live
source.dir = .

# (str) The main entry point file (defaults to main.py)
package.entrypoint = main.py

# (list) Source files to include (let empty list to include all the files)
source.include_exts = py,png,jpg,gif,json,ogg,wav

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty list to not exclude anything)
# source.exclude_exts = spec

# (list) List of directory to exclude (let empty list to not exclude anything)
source.exclude_dirs = .idea, __pycache__

# (list) List of exclusions using pattern matching
# source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements (Python packages required)
requirements = python3,pygame

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 30

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 30

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use (leave empty or set to the same as android.minapi)
# android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
# android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
# android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded)
# android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded)
# android.ant_path =

# (bool) If True, then skip trying to update the SDK/NDK/ANT
# android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
# android.accept_sdk_license = False

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (str) python-for-android branch to use
p4a.branch = develop

# (str) Bootstrap (sdl2 for pygame)
p4a.bootstrap = sdl2

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version (not used currently)
# ios.codesign.debug = "iPhone Developer: <name> (<id>)"

# (str) Name of the certificate to use for signing the release version (not used currently)
# ios.codesign.release = %(ios.codesign.debug)s

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 1

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, default is under source dir
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

# -----------------------------------------------------------------------------
# List as sections
#
# You can define all the "list" as [section:key].
# Each line will be considered as a option to the list.
# Let's take [app] / source.exclude_patterns.
# Instead of doing:
#
#[app]
#source.exclude_patterns = license,data/audio/*.wav,data/images/original/*
#
# This can be translated into:
#
#[app:source.exclude_patterns]
#license
#data/audio/*.wav
#data/images/original/*
#

# -----------------------------------------------------------------------------
# Profiles
#
# You can extend section / key with a profile
# For example, you want to deploy a demo version of your application without
# HD content. You could first change the title to add "(demo)" in the name
# and extend the excluded directories to remove the HD content.
#
#[app@demo]
#title = My Application (demo)
#
#[app:source.exclude_patterns@demo]
#images/hd/*
#
# Then, invoke the command line with the "demo" profile:
#
#buildozer --profile demo android debug

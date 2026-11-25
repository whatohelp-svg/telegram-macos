# RiseGram macOS native port

The shared TelegramCore submodule is pinned to the RiseGram macOS core branch. It uses the same DC2 bootstrap and RSA pin as the Android client; cached address lookup and public backup discovery are disabled.

This is experimental source code, not a DMG. The native framework build, macOS compatibility patch, separate bundle ID and data container, Sparkle update feed isolation, signing and notarization, and on-device login, relaunch, chats, media and economy integration still require verification. Use the full upstream workspace; never reuse a Telegram data directory or distribute an unverified application. See INSTALL.md for the native toolchain.

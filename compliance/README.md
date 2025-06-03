# Compliance Scanner (Prototype)

This directory contains a simple proof-of-concept script for checking
system configuration files against a baseline hash list.

The baseline file `baseline/os_baseline.json` defines the expected SHA256
hash of important files such as `/etc/ssh/sshd_config`. Run `scan.py` to
calculate current hashes, compare them to the baseline, and log the
results in `compliance_logs/`.

This is **not** a full-featured compliance monitoring platform, but a
minimal example to demonstrate how baseline validation might work.

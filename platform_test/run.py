#!/usr/bin/python

import argparse



if __name__ == "__main__":
    print("Gizmotronic Boneless")
    p = argparse.ArgumentParser()
    action = p.add_subparsers(dest="action")

    action.add_parser("info")

    action.add_parser("build")

    action.add_parser("program")

    args = p.parse_args()

    if args.action == "info":
        print("Show info")
    if args.action == "build":
        print("Build")
    if args.action == "program":
        print("Program")

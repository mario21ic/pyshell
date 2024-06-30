import sys
import os
import subprocess

def find_in_path(command, mypath):
    sorted_paths = sorted(mypath.split(":"), key=len)
    for path in sorted_paths:
        cmd_path = f"{path}/{command}"
        if os.path.isfile(cmd_path):
            return cmd_path
    return None

def main(mypath=None):
    # REPL loop
    while True:
        # prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        user_input = input().strip().split(" ")
        command = user_input[0]
        params = user_input[1:]

        if command:
            if command == "exit": # and params=="0"
                break # exit the loop with 0 status

            elif command == "echo":
                print(" ".join(params))
            
            elif command == "type":
                valid_commands = ["exit", "echo", "type", "pwd", "cd"]
                params = " ".join(params)
                if params in valid_commands:
                    print(f"{params} is a shell builtin")
                
                elif mypath:
                    cmd_path = find_in_path(params.split(" ")[0], mypath)
                    if cmd_path:
                        print(f"{params} is {cmd_path}")
                    else:
                        print(f"{params}: not found")
                else:
                    print(f"{params}: not found")

            elif command == "pwd":
                print(os.getcwd())

            elif command == "cd":
                if len(params)==0 or params[0]=="~":
                    os.chdir(os.path.expanduser("~"))
                else:
                    try:
                        os.chdir(params[0])
                    except FileNotFoundError:
                        print(f"cd: {params[0]}: No such file or directory")
                    except NotADirectoryError:
                        print(f"cd: {params[0]}: Not a directory")
                    except PermissionError:
                        print(f"cd: {params[0]}: Permission denied")

            else:
                cmd_path = find_in_path(command, mypath)
                if cmd_path:
                    p = subprocess.Popen(f"{cmd_path} {' '.join(params)}", shell=True, text=True, \
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output = p.communicate()
                    output_err = output[1]
                    if len(output_err)>0:
                        # error on command not found
                        if "command not found" in str(output_err):
                            print(f"{command}: command not found")
                        else: # print the error
                            print(output_err)
                    else:
                        print(output[0].strip()) # print stdout
                else:
                    print(f"{command}: command not found")
                


if __name__ == "__main__":
    main(os.environ['PATH'])
import subprocess, json

def main():
    cmd: list[str] = ["bgpq4", "-4j", "AS270777:AS-RGSUL", "-L", "2", "-l", "prefixes"]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()

    result = json.loads(output.decode("ascii"))

    prefixes: list[tuple] = []
    for prefix in result["prefixes"]:
        prefix = {"prefix": prefix["prefix"].split("/")[0], "netmask": prefix["prefix"].split("/")[1]}
        prefixes.append(prefix)
    
    print(prefixes)

if __name__ == "__main__":
    main()
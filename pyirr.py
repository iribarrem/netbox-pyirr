import subprocess, json, pynetbox
from pynetbox.core.response import Record, RecordSet

def main():
    as_set: str = "AS270777:AS-RGSUL"

    cmd_ipv4: list[str] = ["bgpq4", "-4j", as_set, "-L", "2", "-l", "prefixes"]
    cmd_ipv6: list[str] = ["bgpq4", "-6j", as_set, "-L", "2", "-l", "prefixes"]
    
    process_ipv4 = subprocess.Popen(cmd_ipv4, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process_ipv6 = subprocess.Popen(cmd_ipv6, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output_ipv4, error_ipv4 = process_ipv4.communicate()
    output_ipv6, error_ipv6 = process_ipv6.communicate()

    result_ipv4 = json.loads(output_ipv4.decode("ascii"))
    result_ipv6 = json.loads(output_ipv6.decode("ascii"))

    prefixes_ipv4: list[str] = []
    for prefix in result_ipv4["prefixes"]:
        prefixes_ipv4.append(prefix["prefix"])
    prefixes_ipv6: list[str] = []
    for prefix in result_ipv6["prefixes"]:
        prefixes_ipv6.append(prefix["prefix"])
    
    netbox = pynetbox.api(url="https://netbox.iribarrem.com", token="b186b056aae496bb4b2f1b8240964dad6f941265", threading=True)

    pl_ipv4_name: str = as_set + "_IPv4"
    pl_ipv6_name: str = as_set + "_IPv6"

    pl_ipv4 = netbox.plugins.bgp.prefix_list.get(name=pl_ipv4_name)
    pl_ipv6 = netbox.plugins.bgp.prefix_list.get(name=pl_ipv6_name)

    if pl_ipv4 is None:
        netbox.plugins.bgp.prefix_list.create(name=pl_ipv4_name, family="ipv4", description="")
        print(f"Prefix-list {pl_ipv4_name} created!")
    else:
        print(f"Prefix-list {pl_ipv4_name} already exists, deleting all rules...")
        pl_rules: RecordSet = netbox.plugins.bgp.prefix_list_rule.all()
        pl_rules: list[Record] = [pl_rule for pl_rule in pl_rules if pl_rule.prefix_list["id"] == pl_ipv4.id]
        for pl_rule in pl_rules:
            pl_rule.delete()

    if pl_ipv6 is None:
        netbox.plugins.bgp.prefix_list.create(name=pl_ipv6_name, family="ipv6", description="")
        print(f"Prefix-list {pl_ipv6_name} created!")
    else:
        print(f"Prefix-list {pl_ipv6_name} already exists, deleting all rules...")
        pl_rules: RecordSet = netbox.plugins.bgp.prefix_list_rule.all()
        pl_rules: list[Record] = [pl_rule for pl_rule in pl_rules if pl_rule.prefix_list["id"] == pl_ipv6.id]
        for pl_rule in pl_rules:
            pl_rule.delete()

    for index, prefix in enumerate(prefixes_ipv4, start=1):
        netbox.plugins.bgp.prefix_list_rule.create(prefix_list=pl_ipv4.id, action="permit", index=index*10, prefix_custom=prefix)
    for index, prefix in enumerate(prefixes_ipv6, start=1):
        netbox.plugins.bgp.prefix_list_rule.create(prefix_list=pl_ipv6.id, action="permit", index=index*10, prefix_custom=prefix)


if __name__ == "__main__":
    main()
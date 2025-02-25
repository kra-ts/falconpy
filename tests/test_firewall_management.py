""" test_firewall_management.py - This class tests the firewall_management service class"""
import os
import sys
import datetime
# Authentication via the test_authorization.py
from tests import test_authorization as Authorization
# Import our sibling src folder into the path
sys.path.append(os.path.abspath('src'))
# Classes to test - manually imported from sibling folder
from falconpy import FirewallManagement

auth = Authorization.TestAuthorization()
config = auth.getConfigObject()
falcon = FirewallManagement(auth_object=config)
AllowedResponses = [200, 201, 202, 203, 204, 400, 403, 404, 429]
fmt = '%Y-%m-%d %H:%M:%S'
stddate = datetime.datetime.now().strftime(fmt)
sdtdate = datetime.datetime.strptime(stddate, fmt)
sdtdate = sdtdate.timetuple()
jdate = sdtdate.tm_yday
jdate = "{}{}".format(stddate.replace("-", "").replace(":", "").replace(" ", ""), jdate)
rule_group_name = f"falconpy_debug_{jdate}"
rule_group_id = ""


class TestFirewallManagement:
    """Test harness for the Firewall Management Service Class"""

    @staticmethod
    def set_rule_group_id():
        result = falcon.create_rule_group(name=rule_group_name,
                                          enabled=False,
                                          cs_username="HarryHenderson"
                                          )
        global rule_group_id
        rule_group_id = "1234567890"
        if result["status_code"] not in [400, 403, 404, 429]:
            if result["body"]["resources"]:
                rule_group_id = result["body"]["resources"][0]

        return result

    def firewall_test_all_code_paths(self):
        """Test every code path, accepts all errors except 500"""
        error_checks = True
        tests = {
            "aggregate_events": falcon.aggregate_events(body={}),
            "aggregate_policy_rules": falcon.aggregate_policy_rules(body={}),
            "aggregate_rule_groups": falcon.aggregate_rule_groups(body={}),
            "aggregate_rules": falcon.aggregate_rules(body={}),
            "get_events": falcon.get_events(ids="12345678"),
            "get_firewall_fields": falcon.get_firewall_fields(ids="12345678"),
            "get_platforms": falcon.get_platforms(ids="12345678"),
            "get_policy_containers": falcon.get_policy_containers(ids="12345678"),
            "update_policy_container": falcon.update_policy_container(default_inbound="something",
                                                                      default_outbound="something_else",
                                                                      platform_id="linux",
                                                                      tracking="Bob",
                                                                      cs_username="BillTheCat",
                                                                      enforce=False,
                                                                      is_default_policy=False,
                                                                      test_mode=True,
                                                                      rule_group_ids="12345,67890"
                                                                      ),
            "create_rule_group": self.set_rule_group_id(),
            "create_rule_group_fail_one": falcon.create_rule_group(rules={"whatever": "bro"}),
            "create_rule_group_fail_two": falcon.create_rule_group(rules=[{"whatever": "bro"}]),
            "get_rule_groups": falcon.get_rule_groups(ids=rule_group_id),
            "updat3_rule_group": falcon.update_rule_group(id="12345678",
                                                          tracking="Whatever",
                                                          diff_operations=[{"whatever": "brah"}],
                                                          rule_ids="12345,67890",
                                                          rule_versions="1,2,3"
                                                          ),
            "update_rule_group": falcon.update_rule_group(id="12345678",
                                                          name=rule_group_name,
                                                          enabled=False,
                                                          diff_operations={"whatever": "brah"}
                                                          ),
            "delete_rule_groups": falcon.delete_rule_groups(ids=rule_group_id, cs_username="KyloRen"),
            "get_rules": falcon.get_rules(ids="12345678"),
            "query_events": falcon.query_events(),
            "query_firewall_fields": falcon.query_firewall_fields(),
            "query_platforms": falcon.query_platforms(),
            "query_policy_rules": falcon.query_policy_rules(),
            "query_rule_groups": falcon.query_rule_groups(),
            "query_rules": falcon.query_rules()
        }
        for key in tests:

            if tests[key]["status_code"] not in AllowedResponses:
                error_checks = False
#                print(f"Failed on {key} with {tests[key]}")
#            print(tests[key])
        return error_checks

    def test_all_paths(self):
        """Pytest harness hook"""
        assert self.firewall_test_all_code_paths() is True

import ujson as json
import os
from artemis.configuration_manager import config
from deepdiff import DeepDiff
import urllib.parse


def count_roots(values_changed):
    """
    Json diff example :
    {
        "values_changed": {
            "root[1]['quality']": {
                "new_value": -10,
                "old_value": 0
            },
            "root[2]['name']": {
                "new_value": "rue Jean Jaur\u00e8s (Quimper)",
                "old_value": "rue Jean Jaur\u00e8s (Brest)"
            },
            "root[2]['id']": {
                "new_value": "-4.099163864088552;47.99357755862109",
                "old_value": "-4.476088128765972;48.39663769196877"
            },
            ...
        }
    }
    Counts the number of unique roots. In this example, two items have changed : root[1] and root[2]
    """
    updated_roots = set()
    for root in values_changed:
        root_id = root.split("]")[0]
        updated_roots.add(root_id)
    return len(updated_roots)


def make_req_diff(ref_dict, resp_dict, req):
    ref = ref_dict.get(req, [])
    resp = resp_dict.get(req, [])
    diff = DeepDiff(ref, resp)
    return diff


def count_modified_fields(diff):
    values_changed = diff.get("values_changed", [])
    items_added = len(diff.get("iterable_item_added", []))
    items_removed = len(diff.get("iterable_item_removed", []))
    items_changed = count_roots(values_changed)
    return {"added": items_added, "removed": items_removed, "changed": items_changed}


def response_diff(ref_dict, resp_dict):
    req_type = ["journeys", "places", "geo_status"]
    report_message = ""
    for req in req_type:
        diff = make_req_diff(ref_dict, resp_dict, req)
        items_added = count_modified_fields(diff)["added"]
        items_removed = count_modified_fields(diff)["removed"]
        items_changed = count_modified_fields(diff)["changed"]
        if items_added != 0 or items_removed != 0 or items_changed != 0:
            message = (
                "<u>" + req + " :</u>"
                "<ul><li>new " + req + " nb: {}\n</li>"
                "<li>discarded " + req + " nb: {}\n</li>"
                "<li>updated " + req + " nb: {}\n</li></ul>"
                "<details open><summary>CLICK ME</summary><p>\n\n"
                "<pre><code class='language-json\n'>"
                "{}\n"
                "</p></details>\n</code></pre>"
            ).format(
                items_added, items_removed, items_changed, json.dumps(diff, indent=2)
            )
            report_message = "\n".join([report_message, message])
    return report_message


def add_to_report(test_name, test_query, report_message):
    failures_report_path = os.path.join(
        config["RESPONSE_FILE_PATH"], "failures_report.html"
    )

    reading_mode = "a" if os.path.exists(failures_report_path) else "w"
    with open(failures_report_path, reading_mode) as failures_report:
        failures_report.write("<p><strong>{}\n</strong></p>".format(test_name))
        encoded = urllib.parse.quote(test_query)
        failures_report.write(
            (
                "<p><a href=http://canaltp.github.io/navitia-playground/play.html?request={}\n>"
                "open query in navitia-playground</a></p>"
            ).format(encoded)
        )
        failures_report.write("{}\n".format(report_message))

import ujson as json
import os
import copy
from artemis.configuration_manager import config
from deepdiff import DeepDiff
import urllib.parse
from artemis import default_checker


def journey_to_line_sequence(journey):
    result = []
    for section in journey["sections"]:
        if section["type"] == "public_transport":
            line = None
            for link in section["links"]:
                if link["type"] == "line":
                    line = link["id"]
            result.append(line)
    return result

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

def journey_use_same_line_consecutively(journey):
    line_sequence = journey_to_line_sequence(journey)
    if len(line_sequence) == 0:
        return False
    prev_line = line_sequence[0]
    for line in line_sequence[1:]:
        if line == prev_line:
            return True
        prev_line = line
    return False


def journeys_diff(ref_dict, resp_dict):
    ref_journeys = ref_dict.get("journeys", [])
    resp_journeys = resp_dict.get("journeys", [])

    if not ref_journeys and not resp_journeys:
        diff = {}
    elif not ref_journeys and resp_journeys:
        diff = {jsondiff.symbols.insert: [[i, j] for i, j in enumerate(resp_journeys)]}
    elif ref_journeys and not resp_journeys:
        diff = {jsondiff.symbols.delete: [[i, j] for i, j in enumerate(ref_journeys)]}
    else:
        diff = jsondiff.diff(ref_journeys, resp_journeys, syntax="symmetric")

    updated_nb = sum(str(k).isdigit() for k in diff.keys())

    message = (
        "* new journeys nb: {}\n"
        "* discarded journeys nb: {}\n"
        "* updated journeys nb: {}\n"
        "<details open><summary>CLICK ME</summary><p>\n\n"
        "```json\n"
        "{}\n"
        "```\n"
        "</p></details>\n"
    ).format(
        len(diff.get(jsondiff.symbols.insert, [])),
        len(diff.get(jsondiff.symbols.delete, [])),
        updated_nb,
        json.dumps(diff, indent=2),
    )
    return message


def average_fallback_durations(journeys):
    total_start_fallback = 0.0
    start_count = 0
    total_end_fallback = 0.0
    end_count = 0
    start_or_end_count = 0
    for journey in journeys:
        # we skip direct path journeys
        if len(journey["sections"]) <= 1:
            continue
        first_section = journey["sections"][0]
        first_is_street_network = first_section["type"] == "street_network"
        if first_is_street_network:
            start_count += 1
            total_start_fallback += first_section["duration"]
        last_section = journey["sections"][-1]
        last_is_street_network = last_section["type"] == "street_network"
        if last_is_street_network:
            end_count += 1
            total_end_fallback += last_section["duration"]
        if first_is_street_network or last_is_street_network:
            start_or_end_count += 1

    average_start_fallback = (
        total_start_fallback / (1.0 * start_count) if start_count > 0 else 0.0
    )
    average_end_fallback = (
        total_end_fallback / (1.0 * end_count) if end_count > 0 else 0.0
    )
    average_fallback = (
        (total_start_fallback + total_end_fallback) / (1.0 * start_or_end_count)
        if start_or_end_count > 0
        else 0.0
    )
    return (average_start_fallback, average_end_fallback, average_fallback)


def average_walking_duration(journeys):
    total_walking_duration = 0.0
    count = 0
    for journey in journeys:
        # we skip direct path journeys
        if len(journey["sections"]) <= 1:
            continue
        has_walking = False
        for section in journey["sections"]:
            if section["type"] == "street_network" or section["type"] == "transfer":
                total_walking_duration += section["duration"]
                has_walking = True
        if has_walking:
            count += 1

    average_walking = total_walking_duration / (1.0 * count) if count > 0 else 0.0
    return average_walking


def average_nb_pt_section(journeys):
    total_nb_pt_section = 0.0
    count = 0
    for journey in journeys:
        nb_pt_section_in_journey = 0.0
        for section in journey["sections"]:
            if section["type"] == "public_transport":
                nb_pt_section_in_journey += 1

        if nb_pt_section_in_journey > 0:
            total_nb_pt_section += nb_pt_section_in_journey
            count += 1

    return total_nb_pt_section / (1.0 * count) if count > 0 else 0.0


def add_to_csv_report(ref_dict, resp_dict, test_name):

    ref_journeys = copy.deepcopy(ref_dict.get("journeys", []))
    resp_journeys = copy.deepcopy(resp_dict.get("journeys", []))

    filtered_ref_dict = default_checker.default_journey_checker.filter(ref_dict)
    filtered_resp_dict = default_checker.default_journey_checker.filter(resp_dict)

    filtered_ref_journeys = filtered_ref_dict.get("journeys", [])
    filtered_resp_journeys = filtered_resp_dict.get("journeys", [])

    # mask = utils.BlackListMask([("$..type", lambda x: None)])
    # refs = mask.filter(filtered_ref_journeys)
    # resps = mask.filter(filtered_resp_journeys)
    refs = copy.deepcopy(filtered_ref_journeys)
    resps = copy.deepcopy(filtered_resp_journeys)

    for journey in refs:
        journey["type"] = None
    for journey in resps:
        journey["type"] = None

    if refs is None or resps is None:
        return

    deleted = []
    moved = []
    updated = []
    is_new = [True for _ in range(len(resps))]

    for ref_index, ref in enumerate(refs):
        ref_lines = journey_to_line_sequence(ref_journeys[ref_index])
        found = False
        for resp_index, resp in enumerate(resps):
            resp_lines = journey_to_line_sequence(resp_journeys[resp_index])
            if ref_lines == resp_lines:
                found = True
                is_new[resp_index] = False
                if ref != resp:
                    if ref_index == resp_index:
                        updated.append("{}".format(ref_index))
                    else:
                        updated.append("{} -> {}".format(ref_index, resp_index))
                elif ref_index != resp_index:
                    moved.append("{} -> {}".format(ref_index, resp_index))
                break
        if not found:
            deleted.append(ref_index)

    news = [i for i, it_is_new in enumerate(is_new) if it_is_new]

    ref_start_fallback, ref_end_fallback, ref_fallback = average_fallback_durations(
        refs
    )
    resp_start_fallback, resp_end_fallback, resp_fallback = average_fallback_durations(
        resps
    )

    start_fallback_variation = (
        "{:+.0f}".format(
            (resp_start_fallback - ref_start_fallback) * 100 / ref_start_fallback
        )
        if ref_start_fallback > 0.0
        else ""
    )
    end_fallback_variation = (
        "{:+.0f}".format(
            (resp_end_fallback - ref_end_fallback) * 100 / ref_end_fallback
        )
        if ref_end_fallback > 0.0
        else ""
    )
    fallback_variation = (
        "{:+.0f}".format((resp_fallback - ref_fallback) * 100 / ref_fallback)
        if ref_fallback > 0.0
        else ""
    )

    ref_nb_pt_sections = average_nb_pt_section(refs)
    resp_nb_pt_sections = average_nb_pt_section(resps)
    nb_pt_section_variation = (
        "{:+.0f}".format(
            (resp_nb_pt_sections - ref_nb_pt_sections) * 100 / ref_nb_pt_sections
        )
        if ref_nb_pt_sections > 0.0
        else ""
    )

    ref_average_walking = average_walking_duration(refs)
    resp_average_walking = average_walking_duration(resps)
    walking_variation = (
        "{:+.0f}".format(
            (resp_average_walking - ref_average_walking) * 100 / ref_average_walking
        )
        if ref_average_walking > 0.0
        else ""
    )

    refs_use_same_line_consecutively = any(
        journey_use_same_line_consecutively(ref) for ref in ref_journeys
    )
    resps_use_same_line_consecutively = any(
        journey_use_same_line_consecutively(resp) for resp in resp_journeys
    )

    csv_report_path = os.path.join(config["RESPONSE_FILE_PATH"], "report.csv")

    nb_of_journey_variation = (
        "{:+.0f}".format((len(resps) - len(refs)) * 100.0 / (1.0 * len(refs)))
        if len(resps) != len(refs)
        else ""
    )

    report_file_exists = os.path.exists(csv_report_path)
    reading_mode = "a" if report_file_exists else "w"
    with open(csv_report_path, reading_mode) as csv_report:
        if not report_file_exists:
            csv_report.write(
                (
                    "test name; "
                    "nb_refs; "
                    "nb_resps; "
                    "variation (absolute);"
                    "variation (%); "
                    "nb_discarded; "
                    "nb_added; "
                    "nb_updated; "
                    "deleted; "
                    "new; "
                    "updated; "
                    "moved; "
                    "ref_average_start_fallback; "
                    "resp_average_start_fallback; "
                    "start_fallback_variation (absolute); "
                    "start_fallback_variation (%); "
                    "ref_average_end_fallback; "
                    "resp_average_end_fallback; "
                    "end_fallback_variation (absolute); "
                    "end_fallback_variation (%); "
                    "ref_average_fallback; "
                    "resp_average_fallback; "
                    "average_fallback_variation (absolute); "
                    "average_fallback_variation (%); "
                    "ref_average_walking;"
                    "resp_average_walking;"
                    "walking_variation (absolute);"
                    "walking_variation (%);"
                    "ref_average_nb_pt_sections;"
                    "resp_average_nb_pt_sections;"
                    "nb_pt_sections_variation (absolute);"
                    "nb_pt_sections_variation (%);"
                    "refs_use_same_line_consecutively;"
                    "resps_use_same_line_consecutively"
                    "\n"
                )
            )
        csv_report.write(
            ";".join(
                [
                    "{}".format(test_name),
                    "{}".format(len(refs)),
                    "{}".format(len(resps)),
                    "{}".format(len(resps) - len(refs)),
                    "{}".format(nb_of_journey_variation),
                    "{}".format(len(deleted)) if len(deleted) > 0 else "",
                    "{}".format(len(news)) if len(news) > 0 else "",
                    "{}".format(len(updated)) if len(updated) > 0 else "",
                    "{}".format(deleted) if len(deleted) > 0 else "",
                    "{}".format(news) if len(news) > 0 else "",
                    "{}".format(updated) if len(updated) > 0 else "",
                    "{}".format(moved) if len(moved) > 0 else "",
                    "{:.0f}".format(ref_start_fallback),
                    "{:.0f}".format(resp_start_fallback),
                    "{:.0f}".format(resp_start_fallback - ref_start_fallback),
                    "{}".format(start_fallback_variation),
                    "{:.0f}".format(ref_end_fallback),
                    "{:.0f}".format(resp_end_fallback),
                    "{:.0f}".format(resp_end_fallback - ref_end_fallback),
                    "{}".format(end_fallback_variation),
                    "{:.0f}".format(ref_fallback),
                    "{:.0f}".format(resp_fallback),
                    "{:.0f}".format(resp_fallback - ref_fallback),
                    "{}".format(fallback_variation),
                    "{:.0f}".format(ref_average_walking),
                    "{:.0f}".format(resp_average_walking),
                    "{:.0f}".format(resp_average_walking - ref_average_walking),
                    "{}".format(walking_variation),
                    "{:.2f}".format(ref_nb_pt_sections),
                    "{:.2f}".format(resp_nb_pt_sections),
                    "{:.2f}".format(resp_nb_pt_sections - ref_nb_pt_sections),
                    "{}".format(nb_pt_section_variation),
                    "{}".format(refs_use_same_line_consecutively)
                    if refs_use_same_line_consecutively
                    else "",
                    "{}".format(resps_use_same_line_consecutively)
                    if resps_use_same_line_consecutively
                    else "",
                    "\n",
                ]
            )
        )


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

from scripts.stop_condition_alerts import is_stop_condition_alert


def test_protocol_scaffold_text_does_not_alert():
    text = '"stop_condition": "If the active protocol, manifest, lock, task specification, or repository state disagree on the active task, stop and report."'
    assert not is_stop_condition_alert(text)


def test_not_triggered_summary_does_not_alert():
    text = "Stop condition: not triggered - manifest, lock, active protocol, task spec, and repo state agree."
    assert not is_stop_condition_alert(text)


def test_actual_stopping_message_alerts():
    assert is_stop_condition_alert("Stopping per CGP stop condition. The run prompt and scaffold disagree.")


def test_actual_conflict_message_alerts():
    assert is_stop_condition_alert("Conflict detected: active protocol and manifest disagree on the task.")

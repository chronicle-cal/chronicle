from worker.models import Condition, Action, Rule
from worker.sync.engine import evaluate_condition, apply_actions, apply_rules

from helpers import make_event, make_rule


class TestEvaluateCondition:
    def test_contains_true(self):
        event = make_event(summary="Hello World")
        cond = Condition(field="summary", operator="contains", value="World")
        assert evaluate_condition(event, cond) is True

    def test_contains_false(self):
        event = make_event(summary="Hello World")
        cond = Condition(field="summary", operator="contains", value="Bye")
        assert evaluate_condition(event, cond) is False

    def test_equals_true(self):
        event = make_event(summary="Exact Match")
        cond = Condition(field="summary", operator="equals", value="Exact Match")
        assert evaluate_condition(event, cond) is True

    def test_equals_false(self):
        event = make_event(summary="Exact Match")
        cond = Condition(field="summary", operator="equals", value="No Match")
        assert evaluate_condition(event, cond) is False

    def test_starts_with_true(self):
        event = make_event(summary="Start of sentence")
        cond = Condition(field="summary", operator="starts_with", value="Start")
        assert evaluate_condition(event, cond) is True

    def test_starts_with_false(self):
        event = make_event(description="Not the start")
        cond = Condition(field="description", operator="starts_with", value="Start")
        assert evaluate_condition(event, cond) is False

    def test_ends_with_true(self):
        event = make_event(summary="at the end")
        cond = Condition(field="summary", operator="ends_with", value="end")
        assert evaluate_condition(event, cond) is True

    def test_ends_with_false(self):
        event = make_event(summary="at the end")
        cond = Condition(field="summary", operator="ends_with", value="start")
        assert evaluate_condition(event, cond) is False

    def test_regex_matches(self):
        event = make_event(summary="Lecture: Math 101")
        cond = Condition(field="summary", operator="regex", value=r"Lecture: \w+ \d+")
        assert evaluate_condition(event, cond) is True

    def test_regex_no_match(self):
        event = make_event(summary="Free time")
        cond = Condition(field="summary", operator="regex", value=r"^Lecture")
        assert evaluate_condition(event, cond) is False

    def test_regex_wildcard_matches_all(self):
        event = make_event(summary="Anything goes here")
        cond = Condition(field="summary", operator="regex", value=".*")
        assert evaluate_condition(event, cond) is True

    def test_unknown_operator_returns_false(self):
        event = make_event(summary="anything")
        cond = Condition(field="summary", operator="bad_op", value="anything")
        assert evaluate_condition(event, cond) is False

    def test_missing_field_treated_as_empty_string(self):
        # getattr defaults to "" for unknown fields
        event = make_event()
        cond = Condition(field="nonexistent_field", operator="equals", value="")
        assert evaluate_condition(event, cond) is True

    def test_description_field_is_evaluated(self):
        event = make_event(description="important note")
        cond = Condition(field="description", operator="contains", value="important")
        assert evaluate_condition(event, cond) is True


class TestApplyActions:
    def test_set_field_changes_description(self):
        event = make_event(description="Original")
        actions = [
            Action(type="set_field", field={"name": "description", "value": "New"})
        ]
        result = apply_actions(event, actions)
        assert result.description == "New"

    def test_set_field_changes_summary(self):
        event = make_event(summary="Original")
        actions = [
            Action(type="set_field", field={"name": "summary", "value": "Changed"})
        ]
        result = apply_actions(event, actions)
        assert result.summary == "Changed"

    def test_multiple_set_field_actions_applied_in_order(self):
        event = make_event()
        actions = [
            Action(type="set_field", field={"name": "summary", "value": "S"}),
            Action(type="set_field", field={"name": "description", "value": "D"}),
        ]
        result = apply_actions(event, actions)
        assert result.summary == "S"
        assert result.description == "D"

    def test_unknown_action_type_is_silently_ignored(self):
        event = make_event(summary="Original")
        actions = [Action(type="unsupported", field={"name": "summary", "value": "X"})]
        result = apply_actions(event, actions)
        assert result.summary == "Original"

    def test_empty_actions_list_leaves_event_unchanged(self):
        event = make_event(summary="Unchanged")
        result = apply_actions(event, [])
        assert result.summary == "Unchanged"

    def test_returns_same_event_object(self):
        event = make_event()
        result = apply_actions(event, [])
        assert result is event

    def test_overwrite_field_twice_last_value_wins(self):
        event = make_event(summary="First")
        actions = [
            Action(type="set_field", field={"name": "summary", "value": "Second"}),
            Action(type="set_field", field={"name": "summary", "value": "Third"}),
        ]
        result = apply_actions(event, actions)
        assert result.summary == "Third"


class TestApplyRules:
    def test_rule_applied_when_condition_matches(self):
        event = make_event(summary="Match")
        rules = [make_rule()]
        result = apply_rules(event, rules)
        assert result.description == "Applied"

    def test_rule_skipped_when_condition_does_not_match(self):
        event = make_event(summary="NoMatch", description="Original")
        rules = [make_rule()]
        result = apply_rules(event, rules)
        assert result.description == "Original"

    def test_disabled_rule_is_skipped(self):
        event = make_event(summary="Match", description="Original")
        rules = [make_rule(enabled=False)]
        result = apply_rules(event, rules)
        assert result.description == "Original"

    def test_all_conditions_must_pass_for_rule_to_apply(self):
        event = make_event(summary="Match", description="Desc")
        conds = [
            Condition(field="summary", operator="equals", value="Match"),
            Condition(field="description", operator="equals", value="WrongDesc"),
        ]
        rules = [make_rule(conditions=conds)]
        result = apply_rules(event, rules)
        # Second condition fails → actions not applied
        assert result.description == "Desc"

    def test_multiple_rules_applied_in_order(self):
        """Rule 2 can match based on changes made by Rule 1."""
        event = make_event(summary="Match", description="Start")
        rule1 = make_rule(
            name="rule1",
            conditions=[Condition(field="summary", operator="equals", value="Match")],
            actions=[
                Action(
                    type="set_field",
                    field={"name": "description", "value": "After rule1"},
                )
            ],
        )
        rule2 = Rule(
            enabled=True,
            name="rule2",
            conditions=[
                Condition(field="description", operator="equals", value="After rule1")
            ],
            actions=[
                Action(
                    type="set_field",
                    field={"name": "summary", "value": "After rule2"},
                )
            ],
        )
        result = apply_rules(event, [rule1, rule2])
        assert result.description == "After rule1"
        assert result.summary == "After rule2"

    def test_empty_rules_list_leaves_event_unchanged(self):
        event = make_event(summary="Unchanged")
        result = apply_rules(event, [])
        assert result.summary == "Unchanged"

    def test_empty_conditions_list_applies_actions_unconditionally(self):
        """A rule with no conditions should always pass (all() of empty is True)."""
        event = make_event(description="Original")
        rules = [make_rule()]
        rules[0].conditions = []
        result = apply_rules(event, rules)
        assert result.description == "Applied"

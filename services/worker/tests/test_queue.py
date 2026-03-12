import json
from unittest.mock import MagicMock, patch


class TestRunAction:
    def test_calls_action_function_with_payload(self):
        mock_fn = MagicMock()
        from worker.queue import run_action

        run_action(mock_fn, {"key": "value"})
        mock_fn.assert_called_once_with({"key": "value"})

    def test_catches_exception_and_does_not_propagate(self):
        def bad_action(body):
            raise RuntimeError("intentional failure")

        from worker.queue import run_action

        # Must not raise
        run_action(bad_action, {})


class TestActionsDispatchTable:
    def test_actions_registered(self):
        import worker.queue

        assert "print" in worker.queue.ACTIONS
        assert "long_task" in worker.queue.ACTIONS
        assert "sync" in worker.queue.ACTIONS


class TestCallbackLogic:
    """
    Test the message-dispatch logic inside the RabbitMQ callback in isolation,
    without standing up a real broker.
    """

    def _build_callback(self):
        """
        Re-implement the callback logic extracted from worker.main.py so we can test
        it without touching pika.
        """
        import worker.queue as m

        def callback(ch, method, body):
            try:
                msg = json.loads(body)
                action_type = msg.get("type")
                action = m.ACTIONS.get(action_type)
                if action:
                    m.run_action(action, msg.get("payload"))
                else:
                    m.logging.warning(f"Unknown action type: {action_type}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                m.logging.error(f"Failed to process message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        return callback

    def test_known_action_is_dispatched_and_acknowledged(self):
        import worker.queue as m

        ch = MagicMock()
        method = MagicMock()
        method.delivery_tag = 42
        body = json.dumps({"type": "print", "payload": "hello"}).encode()

        callback = self._build_callback()
        with patch.object(m, "run_action") as mock_run:
            callback(ch, method, body)
            mock_run.assert_called_once()

        ch.basic_ack.assert_called_once_with(delivery_tag=42)
        ch.basic_nack.assert_not_called()

    def test_unknown_action_type_logs_warning_and_acks(self):
        import worker.queue as m

        ch = MagicMock()
        method = MagicMock()
        method.delivery_tag = 1
        body = json.dumps({"type": "does_not_exist", "payload": {}}).encode()

        callback = self._build_callback()
        with patch.object(m.logging, "warning") as mock_warn:
            callback(ch, method, body)
            mock_warn.assert_called_once()

        ch.basic_ack.assert_called_once()

    def test_malformed_json_is_nacked(self):
        ch = MagicMock()
        method = MagicMock()
        method.delivery_tag = 99
        body = b"not valid json {"

        callback = self._build_callback()
        callback(ch, method, body)

        ch.basic_nack.assert_called_once_with(delivery_tag=99, requeue=False)
        ch.basic_ack.assert_not_called()

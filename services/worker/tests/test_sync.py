"""
NOTE: deactivated until integration complete

class TestSyncAction:
    def test_sync_fetches_config_and_runs_engine(self):
        mock_config = MagicMock()
        mock_engine = MagicMock()

        with (
            patch(
                "worker.actions.fetch_sync_config_by_user", return_value=mock_config
            ) as mock_fetch,
            patch("worker.actions.SyncEngine", return_value=mock_engine) as mock_cls,
        ):
            from worker import actions

            actions.sync({"user_id": "user-123"})

            mock_fetch.assert_called_once_with("user-123")
            mock_cls.assert_called_once_with(mock_config)
            mock_engine.run.assert_called_once()

    def test_sync_logs_error_when_db_fetch_fails(self):
        with (
            patch(
                "worker.actions.fetch_sync_config_by_user",
                side_effect=Exception("DB unavailable"),
            ),
            patch("worker.actions.logging") as mock_log,
        ):
            from worker import actions

            # Must not raise
            actions.sync({"user_id": "user-1"})
            mock_log.error.assert_called_once()

    def test_sync_logs_error_when_engine_run_fails(self):
        mock_config = MagicMock()
        mock_engine = MagicMock()
        mock_engine.run.side_effect = Exception("CalDAV timeout")

        with (
            patch("worker.actions.fetch_sync_config_by_user", return_value=mock_config),
            patch("worker.actions.SyncEngine", return_value=mock_engine),
            patch("worker.actions.logging") as mock_log,
        ):
            from worker import actions

            actions.sync({"user_id": "user-1"})
            mock_log.error.assert_called_once()

    def test_sync_missing_user_id_is_caught_and_logged(self):
        with (
            patch(
                "worker.actions.fetch_sync_config_by_user",
                side_effect=KeyError("user_id"),
            ),
            patch("worker.actions.logging") as mock_log,
        ):
            from worker import actions

            actions.sync({})  # no 'user_id' key
            mock_log.error.assert_called_once()

    def test_sync_logs_start_message(self):
        mock_config = MagicMock()
        mock_engine = MagicMock()

        with (
            patch("worker.actions.fetch_sync_config_by_user", return_value=mock_config),
            patch("worker.actions.SyncEngine", return_value=mock_engine),
            patch("worker.actions.logging") as mock_log,
        ):
            from worker import actions

            actions.sync({"user_id": "u1"})
            mock_log.info.assert_called()

"""

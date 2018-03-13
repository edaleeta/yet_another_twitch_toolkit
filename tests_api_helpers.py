"""Tests for api_helpers."""
from unittest import TestCase, mock
import datetime
import server as s
import model as m
from model import connect_to_db, db
from seed_testdb import sample_data
import api_helpers


###############################################################################
# API HELPERS TESTS
###############################################################################


class APIHelpersTestCase(TestCase):
    """Tests API Helpers functions."""

    def setUp(self):
        """Before each test..."""

        # Connect to test db
        connect_to_db(s.app, "postgresql:///testdb", False)

        # If we stop a test midway, let's make sure there's nothing in the db
        # on the next start up.
        db.reflect()
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        db.session.commit()
        sample_data()

    def tearDown(self):
        """After every test..."""

        db.session.close()
        db.reflect()
        db.drop_all()

    def test_create_streams_payload(self):
        """Tests creating payload for returning stream session info."""

        # Construct expected payload.
        user = m.User.query.get(4)
        user_streams = [stream.serialize for stream in user.sessions[:5]]
        next_ts = user_streams[-1]["startedAt"]
        # Datetime is not provided.
        expected_payload = {
            "streams": user_streams,
            "next": f"/api/streams?ts={next_ts}&limit=5"
        }
        
        # Case 1: No date time and limit provided.
        received_payload = api_helpers.create_streams_payload(user)
        self.assertEqual(expected_payload, received_payload)

        # Case 2: Date provided before entries in db.
        dt = datetime.datetime(2017, 12, 12)
        expected_payload = {"streams": []}
        received_payload = api_helpers.create_streams_payload(user, dt=dt)
        self.assertEqual(expected_payload, received_payload)

        # Case 3: Limit 0 provided
        expected_payload = {"streams": []}
        received_payload = api_helpers.create_streams_payload(user, limit=0)
        self.assertEqual(expected_payload, received_payload)
        

if __name__ == "__main__":
    import unittest
    unittest.main()

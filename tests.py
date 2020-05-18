"""Tests for Balloonicorn's Flask app."""

import unittest
import server


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get('/')
        self.assertIn(b'having a party', result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        # Case: RSVP has not been given
        result = self.client.get('/')
        self.assertIn(b'Please RSVP', result.data)
        self.assertNotIn(b'Party Details', result.data)

    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        # Case: RSVP has been given
        rsvp_info = {'name': 'Jane', 'email': 'jane@jane.com'}

        result = self.client.post('/rsvp', data=rsvp_info,
                                  follow_redirects=True)

        self.assertIn(b'Party Details', result.data)
        self.assertNotIn(b'Please RSVP', result.data)

    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        # Case: Exact full name and email match
        rsvp_info = {'name': 'Mel Melitpolski', 'email': 'mel@ubermelon.com'}
        result = self.client.post('/rsvp', data=rsvp_info,
                                    follow_redirects=True)
        self.assertIn(b'Sorry, Mel.', result.data)
        self.assertIn(b'Please RSVP', result.data)
        self.assertNotIn(b'Party Details', result.data)

        # Case: email only match
        rsvp_info = {'name': 'Sneaky', 'email': 'mel@ubermelon.com'}
        result = self.client.post('/rsvp', data=rsvp_info,
                                    follow_redirects=True)
        self.assertIn(b'Sorry, Mel.', result.data)
        self.assertIn(b'Please RSVP', result.data)
        self.assertNotIn(b'Party Details', result.data)

        # Case: Full name only match
        rsvp_info = {'name': 'Mel Melitpolski', 'email': 'sneak@ubermelon.com'}
        result = self.client.post('/rsvp', data=rsvp_info,
                                    follow_redirects=True)
        self.assertIn(b'Sorry, Mel.', result.data)
        self.assertIn(b'Please RSVP', result.data)
        self.assertNotIn(b'Party Details', result.data)

        # Case: Name partial match + different letter case
        rsvp_info = {'name': 'MEL', 'email': 'sneak@ubermelon.com'}
        result = self.client.post('/rsvp', data=rsvp_info,
                                    follow_redirects=True)
        self.assertIn(b'Sorry, Mel.', result.data)
        self.assertIn(b'Please RSVP', result.data)
        self.assertNotIn(b'Party Details', result.data)

        # Case: email different letter case
        rsvp_info = {'name': 'Secret', 'email': 'MEL@UBERmelon.COM'}
        result = self.client.post('/rsvp', data=rsvp_info,
                                    follow_redirects=True)
        self.assertIn(b'Sorry, Mel.', result.data)
        self.assertIn(b'Please RSVP', result.data)
        self.assertNotIn(b'Party Details', result.data)


if __name__ == '__main__':
    unittest.main()

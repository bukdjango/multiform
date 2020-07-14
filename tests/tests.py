from django.test import TestCase, Client


class AppTestCase(TestCase):

    def test_render_1(self):
        r = self.client.get('/')
        self.assertEqual(
            r.status_code, 404
        )
        r = self.client.get('/1')
        self.assertEqual(
            r.status_code, 200
        )
        self.assertIn(
            b'<input type="hidden" name="zxc" value="form1_ctx"',
            r.content,
        )
        self.assertIn(
            b'<input type="hidden" name="zxc" value="form2_ctx"',
            r.content,
        )

    def test_post_1(self):
        r = self.client.post(
            path='/1',
            data={
                'field1': 'a',
                'field2': '2',
            }
        )
        self.assertEqual(
            r.status_code, 400
        )

        r = self.client.post(
            path='/1',
            data={
                'field1': 'a',
                'field2': '2',
                'zxc': 'form1_ctx',
            }
        )
        self.assertEqual(
            r.status_code, 200
        )
        self.assertIn(
            b'Error! Wrong Value!',
            r.content,
        )
        r = self.client.post(
            path='/1',
            data={
                'field1': '1',
                'field2': '2',
                'zxc': 'form1_ctx',
            }
        )
        self.assertNotIn(
            b'Error! Wrong Value!',
            r.content,
        )

        r = self.client.post(
            path='/1',
            data={
                'zxc': 'form2_ctx',
            }
        )
        self.assertIn(
            b'<ul class="errorlist"><li>This field is required',
            r.content,
        )

    def test_render_2(self):
        r = self.client.get('/test')
        self.assertEqual(
            r.status_code, 200
        )
        self.assertIn(
            b'<input type="hidden" name="formtype" value="form2_ctx"',
            r.content,
        )

    def test_post_2(self):
        # form1
        r = self.client.post(
            path='/test',
            data={
                'formtype': 'form1_ctx',
            }
        )
        self.assertEqual(
            r.status_code, 200
        )
        self.assertEqual(
            b'INVALID!form1_ctx',
            r.content,
        )
        r = self.client.post(
            path='/test',
            data={
                'field1': '1',
                'field2': 'a',
                'formtype': 'form1_ctx',
            }
        )
        self.assertEqual(
            r.status_code, 200
        )
        self.assertEqual(
            b'VALID!form1_ctx',
            r.content,
        )

        # form2
        r = self.client.post(
            path='/test',
            data={
                'formtype': 'form2_ctx',
            }
        )
        self.assertEqual(
            r.status_code, 200
        )
        self.assertEqual(
            b'INVALID!form2_ctx',
            r.content,
        )
        r = self.client.post(
            path='/test',
            data={
                'field1': '2',
                'field2': '2',
                'formtype': 'form2_ctx',
            }
        )
        self.assertEqual(
            r.status_code, 200
        )
        self.assertEqual(
            b'VALID!form2_ctx',
            r.content,
        )

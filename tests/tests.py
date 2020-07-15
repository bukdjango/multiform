from django.test import TestCase
from .forms import FormSavedException
from .views import MyMultiFormTemplateView4, MyMultiFormTemplateView3


class AppTestCase(TestCase):

    def test_save(self):
        with self.assertRaises(FormSavedException) as err:
            r = self.client.post(
                '/decoratorview3/6',
                data={
                    'field1': '1',
                    'field2': 'a',
                    'formtype': 'form1_ctx'
                }
            )

    def test_checks(self):
        r = self.client.post(
            '/decoratorview/1',
            data={
                'field1': '1',
                'field2': 'a',
                'formtype': 'form1_ctx'
            }
        )
        self.assertEqual(
            r.status_code, 403
        )
        self.assertEqual(
            b'loginplease', r.content,
        )

    def test_checks2(self):
        r = self.client.post(
            '/decoratorview2/5',
            data={
                'field1': '1',
                'field2': 'a',
                'formtype': 'form1_ctx'
            }
        )
        self.assertEqual(
            r.status_code, 408
        )
        self.assertNotEqual(
            b'loginplease', r.content,
        )

    def test_multiclass_post(self):
        r = self.client.post(
            '/view4/5',
            data={
                'field1': '1',
                'field2': 'a',
                'zxc': 'form4_ctx'
            }
        )
        self.assertEqual(
            r.status_code, 200
        )

        r = self.client.post(
            '/view4/5',
            data={
                'field1': '1',
                'field2': 'a',
                'zxc': 'form2_ctx'
            }
        )
        self.assertEqual(
            r.status_code, 400
        )

        r = self.client.post(
            '/view4/5',
            data={
                'field1': '1',
                'field2': 'a',
                'zxc': 'form1_ctx'
            }
        )
        self.assertEqual(
            r.status_code, 200
        )

    def test_multiclass(self):

        view = MyMultiFormTemplateView3()
        desired = {
            'form3_ctx': {
            },
            'form1_ctx': {
            },
            'form2_ctx': {
            },
        }
        self.assertEqual(
            view.multiforms.keys(),
            desired.keys(),
        )

        view = MyMultiFormTemplateView4()
        print(view.multiforms)
        desired = {
            'form1_ctx': {
            },
            'form4_ctx': {
            },
        }
        self.assertEqual(
            view.multiforms.keys(),
            desired.keys(),
        )

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

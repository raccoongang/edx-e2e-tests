"""
Test uploaded files, aka Assets
"""
from bok_choy.web_app_test import WebAppTest
from regression.pages.studio.asset_index_studio import AssetIndexPageExtended
from regression.pages.studio.utils import upload_new_file
from regression.tests.helpers.api_clients import StudioLoginApi
from regression.tests.helpers.utils import get_course_info


class TestAssetCrud(WebAppTest):

    def test_asset_crud(self):

        """
        Test create/read/update/delete of course assets

        """
        studio_login = StudioLoginApi()
        studio_login.authenticate(self.browser)
        course_info = get_course_info()

        asset_page = AssetIndexPageExtended(
            self.browser,
            course_info['org'],
            course_info['number'],
            course_info['run']
        )
        asset_page.visit()
        asset_page.wait_for_page()
        file_names = [u'README.rst', u'test_pdf.pdf']

        # The course should start with no assets uploaded.
        # There is a bit of Uncertainty Principle here, as we are
        # using the feature itself to set up the course context.
        # TODO: this should be replaced when we have a better
        # mechanism for setting up courses for testing.
        #asset_page.delete_all_assets()  # Put the course in a known state
        # There should be no uploaded assets
        #self.assertEqual(asset_page.asset_files_count, 0)

        # Upload the files
        asset_page.open_upload_file_prompt()
        upload_new_file(asset_page, file_names)
        # Change files name places and
        # Sort files by 'Date Added' and Assert that files have been uploaded.
        file_names[0], file_names[1] = file_names[1], file_names[0]
        asset_page.sort_by_date.click()
        asset_page.sort_by_date.click()
        self.assertIn(file_names[0], asset_page.asset_files_names)
        self.assertIn(file_names[1], asset_page.asset_files_names)

        # Verify that a file can be locked
        asset_page.set_asset_lock()
        # Get the list of locked assets, there should be one
        locked_assets = asset_page.asset_locks(locked_only=True)
        self.assertEqual(len(locked_assets), 1)

        # Confirm that there are 2 assets, with the first
        # locked and the second unlocked.
        all_assets = asset_page.asset_locks(locked_only=False)
        #self.assertEqual(len(all_assets), 2)
        self.assertTrue(all_assets[0].get_attribute('checked'))
        self.assertIsNone(all_assets[1].get_attribute('checked'))

        # Verify that the files can be deleted
        for file_name in file_names:
            if file_name in asset_page.asset_files_names:
                asset_page.delete_asset_named(file_name)
            # Assert files have been deleted.
            #self.assertNotIn(file_names, asset_page.asset_files_names)

        # There should now be no uploaded assets
        self.assertNotIn(file_names[0], asset_page.asset_files_names)
        self.assertNotIn(file_names[1], asset_page.asset_files_names)

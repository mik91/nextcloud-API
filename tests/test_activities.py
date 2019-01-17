from .base import BaseTestCase


class TestActivities(BaseTestCase):

    SUCCESS_CODE = 200

    def test_get_filter_activities(self):
        res = self.nxc.get_activities()
        all_data = res['ocs']['data']
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE

        # test limit
        res = self.nxc.get_activities(limit=1)
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        assert len(res['ocs']['data']) <= 1

        # test ascending sorting
        res = self.nxc.get_activities(sort="asc")
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        data = res['ocs']['data']
        for num in range(1, len(data)):
            assert data[num - 1]['activity_id'] <= data[num]['activity_id']

        # test descending sorting
        res = self.nxc.get_activities(sort="desc")
        assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
        data = res['ocs']['data']
        for num in range(1, len(data)):
            assert data[num - 1]['activity_id'] >= data[num]['activity_id']

        # TODO: add more reliable tests for since, object_id, object_type parameters, if WebDAV Directory API will be
        #  implemented and it will be possible to make files manipulation to create activities from api

        # not reliable test for filter by object_id and object_type
        if len(all_data):
            object_to_filter_by = all_data[0]
            res = self.nxc.get_activities(object_id=object_to_filter_by['object_id'],
                                          object_type=object_to_filter_by['object_type'])
            assert res['ocs']['meta']['statuscode'] == self.SUCCESS_CODE
            data = res['ocs']['data']
            assert len(data) >= 1
            for each in data:
                assert each['object_id'] == object_to_filter_by['object_id']
                assert each['object_type'] == object_to_filter_by['object_type']

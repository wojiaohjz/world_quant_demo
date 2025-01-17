from api.base_api import BaseApi

base_api = BaseApi()


def get_fundamental6_fields(field_type: str = 'MATRIX'):
    searchScope = {
        "instrumentType": "EQUITY",
        "region": "USA",
        "delay": "1",
        "universe": "TOP3000"
    }
    fundamental6 = base_api.get_datafields(searchScope=searchScope, dataset_id="fundamental6")
    return fundamental6[fundamental6['type'] == field_type]['id'].values


def get_news12_fields(field_type: str = 'MATRIX'):
    searchScope = {
        "instrumentType": "EQUITY",
        "region": "USA",
        "delay": "1",
        "universe": "TOP3000"
    }
    news12 = base_api.get_datafields(searchScope=searchScope, dataset_id="news12")
    return news12[news12['type'] == field_type]['id'].values


def get_data_fields(dataset_id: str, field_type: str = 'MATRIX', searchScope: dict = {"instrumentType": "EQUITY",
                                                                         "region": "USA", "delay": "1",
                                                                         "universe": "TOP3000"}):

    datafileds_df = base_api.get_datafields(searchScope=searchScope, dataset_id=dataset_id)
    return datafileds_df[datafileds_df['type'] == field_type]['id'].values


if __name__ == '__main__':
    fileds_list = get_data_fields(dataset_id="fundamental6", field_type='VECTOR')
    print(len(fileds_list))
    print(fileds_list[:20])

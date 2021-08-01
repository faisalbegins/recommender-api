import os
TRENDING_DATA = f'{os.environ.get("DATA_ROOT_DIR")}/trending.data'
POPULAR_DATA = f'{os.environ.get("DATA_ROOT_DIR")}/popular.data'
GENERIC_DATA = f'{os.environ.get("DATA_ROOT_DIR")}/generic.data'
CONTENT_BASED_DATA = f'{os.environ.get("DATA_ROOT_DIR")}/content_based.data'
SIMILARITY_MATRIX = f'{os.environ.get("DATA_ROOT_DIR")}/similarity.matrix'
PERSONALIZED_SVD_RAW = f'{os.environ.get("DATA_ROOT_DIR")}/svd_raw.model'
PERSONALIZED_SVD_DATA = f'{os.environ.get("DATA_ROOT_DIR")}/svd_lookup.data'

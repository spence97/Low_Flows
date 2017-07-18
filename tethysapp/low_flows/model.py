import os
import uuid
import csv
from .app import LowFlows as app


def add_new_thresh(COMID, threshold):
    """
    Persist new dam.
    """
    # Serialize data to json
    threshold_dict = {
        'COMID': '',
        'threshold (cfs)': ''
    }

    # Write to file in app_workspace/Thresholds/UDthresh.csv
    # Make Thresholds dir if it doesn't exist
    app_workspace = app.get_app_workspace()
    threshold_dir = os.path.join(app_workspace.path, 'Thresholds')
    if not os.path.exists(threshold_dir):
        os.mkdir(threshold_dir)

    # Name of the file is its id
    file_name = 'UDThresh.csv'
    file_path = os.path.join(threshold_dir, file_name)

    # Write csv
    with open(file_path, 'w') as f:
        w = csv.DictWriter(f, threshold_dict.keys())
        w.writeheader()
        w.writerow(threshold_dict)

def init_main_db(engine,first_time):
    Base.metadata.create_all(engine)
    if first_time:
        Session = sessionmaker(bind=engine)
        session = Session()
        session.commit()
        session.close()
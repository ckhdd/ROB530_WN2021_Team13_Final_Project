
# NCLT Dataset

Download the dataset using this [script](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/downloader.py)

```
python downloader.py --date="2013-01-10" --vel --gt --gt_cov --sen
cd sensor_data
tar xzf <sensors_data_file_name>
cd ..
cd velodyne_data
tar xzf <velodyne_data_file_name>
```
Change 2013-01-10 to download any dataset you want to work on.

# Kitti Dataset

Download the dataset from [here](http://www.cvlibs.net/datasets/kitti/raw_data.php)
You will need  synced+rectified data, calibration, as well as tracklets for each sequence.
The file structure of the root data directory is as below. Path to the root structure must be included in [kittipoles.py](https://github.com/ckhdd/ROB530_WN2021_Team13_Final_Project/blob/python3_update/Localization/kittipoles.py)

```
-kitti/
  - date/
      - date_drive#_sync/
          - date_drive#_tracklets/
          - image_##/
          - image_##/
          -   ..
          -   ..
          - image_##/
          - oxts/
              - data/
              - dataformat.txt
              - timestamps.txt
          - velodyne_points/
              - data/
              - timestamps.txt
              - timestamps_start.txt
              - timestamps_end.txt
      - calib_cam_to_cam.txt
      - calib_imu_to_velo.txt
      - calib_velo_to_cam.txt
```

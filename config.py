#
# Configuration parameters
#
import os

input_dir = './inputs'
output_dir = './outputs'

# input data directly from Itinerum
input_coordinates_file = input_dir + '/coordinates.csv'
input_survey_responses_file = input_dir + '/survey_responses.csv'

# output files generated by these scripts
output_episodes_file = output_dir + '/episodes.csv'
output_locations_file = output_dir + '/locations.csv'
output_points_file = output_dir + '/classified_points.csv'
output_days_file = output_dir + '/days.csv'
output_compare_file = output_dir + '/compare.csv'

# manual ground truth data for comparison with compare.py
locations_gt = output_dir + '/locations_ground_truth.csv'
activities_gt = output_dir + '/episodes_ground_truth.csv'

# How much time must be spent in one spot for it to be detected as a potential
# activity location? In seconds.
minimum_activity_time = 10*60

# Spatial kernel bandwidth in meters (standard deviation of gaussian kernel)
kernel_bandwidth = 25

# what is the limit of stated h_accuracy which will be acceptable?
# (standard deviation in meters of a normal distribution?)
min_accuracy = 100

# minimum distance between separate clusters
# (parameter for activity location detection)
cluster_distance = 50

location_distance = 150  # meters

# interpolation distance parameter (meters). maximum length of segment to
# remain uninterpolated for linear spatial interpolations.
# For reasonable results, this must be < cluster_distance
interpolation_distance = 30
# Flag for debugging outputs
db_out = True

# Number of worker processes on which to run main.py
#
num_pro = os.cpu_count()
multi_process = True
assert cluster_distance > interpolation_distance

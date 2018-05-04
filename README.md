# cs244r-final-project
CS 244r Final Project

We have implemented all the files in this repository ourselves.

The client_dual_stream/client_single_stream and server_dual_stream/server_single_stream
files are the TCP clients and serves in the dual stream and single stream setups.
The video_transform file takes in spreadsheets that show which frames to keep
and makes videos with only those frames. (So first the TCP clients/servers are
run to determine which frames to keep, and then the video_transform actually
makes the videos with those frames.)

The frame_analyzer file counts the total number of frames in a video and the
pctdrop file drops a given percent of P/B frames. The video_transform file is
used for the percent drop case as well, to put together the videos with frames
given by the output of the pctdrop file.

The IPython notebooks do everything from processing annotations (made by hand
with the LabelImg tool) to implementing and running the object tracking models
and visualizing the results of the model runs. The process_annotations file
processes annotations and stores the locations/dimensions of the hand-annotated
bounding boxes in an output file, and recombines the annotated images into
video form. The process_lossy_vidoes file splits lossy videos into their
component frames. The process_original_videos file splits the original videos
into their component frames and pulls out several-second snippets of the videos
for analysis/testing. The salt_and_pepper file runs Experiment I described
in our paper. The drop_loss file runs Experiment II described in our paper.
The tcp_loss file runs the TCP streaming runs Experiment III described in our paper.
The visualize_results file visualizes the results.

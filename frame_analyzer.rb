require 'aviglitch'

# get the total number of frames in the video
a = AviGlitch.open 'dataset/30pctvid6.avi'
all_frames = []
d = []
a.frames.each_with_index do |f, i|
  d.push(i) if f.is_deltaframe?
  all_frames.push(i)
end
puts all_frames.length
